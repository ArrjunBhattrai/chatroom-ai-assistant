from db.models import Message
from db.models import Query
from db.models import Response
from db.database import SessionLocal
from datetime import datetime

def save_message(message_id, username, channel, message, timestamp):
    db = SessionLocal()
    try:
        msg = Message(
            message_id=message_id,
            username=username,
            channel=channel,
            message=message,
            timestamp=datetime.fromisoformat(timestamp)
        )
        db.add(msg)
        db.commit()
        print("Message saved to DB")
    except Exception as e:
        db.rollback()
        print("Error saving message:", e)
    finally:
        db.close()

def save_query(username: str, channel: str, query_text: str, timestamp: str = None) -> int:
    db = SessionLocal()
    try:
        query = Query(
            username=username,
            channel=channel,
            query_text=query_text,
            timestamp=timestamp or datetime.utcnow()
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return query.id  
    finally:
        db.close()

def save_response(query_id: int, response_text: str, timestamp: str = None) -> int:
    db = SessionLocal()
    try:
        response = Response(
            query_id=query_id,
            response_text=response_text,
            timestamp=timestamp or datetime.utcnow()
        )
        db.add(response)
        db.commit()
        db.refresh(response)
        return response.id
    finally:
        db.close()