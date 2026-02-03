import os
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()

# 1. This grabs your secret password from Render
MY_SECRET_KEY = os.getenv("MY_SECRET_KEY")

@app.post("/chat")
async def handle_scam(request: Request, x_api_key: str = Header(None)):
    # 2. Check the API Key first
    if x_api_key != MY_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # 3. Accept ANY JSON data (Prevents the "INVALID_REQUEST_BODY" error)
    try:
        await request.json()
    except:
        pass 

    # 4. Return the response GUVI expects
    return {
        "status": "success",
        "reply": "Wait, I don't understand. Who is this?"
    }

@app.get("/")
async def health_check():
    return {"status": "Honeypot is Live!"}
