from logic.handlers.handler_utils.crud_handler_component import (
    CrudHandlerComponent,
)
from logic.handlers.handler_utils.utils_handler_component import (
    UtilsHandlerComponent,
)
from protogen import channel_pb2
from logic.handlers.handler_utils.generic_tools import (
    SUCCESFUL_TRANSACTION,
    make_error_message,
)
from models.channel import Channel
from pipe import map


class ChannelHandler:
    def __init__(self):
        self.object_instance = Channel()
        self.crud_component = CrudHandlerComponent(object_instance=self.object_instance)
        self.utils_component = UtilsHandlerComponent(
            object_instance=self.object_instance
        )

    def create(
        self, request: channel_pb2.CreateChannelRequest
    ) -> channel_pb2.CreateChannelResponse:
        try:
            self.crud_component.create(Channel(grpc_channel_object=request).__dict__)
            return channel_pb2.CreateChannelResponse(msg=SUCCESFUL_TRANSACTION)
        except Exception as e:
            return channel_pb2.CreateChannelResponse(msg=make_error_message(e))

    def read(
        self, request: channel_pb2.ReadChannelRequest
    ) -> channel_pb2.ReadChannelResponse:
        try:
            channel = self.crud_component.read(request[0])
            return channel_pb2.ReadChannelResponse(
                channel_object=channel.to_grpc_object(), msg=SUCCESFUL_TRANSACTION
            )
        except Exception as e:
            return channel_pb2.ReadChannelResponse(msg=make_error_message(e))

    def update(
        self, request: channel_pb2.UpdateChannelRequest
    ) -> channel_pb2.UpdateChannelResponse:
        try:
            channel = Channel(grpc_channel_object=request[1])
            self.crud_component.update(id=request[0], obj=channel)
            return channel_pb2.UpdateChannelResponse(msg=SUCCESFUL_TRANSACTION)
        except Exception as e:
            return channel_pb2.UpdateChannelResponse(msg=make_error_message(e))

    def delete(
        self, request: channel_pb2.DeleteChannelRequest
    ) -> channel_pb2.DeleteChannelResponse:
        try:
            self.crud_component.delete(id=request[0])
            return channel_pb2.DeleteChannelResponse(msg=SUCCESFUL_TRANSACTION)
        except Exception as e:
            return channel_pb2.DeleteChannelResponse(msg=make_error_message(e))

    def read_list(
        self, request: channel_pb2.ReadChannelListRequest
    ) -> channel_pb2.ReadChannelListResponse:
        try:
            return channel_pb2.ReadChannelListResponse(
                channel_objects=list(
                    self.crud_component.read_list()
                    | map(lambda channel: channel.to_grpc_object())
                ),
                msg=SUCCESFUL_TRANSACTION,
            )
        except Exception as e:
            return channel_pb2.ReadChannelListResponse(msg=make_error_message(e))
