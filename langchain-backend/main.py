from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from models.chat import ChatPayload
from chains.summarizer_chain import summarize_chat

app = FastAPI()

# Logging raw body
@app.middleware("http")
async def log_request(request: Request, call_next):
    body = await request.body()
    print("Raw Request Body:\n", body.decode())
    return await call_next(request)

# Global error handler
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
        result = summarize_chat(payload)

        print("Final JSON Response to send:", { "summary": result["summary"] })
        return JSONResponse(content={ "summary": result["summary"] })

    except Exception as e:
        print("Summarizer Error:", e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
