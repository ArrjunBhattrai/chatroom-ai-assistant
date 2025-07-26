from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    query_text = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    # One-to-many: one query → many responses
    responses = relationship("Response", back_populates="query")


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    response_text = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    # Back reference to query
    query = relationship("Query", back_populates="responses")