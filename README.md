# Personal AI (FastAPI + local memory)

Small FastAPI service that:

- Stores text “memories” in a local ChromaDB collection (persisted to `./memory_db/`)
- Retrieves relevant memories for a prompt
- Sends the prompt + memory context to a local Ollama model

## Requirements

- Python 3.10+ recommended
- Ollama running locally at `http://localhost:11434`
- The model used in code: `gemma:2b`

## Setup

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

Service defaults to `http://127.0.0.1:8000`.

## API

- `GET /` → health message
- `GET /store?text=...` → stores a memory string
- `GET /ask?prompt=...` → searches memory and asks the Ollama model

Example:

```bash
curl "http://127.0.0.1:8000/store?text=I%20like%20coffee"
curl "http://127.0.0.1:8000/ask?prompt=What%20do%20I%20like%3F"
```

## Notes

- Memories are persisted in `memory_db/` (ignored by git via `.gitignore`).
- If Ollama isn’t running or the model isn’t available, `/ask` will fail with the upstream error response.

