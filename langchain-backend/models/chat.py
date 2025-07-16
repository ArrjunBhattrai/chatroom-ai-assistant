from pydantic import BaseModel
from typing import List

class ChatPayload(BaseModel):
    userQuery: str
    triggerUser: str
    messages: List[str]
