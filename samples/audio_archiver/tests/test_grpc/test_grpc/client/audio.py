import grpc

from protogen import audio_pb2_grpc
from utils.config import CONFIG

_CLIENT_CONFIG: str = CONFIG["grpc"]


def _create_stub():
    channel = grpc.insecure_channel(
        f"{_CLIENT_CONFIG['host']}:{_CLIENT_CONFIG['port']}")
    return audio_pb2_grpc.AudioStub(channel)


def create_audio(audio):
    return _create_stub().CreateAudio(audio)


def read_audio(id):
    return _create_stub().ReadAudio(id)


def update_audio(id, audio):
    return _create_stub().UpdateAudio(id, audio)


def delete_audio(id):
    return _create_stub().DeleteAudio(id)


def read_audio_list():
    return _create_stub().ReadAudioList()