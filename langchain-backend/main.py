from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from models.chat import ChatPayload
from orchestrator import process_chat_intelligently  
from routes.message_routes import router as message_router  

app = FastAPI()
app.include_router(message_router)  

@app.middleware("http")
async def log_request(request: Request, call_next):
    body = await request.body()
    print("Raw Request Body:\n", body.decode())
    return await call_next(request)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("Global Error:", repr(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": str(exc)}
    )

@app.post("/process")
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
