# 🛍️ Customer Sales AI — Product Recommendation System

> An AI-powered product recommendation engine built with Machine Learning and **Endee Vector Database** for semantic similarity search.

---

## 📌 Project Overview

This project transforms a traditional Customer Sales Dashboard into an intelligent recommendation system. By leveraging **Sentence Transformers** for embedding generation and **Endee** as the vector database, the system finds semantically similar products based on sales data — going far beyond simple keyword matching.

**Example:** Search "Laptop" → System recommends "Phone", "Tablet", "Electronics accessories" based on semantic similarity, not just category match.

---

## 🏗️ System Design

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   MySQL (XAMPP) │────▶│  Python ML Pipeline  │────▶│  Endee Vector   │
│   salesdb       │     │  Sentence Transformers│     │  Database       │
│   (Sales Data)  │     │  (384-dim embeddings) │     │  (ANN Search)   │
└─────────────────┘     └──────────────────────┘     └────────┬────────┘
                                                               │
                        ┌──────────────────────┐              │
                        │   Node.js Dashboard  │◀─────────────┤
                        │   Express + EJS      │              │
                        │   Port: 3000         │     ┌────────▼────────┐
                        └──────────────────────┘     │  FastAPI Server │
                                                      │  REST API       │
                                                      │  Port: 8000     │
                                                      └─────────────────┘
```

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Vector Database** | [Endee](https://github.com/endee-io/endee) — High-performance ANN search |
| **ML Embeddings** | Sentence Transformers (`all-MiniLM-L6-v2`, 384-dim) |
| **ML API** | Python + FastAPI |
| **Frontend/Backend** | Node.js + Express + EJS |
| **Sales Database** | MySQL (via XAMPP) |
| **Similarity Metric** | Cosine Similarity |

---

## ✨ Features

- 🔍 **Semantic Product Search** — Find similar products by meaning, not just keywords
- ⚡ **Real-time Recommendations** — Sub-millisecond vector search via Endee
- 🧠 **ML-powered Embeddings** — Sentence Transformers encode product + category + sales context
- 📊 **Sales Dashboard** — Visualize sales data with charts
- 🔗 **REST API** — Clean FastAPI endpoints for recommendations
- 💾 **Persistent Vector Store** — Endee stores embeddings for fast retrieval

---

## 🚀 How Endee is Used

Endee serves as the **core retrieval layer** for this project:

1. **Index Creation** — A `products` index is created in Endee with 384 dimensions (matching MiniLM output) and cosine distance metric
2. **Vector Upsert** — Each product is encoded as a 384-dimensional embedding and stored in Endee with metadata (product name, category, sales amount)
3. **Similarity Search** — When a user queries a product name, it is embedded and searched against Endee using Approximate Nearest Neighbor (ANN) search
4. **Filtered Retrieval** — Top-K similar products are returned with similarity scores

```python
# Endee usage example from this project
from endee import Endee
client = Endee()

# Store product embeddings
client.upsert(index="products", vectors=[{
    "id": "product_0",
    "vector": embedding,  # 384-dim from SentenceTransformer
    "metadata": {"product": "Laptop", "category": "Electronics", "sales_amount": 75000.0}
}])

# Semantic search
results = client.search(index="products", vector=query_embedding, top_k=3)
```

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- XAMPP (MySQL)
- Git

### 1. Star & Fork Endee (Mandatory)

```
⭐ Star: https://github.com/endee-io/endee
🍴 Fork: Click "Fork" on the Endee GitHub page
```

### 2. Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/customer-sales-recommendations.git
cd customer-sales-recommendations
```

### 3. Install Node.js Dependencies

```bash
npm install
```

### 4. Install Python Dependencies

```bash
pip install endee sentence-transformers mysql-connector-python pandas fastapi uvicorn
```

### 5. Setup MySQL Database

Start XAMPP → Start MySQL, then run in phpMyAdmin or MySQL CLI:

```sql
CREATE DATABASE salesdb;
USE salesdb;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100),
  password VARCHAR(100)
);

CREATE TABLE sales (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product VARCHAR(100),
  category VARCHAR(100),
  sales_amount DECIMAL(10,2)
);

INSERT INTO users VALUES (NULL, 'admin', 'admin123');

INSERT INTO sales VALUES
(NULL, 'Laptop', 'Electronics', 75000),
(NULL, 'Phone', 'Electronics', 45000),
(NULL, 'Shirt', 'Clothing', 1500),
(NULL, 'Shoes', 'Clothing', 3000),
(NULL, 'Table', 'Furniture', 12000),
(NULL, 'Headphones', 'Electronics', 8000),
(NULL, 'Sofa', 'Furniture', 25000),
(NULL, 'Jeans', 'Clothing', 2000);
```

### 6. Load Data into Endee Vector DB

```bash
python ml_recommender.py
```

Expected output:
```
✅ Data loaded: (8, 3)
✅ Endee index created!
✅ 8 products stored in Endee!

🔍 Recommendations for 'Laptop':
  → Phone (Electronics) - ₹45000.0
  → Headphones (Electronics) - ₹8000.0
  → Table (Furniture) - ₹12000.0
```

### 7. Start FastAPI Server

```bash
python -m uvicorn recommend_api:app --reload --port 8000
```

### 8. Start Node.js Server

```bash
npm start
```

---

## 🧪 API Usage

### Get Recommendations

```
GET http://localhost:8000/recommend/{product_name}?top_k=3
```

**Example Request:**
```bash
curl http://localhost:8000/recommend/Laptop
```

**Example Response:**
```json
{
  "query": "Laptop",
  "recommendations": [
    {
      "product": "Phone",
      "category": "Electronics",
      "sales_amount": 45000.0,
      "similarity_score": 0.94
    },
    {
      "product": "Headphones",
      "category": "Electronics",
      "sales_amount": 8000.0,
      "similarity_score": 0.87
    }
  ]
}
```

### Via Node.js Dashboard

```
GET http://localhost:3000/api/recommend/{product_name}
```

---

## 📁 Project Structure

```
customer-sales-recommendations/
│
├── ml_recommender.py      # ML pipeline — embeds & stores in Endee
├── recommend_api.py       # FastAPI — recommendation REST API
├── server.js              # Node.js — main server + dashboard routes
├── package.json           # Node.js dependencies
│
├── views/
│   ├── login.html         # Login page
│   └── dashboard.html     # Sales dashboard
│
├── public/                # Static assets (CSS, JS)
├── routes/                # Express routes
├── controllers/           # Route controllers
├── models/                # Data models
└── README.md
```

---

## 🌐 Application URLs

| Service | URL |
|---------|-----|
| Node.js Dashboard | http://localhost:3000 |
| FastAPI Docs (Swagger) | http://localhost:8000/docs |
| Recommendation API | http://localhost:8000/recommend/Laptop |

**Login:** `admin` / `admin123`

---

## 🔗 References

- [Endee Vector Database](https://github.com/endee-io/endee)
- [Endee Documentation](https://docs.endee.io)
- [Sentence Transformers](https://www.sbert.net/)
- [FastAPI](https://fastapi.tiangolo.com/)
