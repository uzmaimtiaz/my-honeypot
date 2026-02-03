from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

# CHANGE THIS to your chosen password!
MY_SECRET_KEY = "rosepetal_secret_key_47921" 

@app.post("/chat")
async def handle_scam(request: dict, x_api_key: str = Header(None)):
    # 1. Check if the password is correct
    if x_api_key != MY_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Wrong Password")
    
    # 2. Return a simple success response
    return {
        "status": "success",
        "reply": "I am interested. Tell me more."
    }
