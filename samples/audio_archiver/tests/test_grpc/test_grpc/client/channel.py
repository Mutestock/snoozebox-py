import grpc

from protogen import channel_pb2_grpc, channel_pb2
from utils.config import CONFIG

_CLIENT_CONFIG: str = CONFIG["grpc"]


def _create_stub():
    channel = grpc.insecure_channel(
        f"{_CLIENT_CONFIG['host']}:{_CLIENT_CONFIG['port']}"
    )
    return channel_pb2_grpc.ChannelStub(channel)


def create_channel(channel: dict) -> channel_pb2.CreateChannelResponse:
    return _create_stub().CreateChannel(
        channel_pb2.CreateChannelRequest(
            new_channel_object=channel_pb2.NewChannelObject(
                title=channel.get("title"),
                channel_is_alive=channel.get("channel_is_alive"),
                url=channel.get("url"),
            )
        )
    )


def read_channel(id) -> channel_pb2.ReadChannelResponse:
    return _create_stub().ReadChannel(channel_pb2.ReadChannelRequest(id=id))


def update_channel(id, channel) -> channel_pb2.UpdateChannelResponse:
    return _create_stub().UpdateChannel(
        channel_pb2.UpdateChannelRequest(
            id=id,
            new_channel_object=channel_pb2.NewChannelObject(
                title=channel.get("title"),
                channel_is_alive=channel.get("channel_is_alive"),
                url=channel.get("url"),
            ),
        )
    )


def delete_channel(id) -> channel_pb2.DeleteChannelResponse:
    return _create_stub().DeleteChannel(channel_pb2.DeleteChannelRequest(id=id))


def read_channel_list() -> channel_pb2.ReadChannelListResponse:
    return _create_stub().ReadChannelList(channel_pb2.ReadChannelListRequest())
