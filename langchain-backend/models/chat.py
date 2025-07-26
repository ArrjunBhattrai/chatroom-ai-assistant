from pydantic import BaseModel
from typing import List
from datetime import datetime

class Message(BaseModel):
    username: str
    content: str
    timestamp: datetime
    id: str

class ChatPayload(BaseModel):
    userQuery: str
    triggerUser: str
    channel: str                     
