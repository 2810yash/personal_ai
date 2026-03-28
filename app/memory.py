import chromadb
import os
from sentence_transformers import SentenceTransformer

# Absolute path (FIX)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "memory_db")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent DB
client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(name="memory")


def store_memory(text):
    embedding = model.encode(text).tolist()
    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(hash(text))]
    )


def search_memory(query):
    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    if results["documents"] and len(results["documents"]) > 0:
        return results["documents"][0]
    return []