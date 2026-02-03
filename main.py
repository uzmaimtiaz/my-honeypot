import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# This looks for the 'MY_SECRET_KEY' you saved in Render's "Environment Variables"
MY_SECRET_KEY = os.getenv("MY_SECRET_KEY")

class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[dict] = []
    metadata: Optional[dict] = {}

@app.post("/chat")
async def handle_scam(request: ScamRequest, x_api_key: str = Header(None)):
    # Verify the password
    if x_api_key != MY_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # LEVEL 1 RESPONSE: Simple success message for the GUVI tester
    return {
        "status": "success",
        "reply": "I don't understand. Why would my account be blocked?"
    }
