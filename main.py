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

    context = "\n".join(memories) if memories else "No past data"

    full_prompt = f"""
You are a personal AI assistant.

User past activity:
{context}

Question:
{prompt}

Give a short and helpful answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "gemma:2b",
            "prompt": full_prompt,
            "stream": False
        }
    )

    return response.json()