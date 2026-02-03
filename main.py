import os
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# This pulls the key from your Render Environment Variables
MY_SECRET_KEY = os.getenv("MY_SECRET_KEY")

# This is the "Shape" of the data GUVI sends. 
# If this is missing, you get the 'INVALID_REQUEST_BODY' error.
class Message(BaseModel):
    sender: str
    text: str

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[dict]] = []

@app.post("/chat")
async def handle_scam(request: ScamRequest, x_api_key: str = Header(None)):
    # 1. Check the API Key
    if x_api_key != MY_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # 2. Level 1 Response: Just a simple reply to pass the test
    return {
        "status": "success",
        "reply": "Wait, I don't understand. Who is this?"
    }

# Optional: Add a simple GET route so you can check if the site is up in your browser
@app.get("/")
async def root():
    return {"message": "Honeypot is Live!"}
