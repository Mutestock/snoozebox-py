from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from connection.pg_connection import Base


class Channel(Base):
    __tablename__ = "channel"

    def __init__(
        self,
        id: int = None,
        title: str = None,
        channel_is_alive: bool = None,
        url: bool = None,
    ):
        self.id = id
        self.title = title
        self.channel_is_alive = channel_is_alive
        self.url = url

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    channel_is_alive = Column(Boolean, nullable=False)
    url = Column(String(100))
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), onupdate=func.now())
