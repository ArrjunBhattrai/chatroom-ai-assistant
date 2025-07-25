from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from db.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
