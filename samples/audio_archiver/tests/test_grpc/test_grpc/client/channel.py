import grpc

from protogen import channel_pb2_grpc
from utils.config import CONFIG

_CLIENT_CONFIG: str = CONFIG["grpc"]


def _create_stub():
    channel = grpc.insecure_channel(
        f"{_CLIENT_CONFIG['host']}:{_CLIENT_CONFIG['port']}")
    return channel_pb2_grpc.ChannelStub(channel)


def create_channel(channel):
    return _create_stub().CreateChannelRequest(channel)


def read_channel(id):
    return _create_stub().ReadChannelRequest(id)


def update_channel(id, channel):
    return _create_stub().UpdateChannelRequest(id, channel)


def delete_channel(id):
    return _create_stub().DeleteChannelRequest(id)


def read_channel_list():
    return _create_stub().ReadChannelListRequest()