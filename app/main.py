import os
import time
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(title="DraftPilot API (Gemini Edition)", version="1.0.0")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from the environment variables or .env file.")

client = genai.Client(api_key=api_key)

request_limits = {}
MAX_REQUESTS_PER_DAY = 2

class ContentRequest(BaseModel):
    topic: str = Field(..., example="Introduction to Python async programming")
    tone: str = Field(default="Professional", example="Casual, Technical, Professional")
    format_type: str = Field(default="Blog Post", example="Blog Post, Twitter Thread, Summary")

@app.get("/")
def home():
    return {"message": "Welcome to DraftPilot API powered by Gemini! Rate limit is 2 requests per day."}

@app.post("/generate")
def generate_content(data: ContentRequest, request: Request):
    client_ip = request.client.host
    now = datetime.now()

    if client_ip in request_limits:
        user_data = request_limits[client_ip]
        if now > user_data["reset_time"]:
            request_limits[client_ip] = {"count": 1, "reset_time": now + timedelta(days=1)}
        else:
            if user_data["count"] >= MAX_REQUESTS_PER_DAY:
                raise HTTPException(
                    status_code=429,
                    detail="Daily limit reached! You can only make 2 requests per day. Try again tomorrow."
                )
            user_data["count"] += 1
    else:
        request_limits[client_ip] = {"count": 1, "reset_time": now + timedelta(days=1)}

    prompt = f"Write a {data.format_type} about '{data.topic}' using a {data.tone} tone."

    # Automatic Retry Loop for 503 Errors
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )
            
            generated_text = response.text
            remaining = MAX_REQUESTS_PER_DAY - request_limits[client_ip]["count"]
            
            return {
                "topic": data.topic,
                "tone": data.tone,
                "result": generated_text,
                "remaining_requests": remaining
            }

        except Exception as e:
            error_msg = str(e)
            # If it's a 503 error and we haven't run out of retries, wait and loop again
            if "503" in error_msg and attempt < max_retries - 1:
                time.sleep(2)
                continue
            
            # If it fails 3 times, or is a different error, raise it to the UI
            raise HTTPException(status_code=500, detail=error_msg)