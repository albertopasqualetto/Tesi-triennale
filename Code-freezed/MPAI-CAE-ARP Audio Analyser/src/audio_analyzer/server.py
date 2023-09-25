import os
from concurrent import futures
from typing import Any, Callable
import grpc
from grpc import StatusCode
from rich.console import Console

from mpai_cae_arp.files import File, FileType
from mpai_cae_arp.types.irregularity import IrregularityFile, Source
from mpai_cae_arp.network import arp_pb2_grpc as arp_pb2_grpc
from mpai_cae_arp.network.arp_pb2 import (
    JobRequest,
    JobResponse,
    Contact,
    InfoResponse,
    License,
)

import audio_analyzer.segment_finder as sf
import audio_analyzer.classifier as cl

info = File(path='config.yml', format=FileType.YAML).get_content()


def try_or_error_response(
    context,
    on_success_message: str,
    on_error_message: str,
    func: Callable,
    args,
    on_success_status: StatusCode = StatusCode.OK,
    on_error_status: StatusCode = StatusCode.INTERNAL,
) -> tuple[JobResponse, Any]:
    try:
        result = func(*args)
        context.set_code(on_success_status)
        context.set_details(on_success_message)
        return JobResponse(status="success", message=on_success_message), result
    except:
        context.set_code(on_error_status)
        context.set_details(on_error_message)
        return JobResponse(status="error", message=on_error_message), None


def error_response(context, status, message):
    context.set_code(status)
    context.set_details(message)
    return JobResponse(status="error", message=message)


class AudioAnalyserServicer(arp_pb2_grpc.AIMServicer):

    def __init__(self, console: Console):
        self.console = console

    def getInfo(self, request, context) -> InfoResponse:
        self.console.log('Received request for AIM info')

        context.set_code(StatusCode.OK)
        context.set_details('Success')

        return InfoResponse(
            title=info['title'],
            description=info['description'],
            version=info['version'],
            contact=Contact(
                name=info['contact']['name'],
                email=info['contact']['email'],
            ),
            license=License(
                name=info['license_info']['name'],
                url=info['license_info']['url'],
            )
        )

    def work(self, request: JobRequest, context):

        self.console.log('Received request for computation')
        self.console.log(request)
        
        working_dir: str = request.working_dir
        files_name: str = request.files_name
        index: int = request.index

        audio_src = os.path.join(working_dir, "PreservationAudioFile", f"{files_name}.wav")
        video_src = os.path.join(working_dir, "PreservationAudioVisualFile", f"{files_name}.mov")

        temp_dir = os.path.join(working_dir, "temp", files_name)
        audio_irreg_1 = os.path.join(temp_dir, "AudioAnalyser_IrregularityFileOutput1.json")
        audio_irreg_2 = os.path.join(temp_dir, "AudioAnalyser_IrregularityFileOutput2.json")
        video_irreg_1 = os.path.join(temp_dir, "VideoAnalyser_IrregularityFileOutput1.json")
        
        if index == 1:

            response, _ = try_or_error_response(
                context=context,
                func=os.makedirs,
                args=[temp_dir],
                on_success_message="Folders created successfully",
                on_error_message="Unable to create temporary directory, output path already exists",
                on_error_status=StatusCode.ALREADY_EXISTS,
            )
            yield response

            response, irreg1 = try_or_error_response(
                context,
                func=sf.create_irreg_file,
                args=(audio_src, video_src),
                on_success_message=f"Found irregularities in Audio source",
                on_error_message="Failed to create irregularity file 1",
            )
            yield response

            try:
                File(path=audio_irreg_1, format=FileType.JSON).write_content(irreg1.to_json())
                context.set_code(StatusCode.OK)
                yield JobResponse(status="success", message="Irregularity file 1 saved to disk")
            except:
                yield error_response(context, StatusCode.INTERNAL, "Failed to save irregularity file 1")

        if index == 2:
            
            audio_irregularity_1 = File(path=audio_irreg_1, format=FileType.JSON).get_content()
            video_irregularity_1 = File(path=video_irreg_1, format=FileType.JSON).get_content()

            response, irreg2 = try_or_error_response(
                context,
                func=sf.merge_irreg_files,
                args=(IrregularityFile.from_json(audio_irregularity_1), IrregularityFile.from_json(video_irregularity_1)),
                on_success_message="Irregularity files merged successfully",
                on_error_message="Failed to merge irregularity files",
            )
            yield response

            response, irreg2 = try_or_error_response(
                context,
                func=sf.extract_audio_irregularities,
                args=(audio_src, irreg2, temp_dir),
                on_success_message="Audio irregularities extracted",
                on_error_message="Failed to extract audio irregularities",
            )
            yield response

            response, irregularities_features = try_or_error_response(
                context,
                func=cl.extract_features,
                args=[irreg2.irregularities],
                on_success_message="Audio irregularities features extracted",
                on_error_message="Failed to extract audio irregularities features",
            )
            yield response

            response, classification_results = try_or_error_response(
                context,
                func=cl.classify,
                args=[irregularities_features],
                on_success_message="Audio irregularities classified",
                on_error_message="Failed to classify audio irregularities",
            )
            yield response

            for irreg, classification_result in zip(irreg2.irregularities, classification_results):
                if irreg.source == Source.AUDIO:
                    irreg.irregularity_type = classification_result.get_irregularity_type()
                    irreg.irregularity_properties = classification_result if classification_result.get_irregularity_type() is not None else None

            File(path=audio_irreg_2, format=FileType.JSON).write_content(irreg2.to_json())
            yield JobResponse(status="success", message="Irregularity file 2 created")


def serve(console):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    arp_pb2_grpc.add_AIMServicer_to_server(AudioAnalyserServicer(console), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    console = Console()
    console.print('Server started at localhost:50051 :satellite:')
    serve(console)
