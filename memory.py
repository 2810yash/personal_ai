from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Fast embedding model (very important for your system)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create local DB
client = Client(Settings(persist_directory="./memory_db"))

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
        n_results=1
    )

    if results["documents"]:
        return results["documents"][0]
    return []