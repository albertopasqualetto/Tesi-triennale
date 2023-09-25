# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import arp_pb2 as arp__pb2


class AIMStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getInfo = channel.unary_unary(
            '/arp.AIM/getInfo',
            request_serializer=arp__pb2.InfoRequest.SerializeToString,
            response_deserializer=arp__pb2.InfoResponse.FromString,
        )
        self.work = channel.unary_stream(
            '/arp.AIM/work',
            request_serializer=arp__pb2.JobRequest.SerializeToString,
            response_deserializer=arp__pb2.JobResponse.FromString,
        )


class AIMServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getInfo(self, request, context):
        """
        Get information about the AIM
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def work(self, request, context):
        """
        A generic method to perform the AIM task
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AIMServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'getInfo':
        grpc.unary_unary_rpc_method_handler(
            servicer.getInfo,
            request_deserializer=arp__pb2.InfoRequest.FromString,
            response_serializer=arp__pb2.InfoResponse.SerializeToString,
        ),
        'work':
        grpc.unary_stream_rpc_method_handler(
            servicer.work,
            request_deserializer=arp__pb2.JobRequest.FromString,
            response_serializer=arp__pb2.JobResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler('arp.AIM',
                                                           rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler, ))


# This class is part of an EXPERIMENTAL API.
class AIM(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getInfo(request,
                target,
                options=(),
                channel_credentials=None,
                call_credentials=None,
                insecure=False,
                compression=None,
                wait_for_ready=None,
                timeout=None,
                metadata=None):
        return grpc.experimental.unary_unary(request, target, '/arp.AIM/getInfo',
                                             arp__pb2.InfoRequest.SerializeToString,
                                             arp__pb2.InfoResponse.FromString, options,
                                             channel_credentials, insecure,
                                             call_credentials, compression,
                                             wait_for_ready, timeout, metadata)

    @staticmethod
    def work(request,
             target,
             options=(),
             channel_credentials=None,
             call_credentials=None,
             insecure=False,
             compression=None,
             wait_for_ready=None,
             timeout=None,
             metadata=None):
        return grpc.experimental.unary_stream(request, target, '/arp.AIM/work',
                                              arp__pb2.JobRequest.SerializeToString,
                                              arp__pb2.JobResponse.FromString, options,
                                              channel_credentials, insecure,
                                              call_credentials, compression,
                                              wait_for_ready, timeout, metadata)
