from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from routes.message_routes import router as message_router  
from routes.process_routes import router as process_router 

app = FastAPI()

# Include all route modules
app.include_router(message_router)
app.include_router(process_router)

# Logging middleware
@app.middleware("http")
async def log_request(request: Request, call_next):
    body = await request.body()
    print("Raw Request Body:\n", body.decode())
    return await call_next(request)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("Global Error:", repr(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": str(exc)}
    )
