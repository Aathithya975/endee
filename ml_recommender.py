import mysql.connector
import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd

# MySQL connect
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # ungal password
    database="salesdb"
)

# Sales data fetch
df = pd.read_sql("SELECT product, category, sales_amount FROM sales", conn)
print("Data loaded:", df.shape)

# ChromaDB setup
client = chromadb.Client()
collection = client.get_or_create_collection("products")

# Sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Product text create panni embed pannunga
for i, row in df.iterrows():
    text = f"{row['product']} {row['category']} sales {row['sales_amount']}"
    embedding = model.encode(text).tolist()
    
    collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[{
            "product": row['product'],
            "category": row['category'],
            "sales_amount": float(row['sales_amount'])
        }],
        ids=[f"product_{i}"]
    )

print("ChromaDB-la embeddings stored!")

# Test: Similar products recommend
def recommend(product_name, top_k=3):
    query_embedding = model.encode(product_name).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['metadatas'][0]

# Test pannunga
print("\nRecommendations for 'Laptop':")
recs = recommend("Laptop")
for r in recs:
    print(f"  → {r['product']} ({r['category']}) - ₹{r['sales_amount']}")