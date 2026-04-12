from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from sentence_transformers import SentenceTransformer

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = chromadb.Client()
collection = client.get_or_create_collection("products")
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.get("/recommend/{product_name}")
def recommend(product_name: str, top_k: int = 3):
    embedding = model.encode(product_name).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return {
        "query": product_name,
        "recommendations": results['metadatas'][0]
    }