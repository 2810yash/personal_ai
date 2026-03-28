from fastapi import FastAPI
import requests
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware
from app.memory import store_memory, search_memory

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"


@app.get("/")
def home():
    return {"message": "Personal AI is running"}


@app.get("/store")
def add_memory(text: str):
    store_memory(text)
    return {"status": "stored"}


@app.get("/ask")
def ask_ai(prompt: str):
    memories = search_memory(prompt)

    print("DEBUG memories:", memories)

    if len(memories) > 0:
        files = [m.split("→")[-1].strip() for m in memories]
        counts = Counter(files)

        context = ", ".join([f"{file} ({count})" for file, count in counts.items()])
    else:
        context = "No past data"

    full_prompt = f"""
You are a personal AI assistant.

Rules:
- Use ONLY the provided user activity
- Do NOT add new assumptions
- Answer in 1 short sentence
- Be direct and specific

User activity:
{context}

Question:
{prompt}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi",
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        }
    )

    return response.json()