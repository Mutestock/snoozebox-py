from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from connection.pg_connection import Base
from protogen import channel_pb2


class Channel(Base):
    __tablename__: str = "channel"

    def __init__(
        self,
        id: int = None,
        title: str = None,
        channel_is_alive: bool = None,
        url: bool = None,
        grpc_channel_object: channel_pb2.NewChannelObject = None,
    ) -> None:
        if grpc_channel_object:
            self.title = grpc_channel_object.new_channel_object.title
            self.channel_is_alive = grpc_channel_object.new_channel_object.channel_is_alive
            self.url = grpc_channel_object.new_channel_object.url
        else:
            self.id = id
            self.title = title
            self.channel_is_alive = channel_is_alive
            self.url = url

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    channel_is_alive = Column(Boolean, nullable=False)
    url = Column(String(100))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_grpc_object(self) -> channel_pb2.ChannelObject:
        return channel_pb2.ChannelObject(
            id=self.id,
            title=self.title,
            channel_is_alive=self.channel_is_alive,
            url=self.url,
            updated_at=str(self.updated_at),
            created_at=str(self.created_at),
        )
