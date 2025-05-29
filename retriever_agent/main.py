from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np

app = FastAPI()

# Load model and index
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load documents and index
docs = []
doc_dir = os.path.join(os.path.dirname(__file__), "data")
doc_paths = [os.path.join(doc_dir, f) for f in os.listdir(doc_dir) if f.endswith(".txt")]
for path in doc_paths:
    with open(path, "r", encoding="utf-8") as file:
        docs.append(file.read())

doc_embeddings = model.encode(docs, convert_to_numpy=True)
index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(doc_embeddings)

@app.get("/retrieve")
def retrieve_top_k(query: str = Query(...), k: int = 2):
    query_vector = model.encode([query])
    D, I = index.search(query_vector, k)
    results = [docs[i] for i in I[0]]
    return {"chunks": results}
