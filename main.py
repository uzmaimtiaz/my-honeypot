import os
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 1. Get your secret key from Render's Environment Variables
MY_SECRET_KEY = os.getenv("MY_SECRET_KEY")

@app.post("/chat")
async def handle_scam(request: Request, x_api_key: str = Header(None)):
    # 2. Security Check
    if x_api_key != MY_SECRET_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    
    # 3. Try to read the body, but don't crash if it's weird or different
    try:
        body = await request.json()
        print(f"Message received: {body}")
    except Exception:
        print("Received a request with no valid JSON body.")

    # 4. Return the exact response format GUVI expects
    return {
        "status": "success",
        "reply": "Wait, I don't understand. Why would my account be blocked?"
    }

# This lets you check if the site is up by just clicking the link
@app.get("/")
async def health_check():
    return {"status": "Honeypot is Live!"}
