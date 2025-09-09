
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import requests

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Excel data at startup
EXCEL_PATH = os.path.join(os.path.dirname(__file__), '../CentralReport1757410209484.xlsx')
data_df = pd.read_excel(EXCEL_PATH)

# Gemini API setup
GEMINI_API_KEY = "AIzaSyDVeFvBen77ocY_Vbk1DD6z2bihDdBg0JM"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

def query_excel(user_message):
    # Simple keyword-based search for groundwater data
    keywords = ["groundwater", "level", "estimation", "assessment", "history", "current", "trend"]
    if any(k in user_message.lower() for k in keywords):
        # Return first 3 rows as a sample (customize as needed)
        return data_df.head(3).to_dict(orient="records")
    return None

def ask_gemini(prompt, context_data=None):
    # Compose the prompt for Gemini
    if context_data:
        prompt = f"User question: {prompt}\nRelevant groundwater data: {context_data}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(GEMINI_API_URL, json=payload)
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "Sorry, I couldn't parse Gemini's response."
    else:
        return f"Gemini API error: {response.text}"

@app.get("/data/summary")
def get_data_summary():
    return {"columns": list(data_df.columns), "rows": len(data_df)}

@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    user_message = body.get("message", "")
    # Try to find relevant groundwater data
    context_data = query_excel(user_message)
    # Ask Gemini with context
    gemini_response = ask_gemini(user_message, context_data)
    return {"response": gemini_response}
