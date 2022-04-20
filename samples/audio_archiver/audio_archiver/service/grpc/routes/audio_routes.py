from protogen.audio_pb2_grpc import AudioServicer
from protogen import audio_pb2
from logic.handlers.audio_handler import AudioHandler


class AudioRouter(AudioServicer):
    audio_handler: AudioHandler = AudioHandler()

    def CreateAudio(
        self, request: audio_pb2.CreateAudioRequest, _
    ) -> audio_pb2.CreateAudioResponse:
        return self.audio_handler.create(request)

    def ReadAudio(
        self, request: audio_pb2.ReadAudioRequest, _
    ) -> audio_pb2.ReadAudioResponse:
        return self.audio_handler.read(request)

    def UpdateAudio(
        self, request: audio_pb2.UpdateAudioRequest, _
    ) -> audio_pb2.UpdateAudioResponse:
        return self.audio_handler.update(request)

    def DeleteAudio(
        self, request: audio_pb2.DeleteAudioRequest, _
    ) -> audio_pb2.DeleteAudioRequest:
        return self.audio_handler.delete(request)

    def ReadAudioList(
        self, request: audio_pb2.ReadAudioListRequest, _
    ) -> audio_pb2.ReadAudioListRequest:
        return self.audio_handler.read_list(request)
