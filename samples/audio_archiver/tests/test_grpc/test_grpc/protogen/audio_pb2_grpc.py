# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protogen.audio_pb2 as audio__pb2


class AudioStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateAudio = channel.unary_unary(
                '/audio.Audio/CreateAudio',
                request_serializer=audio__pb2.CreateAudioRequest.SerializeToString,
                response_deserializer=audio__pb2.CreateAudioResponse.FromString,
                )
        self.ReadAudio = channel.unary_unary(
                '/audio.Audio/ReadAudio',
                request_serializer=audio__pb2.ReadAudioRequest.SerializeToString,
                response_deserializer=audio__pb2.ReadAudioResponse.FromString,
                )
        self.UpdateAudio = channel.unary_unary(
                '/audio.Audio/UpdateAudio',
                request_serializer=audio__pb2.UpdateAudioRequest.SerializeToString,
                response_deserializer=audio__pb2.UpdateAudioResponse.FromString,
                )
        self.DeleteAudio = channel.unary_unary(
                '/audio.Audio/DeleteAudio',
                request_serializer=audio__pb2.DeleteAudioRequest.SerializeToString,
                response_deserializer=audio__pb2.DeleteAudioResponse.FromString,
                )
        self.ReadAudioList = channel.unary_unary(
                '/audio.Audio/ReadAudioList',
                request_serializer=audio__pb2.ReadAudioListRequest.SerializeToString,
                response_deserializer=audio__pb2.ReadAudioListResponse.FromString,
                )


class AudioServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateAudio(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReadAudio(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateAudio(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteAudio(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReadAudioList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AudioServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateAudio': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAudio,
                    request_deserializer=audio__pb2.CreateAudioRequest.FromString,
                    response_serializer=audio__pb2.CreateAudioResponse.SerializeToString,
            ),
            'ReadAudio': grpc.unary_unary_rpc_method_handler(
                    servicer.ReadAudio,
                    request_deserializer=audio__pb2.ReadAudioRequest.FromString,
                    response_serializer=audio__pb2.ReadAudioResponse.SerializeToString,
            ),
            'UpdateAudio': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateAudio,
                    request_deserializer=audio__pb2.UpdateAudioRequest.FromString,
                    response_serializer=audio__pb2.UpdateAudioResponse.SerializeToString,
            ),
            'DeleteAudio': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteAudio,
                    request_deserializer=audio__pb2.DeleteAudioRequest.FromString,
                    response_serializer=audio__pb2.DeleteAudioResponse.SerializeToString,
            ),
            'ReadAudioList': grpc.unary_unary_rpc_method_handler(
                    servicer.ReadAudioList,
                    request_deserializer=audio__pb2.ReadAudioListRequest.FromString,
                    response_serializer=audio__pb2.ReadAudioListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'audio.Audio', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Audio(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateAudio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/audio.Audio/CreateAudio',
            audio__pb2.CreateAudioRequest.SerializeToString,
            audio__pb2.CreateAudioResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReadAudio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/audio.Audio/ReadAudio',
            audio__pb2.ReadAudioRequest.SerializeToString,
            audio__pb2.ReadAudioResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateAudio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/audio.Audio/UpdateAudio',
            audio__pb2.UpdateAudioRequest.SerializeToString,
            audio__pb2.UpdateAudioResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteAudio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/audio.Audio/DeleteAudio',
            audio__pb2.DeleteAudioRequest.SerializeToString,
            audio__pb2.DeleteAudioResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReadAudioList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/audio.Audio/ReadAudioList',
            audio__pb2.ReadAudioListRequest.SerializeToString,
            audio__pb2.ReadAudioListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
