from fastapi import FastAPI
import requests
from memory import store_memory, search_memory

app = FastAPI()

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

    context = "\n".join(memories) if len(memories) > 0 else "No past data"

    full_prompt = f"""
You are a personal AI assistant.

User past activity:
{context}

Instructions:
- Analyze ALL activities
- Mention multiple tasks if present
- Be specific

Question:
{prompt}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi",
            "prompt": full_prompt,
            "stream": False
        }
    )

    return response.json()