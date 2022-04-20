from protogen.channel_pb2_grpc import ChannelServicer
from protogen import channel_pb2
from logic.handlers.channel_handler import ChannelHandler


class ChannelRouter(ChannelServicer):
    channel_handler: ChannelHandler = ChannelHandler()

    def CreateChannel(
        self, request: channel_pb2.CreateChannelRequest, _
    ) -> channel_pb2.CreateChannelResponse:
        return self.channel_handler.create(request)

    def ReadChannel(
        self, request: channel_pb2.ReadChannelRequest, _
    ) -> channel_pb2.ReadChannelResponse:
        return self.channel_handler.read(request)

    def UpdateChannel(
        self, request: channel_pb2.UpdateChannelRequest, _
    ) -> channel_pb2.UpdateChannelResponse:
        return self.channel_handler.update(request)

    def DeleteChannel(
        self, request: channel_pb2.DeleteChannelRequest, _
    ) -> channel_pb2.DeleteChannelRequest:
        return self.channel_handler.delete(request)

    def ReadChannelList(
        self, request: channel_pb2.ReadChannelListRequest, _
    ) -> channel_pb2.ReadChannelListRequest:
        return self.channel_handler.read_list(request)
