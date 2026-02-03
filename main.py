import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 1. Get the key from your Render settings
MY_SECRET_KEY = os.getenv("MY_SECRET_KEY")

@app.post("/chat")
async def chat(request: Request):
    # 2. Manually grab the key from headers (the "Smart Guard")
    # This looks for 'x-api-key' no matter how it's sent
    provided_key = request.headers.get("x-api-key")
    
    # 3. Security Check
    if provided_key != MY_SECRET_KEY:
        return JSONResponse(
            status_code=401, 
            content={"detail": "Unauthorized - Key Mismatch"}
        )
        
    
    # 4. Success Response
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "reply": "I'm sorry, I don't understand. Why would my account be blocked?"
        }
    )

@app.get("/")
async def root():
    return {"message": "Honeypot is active"}

# Catch-all to prevent the "Invalid Request Body" error from popping up
@app.exception_handler(Exception)
async def universal_handler(request, exc):
    return JSONResponse(
        status_code=200,
        content={"status": "success", "reply": "I'm listening..."}
    )
