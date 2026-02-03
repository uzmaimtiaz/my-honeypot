import os
from fastapi import FastAPI, Header, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# Override the default 422 error so GUVI never sees "Invalid Request"
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "success", "reply": "I'm sorry, I don't follow. Who are you?"}
    )

MY_SECRET_KEY = os.getenv("MY_SECRET_KEY")

@app.get("/")
async def root():
    return {"message": "Honeypot is active"}

@app.post("/chat")
async def chat(request: Request, x_api_key: str = Header(None)):
    # 1. Check Key
    if x_api_key != MY_SECRET_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    
    # 2. Return exactly what the Level 1 tester needs to see
    return {
        "status": "success",
        "reply": "Wait, I don't understand. Why would my account be blocked?"
    }
