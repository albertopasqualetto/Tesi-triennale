import os
from concurrent import futures
import grpc
from grpc import StatusCode
from rich.console import Console
from pathlib import Path

from mpai_cae_arp.files import File, FileType
from mpai_cae_arp.network import arp_pb2_grpc
from mpai_cae_arp.network.arp_pb2 import (
    JobRequest,
    JobResponse,
    Contact,
    InfoResponse,
    License,
)

from packager import lib

PORT = os.getenv("PORT") or '50051'
info = File(path='config.yml', format=FileType.YAML).get_content()


def error_response(context, status, message):
    context.set_code(status)
    context.set_details(message)
    return JobResponse(status="error", message=message)


class PackagerServicer(arp_pb2_grpc.AIMServicer):

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

        working_dir: Path = Path(request.working_dir)
        files_name: str = request.files_name

        temp_dir = Path(working_dir / 'temp' / files_name)

        yield JobResponse(status="success", message="Job started")

        # By default, AccessCopyFiles directory is created in the output path...
        acf_path = Path(working_dir / 'AccessCopyFiles' / files_name)
        # ...however, if it already exists, the user can decide if it has to be overridden
        make_acf = lib.make_dir(acf_path)

        # noinspection DuplicatedCode
        if make_acf:
            # Copy RestoredAudioFiles
            return_code, message = lib.copy_restored_audio_files(temp_dir, acf_path)
            to_yield = check_return_code(context, return_code, message)
            if to_yield:
                yield to_yield
            console.log("Restored Audio Files copied")
            yield JobResponse(status="success", message="Restored Audio Files copied")

            # Copy Editing List
            return_code, message = lib.copy_editing_list(temp_dir, acf_path)
            to_yield = check_return_code(context, return_code, message)
            if to_yield:
                yield to_yield
            console.log("Editing List copied")
            yield JobResponse(status="success", message="Editing List copied")

            # Create Irregularity Images archive
            return_code, message = lib.create_irregularity_images_archive(temp_dir, acf_path)
            to_yield = check_return_code(context, return_code, message)
            if to_yield:
                yield to_yield
            console.log("Irregularity Images archive created")
            yield JobResponse(status="success", message="Irregularity Images archive created")

            # Copy Irregularity File
            return_code, message = lib.copy_irregularity_file(temp_dir, acf_path)
            to_yield = check_return_code(context, return_code, message)
            if to_yield:
                yield to_yield
            console.log("Irregularity File copied")
            yield JobResponse(status="success", message="Irregularity File copied")


        # Preservation Master Files
        console.log('Creation of Preservation Master Files...')
        yield JobResponse(status="success", message="Creation of Preservation Master Files...")

        # By default, PreservationMasterFiles directory is created in the output path...
        pmf_path = Path(working_dir / 'PreservationMasterFiles' / files_name)
        # ...however, if it already exists, it is possible to skip its creation
        make_pmf = lib.make_dir(pmf_path)

        if make_pmf:
            # Copy Preservation Audio File
            return_code, message = lib.copy_preservation_audio_file(files_name, working_dir, pmf_path)
            to_yield = check_return_code(context, return_code, message)
            if to_yield:
                yield to_yield
            console.log("Preservation Audio File copied")
            yield JobResponse(status="success", message="Preservation Audio File copied")

            # Create Preservation Audio-Visual File with substituted audio
            return_code, message = lib.create_preservation_audio_visual_file(files_name, working_dir, temp_dir, pmf_path)
            to_yield = check_return_code(context, return_code, message)
            if to_yield:
                yield to_yield
            console.log("Preservation Audio-Visual File created")
            yield JobResponse(status="success", message="Preservation Audio-Visual File created")

            # Create Irregularity Images archive
            return_code, message = lib.create_irregularity_images_archive(temp_dir, pmf_path)
            to_yield = check_return_code(context, return_code, message)
            if to_yield:
                yield to_yield
            console.log("Irregularity Images archive created")
            yield JobResponse(status="success", message="Irregularity Images archive created")

            # Copy Irregularity File (already checked)
            return_code, message = lib.copy_irregularity_file(temp_dir, pmf_path)
            to_yield = check_return_code(context, return_code, message)
            if to_yield:
                yield to_yield
            console.log("Irregularity File copied")
            yield JobResponse(status="success", message="Irregularity File copied")

            # End Preservation Master Files
            yield JobResponse(status="success", message="Success!")

        else:
            console.log("\nExit")
            yield JobResponse(status="success", message="Exit")


def check_return_code(context, return_code: lib.ReturnCode, message: str):
    """
    Check the return code of a function and return a JobResponse.

    Parameters
    ----------
    context
        The context of the request.
    return_code : lib.ReturnCode
        The return code of the function.
    message : str
        The message to return.
    """
    match return_code:
        case lib.ReturnCode.ERROR:
            return error_response(context, StatusCode.INVALID_ARGUMENT, message)
        case lib.ReturnCode.WARNING:
            return JobResponse(status="warning", message=message)
        case _:
            return None


def serve(console):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    arp_pb2_grpc.add_AIMServicer_to_server(PackagerServicer(console), server)
    server.add_insecure_port(f'[::]:{PORT}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    console = Console()
    console.print(f'Server started at localhost:{PORT} :satellite:')
    serve(console)
