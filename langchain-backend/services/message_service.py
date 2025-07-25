from db.models import Message
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
