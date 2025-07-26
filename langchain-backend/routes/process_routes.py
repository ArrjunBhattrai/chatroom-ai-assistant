from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from models.chat import ChatPayload
from orchestrator import process_chat_intelligently

router = APIRouter()

@router.post("/process")
async def process_chat(payload: ChatPayload):
    try:
        result = process_chat_intelligently(payload)
        print("Final JSON Response to send:", result)
        return JSONResponse(content=result)
    except Exception as e:
        print("Summarizer Error:", e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
