from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from connection.pg_connection import Base
from protogen import audio_pb2


class Audio(Base):
    __tablename__: str = "audio"

    def __init__(
        self,
        title: str = None,
        channel_id: int = None,
        status: str = None,
        duration: str = None,
        url: str = None,
        grpc_audio_object: audio_pb2.NewAudioObject = None,
    ):
        if grpc_audio_object:
            self.channel_id = grpc_audio_object.channel_id
            self.title = grpc_audio_object.title
            self.status = grpc_audio_object.status
            self.duration = grpc_audio_object.duration
            self.url = grpc_audio_object.url
        else:    
            self.channel_id = channel_id
            self.title = title
            self.status = status
            self.duration = duration
            self.url = url

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    channel_id = Column(Integer, ForeignKey("channel.id"))
    title = Column(String(1000), nullable=False)
    status = Column(String(50), nullable=False)
    duration = Column(String(100), nullable=False)
    url = Column(String(200), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_grpc_object(self) -> audio_pb2.AudioObject:
        return audio_pb2.AudioObject(
            id=self.id,
            channel_id=self.channel_id,
            title=self.title,
            status=self.status,
            duration=self.duration,
            url=self.url,
            updated_at=str(self.updated_at),
            created_at=str(self.created_at),
        )
