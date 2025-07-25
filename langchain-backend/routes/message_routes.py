from fastapi import APIRouter
from pydantic import BaseModel
from services.message_service import save_message

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
    return {"status": "stored"}
