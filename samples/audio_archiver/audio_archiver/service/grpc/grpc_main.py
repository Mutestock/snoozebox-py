import grpc
from concurrent import futures

from utils.config import CONFIG
from protogen.audio_pb2_grpc import add_AudioServicer_to_server
from protogen.channel_pb2_grpc import (
    
    add_ChannelServicer_to_server,
)

from service.grpc.routes.audio_routes import AudioRouter
from service.grpc.routes.channel_routes import ChannelRouter


def run_grpc() -> None:
    uri = f"{CONFIG.get('grpc').get('host')}:{CONFIG.get('grpc').get('port')}"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    print(f"GRPC: running on {uri}")
    add_AudioServicer_to_server(AudioRouter(), server)
    add_ChannelServicer_to_server(ChannelRouter(), server)
    server.add_insecure_port(uri)
    server.start()
    server.wait_for_termination()
