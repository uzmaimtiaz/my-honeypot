import os  # Added to read environment variables
from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import httpx

app = FastAPI()

# This now pulls from the "MY_API_KEY" variable you set in the Render Dashboard
YOUR_SECRET_API_KEY = os.getenv("MY_API_KEY")

# --- Data Models ---
class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class Metadata(BaseModel):
    channel: str
    language: str
    locale: str

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message]
    metadata: Optional[Metadata]

# --- Intelligence Extraction Helper ---
async def send_final_callback(payload: dict):
    url = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=payload, timeout=10.0)
        except Exception as e:
            print(f"Callback failed: {e}")

# --- API Endpoints ---

@app.get("/")
def health_check():
    return {"status": "running", "message": "Honeypot Agent is active."}

@app.post("/chat")
async def handle_scam(
    request: ScamRequest, 
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(None)
):
    # 2. AUTHENTICATION CHECK
    if x_api_key != YOUR_SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 3. SCAM DETECTION & AGENT LOGIC
    incoming_text = request.message.text.lower()
    
    is_scam = any(word in incoming_text for word in ["block", "verify", "urgent", "bank"])
    
    if is_scam:
        bot_reply = "Oh no! Which bank is this? I need my account for my pension."
        
        final_data = {
            "sessionId": request.sessionId,
            "scamDetected": True,
            "totalMessagesExchanged": len(request.conversationHistory) + 1,
            "extractedIntelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": ["block", "verify"]
            },
            "agentNotes": "Scammer impersonating a bank official."
        }
        background_tasks.add_task(send_final_callback, final_data)
        
        return {"status": "success", "reply": bot_reply}
    
    return {"status": "success", "reply": "I'm not sure I understand."}
