import os
import time
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from google import genai
from google.genai import types

from app import models
from app.database import engine, get_db

load_dotenv()

# ========================================================
# THE FIX: Force PostgreSQL to create all missing tables
# ========================================================
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DraftPilot API - Phase 3", version="3.0.0")

# --- Startup Event (Mock User for Phase 3) ---
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    if not db.query(models.User).filter(models.User.email == "test@draftpilot.com").first():
        dummy_user = models.User(email="test@draftpilot.com", password_hash="dummyhash")
        db.add(dummy_user)
        db.commit()

# --- Gemini Service Initialization ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "your_actual_api_key_here":
    print("WARNING: Gemini API Key is missing or invalid in .env")
    
client = genai.Client(api_key=api_key) if api_key and api_key != "your_actual_api_key_here" else None

# --- Pydantic Schemas ---
class ContentRequest(BaseModel):
    content_type: str = Field(..., example="LinkedIn Post")
    topic: str = Field(..., example="AI in software development")
    tone: str = Field(default="Professional", example="Professional")
    length: str = Field(default="Medium", example="Medium")
    language: str = Field(default="English", example="English")

# --- Prompt Architecture ---
SYSTEM_PROMPT = """You are an elite, highly adaptable AI content strategist and copywriter. 
Your goal is to produce top-tier, publication-ready content strictly adhering to the user's constraints.
Do not include conversational filler, meta-commentary, or introductory greetings. 
Output ONLY the requested content, formatted beautifully using Markdown where appropriate."""

def build_prompt(data: ContentRequest) -> str:
    return f"""
    Please generate the following content based on the exact parameters below:
    
    [PARAMETERS]
    - Content Type: {data.content_type}
    - Topic: {data.topic}
    - Tone: {data.tone}
    - Length: {data.length}
    - Output Language: {data.language}
    
    [INSTRUCTIONS]
    Ensure the formatting and structure perfectly match the conventions of a {data.content_type}. 
    Write the final output exclusively in {data.language}.
    """

# --- Endpoints ---
@app.post("/generate")
def generate_content(data: ContentRequest, request: Request, db: Session = Depends(get_db)):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini API Key missing in .env file.")
        
    prompt = build_prompt(data)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
            )
            
            new_generation = models.Generation(
                user_id=1, 
                content_type=data.content_type,
                prompt=prompt,
                content=response.text
            )
            db.add(new_generation)
            db.commit()
            db.refresh(new_generation)

            return {"content": response.text, "id": new_generation.id}
            
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/generations")
def get_history(db: Session = Depends(get_db)):
    history = db.query(models.Generation).filter(models.Generation.user_id == 1).order_by(models.Generation.created_at.desc()).all()
    return history

@app.delete("/generations/{generation_id}")
def delete_generation(generation_id: int, db: Session = Depends(get_db)):
    generation = db.query(models.Generation).filter(models.Generation.id == generation_id).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Content not found")
    
    db.delete(generation)
    db.commit()
    return {"message": "Content deleted successfully"}