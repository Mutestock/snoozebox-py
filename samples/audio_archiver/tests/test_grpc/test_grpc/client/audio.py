
import grpc

from protogen import audio_pb2_grpc, audio_pb2
from utils.config import CONFIG

_CLIENT_CONFIG: str = CONFIG["grpc"]


def _create_stub():
    channel = grpc.insecure_channel(
        f"{_CLIENT_CONFIG['host']}:{_CLIENT_CONFIG['port']}")
    return audio_pb2_grpc.AudioStub(channel)


def create_audio(audio: dict) -> audio_pb2.CreateAudioResponse:
    return _create_stub().CreateAudio(
        audio_pb2.CreateAudioRequest(
            new_audio_object=audio_pb2.NewAudioObject(
                title=audio.get("title"),
                channel_id=audio.get("channel_id"),
                status=audio.get("status"),
                duration=audio.get("duration"),
                url=audio.get("url"),
            )
        )
    )


def read_audio(id) -> audio_pb2.ReadAudioResponse:
    return _create_stub().ReadAudio(
        audio_pb2.ReadAudioRequest(id=id)
    )


def update_audio(id, audio) -> audio_pb2.UpdateAudioResponse:
    return _create_stub().UpdateAudio(audio_pb2.UpdateAudioRequest(
        id=id,
        new_audio_object=audio_pb2.NewAudioObject(
            title=audio.get("title"),
            channel_id=audio.get("id"),
            status=audio.get("status"),
            duration=audio.get("duration"),
            url=audio.get("url"),
        )
    ))


def delete_audio(id) -> audio_pb2.DeleteAudioResponse:
    return _create_stub().DeleteAudio(
        audio_pb2.DeleteAudioRequest(
            id=id
        )
    )


def read_audio_list() -> audio_pb2.ReadAudioListResponse:
    return _create_stub().ReadAudioList(audio_pb2.ReadAudioListRequest())
