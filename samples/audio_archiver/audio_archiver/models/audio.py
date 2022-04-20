from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from connection.pg_connection import Base


class Audio(Base):
    __tablename__: str = "audio"

    def __init__(
        self,
        channel_id: int = None,
        title: str = None,
        status: str = None,
        duration: str = None,
        url: str = None,
    ):
        pass

    id = Column(Integer, primary_key=True, nullable=False)
    channel_id = Column(Integer, ForeignKey("channel.id"))
    title = Column(String(1000), nullable=False)
    status = Column(String(50), nullable=False)
    duration = Column(String(100), Duration=False)
    url = Column(String(200), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), onupdate=func.now())
