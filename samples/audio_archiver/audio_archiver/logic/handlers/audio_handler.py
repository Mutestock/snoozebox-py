from audio_archiver.logic.handlers.handler_utils.crud_handler_component import CrudHandlerComponent
from audio_archiver.logic.handlers.handler_utils.utils_handler_component import UtilsHandlerComponent
from models.audio import Audio


class AudioHandler:
    def __init__(self):
        self.object_instance = Audio()
        self.crud_component = CrudHandlerComponent(object_instance=self.object_instance)
        self.utils_component = UtilsHandlerComponent(object_instance=self.object_instance)
