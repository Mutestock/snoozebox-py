from logic.handlers.handler_utils.crud_handler_component import (
    CrudHandlerComponent,
)
from logic.handlers.handler_utils.utils_handler_component import (
    UtilsHandlerComponent,
)
from protogen import audio_pb2
from logic.handlers.handler_utils.generic_tools import (
    SUCCESFUL_TRANSACTION,
    make_error_message,
)
from models.audio import Audio
from pipe import map


class AudioHandler:
    def __init__(self):
        self.object_instance = Audio()
        self.crud_component = CrudHandlerComponent(object_instance=self.object_instance)
        self.utils_component = UtilsHandlerComponent(
            object_instance=self.object_instance
        )

    def create(
        self, request: audio_pb2.CreateAudioRequest
    ) -> audio_pb2.CreateAudioResponse:
        try:
            self.crud_component.create(Audio(grpc_audio_object=request))
            return audio_pb2.CreateAudioResponse(msg=SUCCESFUL_TRANSACTION)
        except Exception as e:
            print(e)
            return audio_pb2.CreateAudioResponse(
                msg=make_error_message(e) + " " + str(request)
            )

    def read(
        self, request: audio_pb2.ReadAudioRequest
    ) -> audio_pb2.ReadAudioResponse:
        try:
            audio = self.crud_component.read(request[0])
            return audio_pb2.ReadAudioResponse(
                audio_object=audio.to_grpc_object(), msg=SUCCESFUL_TRANSACTION
            )
        except Exception as e:
            return audio_pb2.ReadAudioResponse(msg=make_error_message(e))

    def update(
        self, request: audio_pb2.UpdateAudioRequest
    ) -> audio_pb2.UpdateAudioResponse:
        try:
            audio = Audio(grpc_audio_object=request[1])
            self.crud_component.update(id=request[0], obj=audio)
            return audio_pb2.UpdateAudioResponse(msg=SUCCESFUL_TRANSACTION)
        except Exception as e:
            return audio_pb2.UpdateAudioResponse(msg=make_error_message(e))

    def delete(
        self, request: audio_pb2.DeleteAudioRequest
    ) -> audio_pb2.DeleteAudioResponse:
        try:
            self.crud_component.delete(id=request[0])
            return audio_pb2.DeleteAudioResponse(msg=SUCCESFUL_TRANSACTION)
        except Exception as e:
            return audio_pb2.DeleteAudioResponse(msg=make_error_message(e))

    def read_list(
        self, request: audio_pb2.ReadAudioListRequest
    ) -> audio_pb2.ReadAudioListResponse:
        try:
            return audio_pb2.ReadAudioListResponse(
                audio_objects=list(
                    self.crud_component.read_list()
                    | map(lambda audio: audio.to_grpc_object())
                ),
                msg=SUCCESFUL_TRANSACTION,
            )
        except Exception as e:
            return audio_pb2.ReadAudioListResponse(msg=make_error_message(e))
