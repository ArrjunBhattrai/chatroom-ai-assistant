from fastapi import APIRouter
from pydantic import BaseModel
from services.message_service import save_message
from chroma.vector_store import add_message_to_vector_store

router = APIRouter()

class MessagePayload(BaseModel):
    message_id: str
    username: str
    channel: str
    message: str
    timestamp: str  

@router.post("/storeMessage")
def store_message(payload: MessagePayload):
    save_message(
        message_id=payload.message_id,
        username=payload.username,
        channel=payload.channel,
        message=payload.message,
        timestamp=payload.timestamp
    )

    add_message_to_vector_store(
        text=payload.message,
        metadata={
            "username": payload.username,
            "channel": payload.channel,
            "timestamp": payload.timestamp,
        }
    )
    return {"status": "Message stored and embedded"}
