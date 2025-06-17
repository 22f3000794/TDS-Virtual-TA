import os
import json
import faiss
import numpy as np
from langchain_nomic import NomicEmbeddings

INDEX_FILE = "discourse.index"
META_FILE = "discourse_meta.json"

# ✅ Ensure API key is set
if not os.getenv("NOMIC_API_KEY"):
    raise EnvironmentError("❌ NOMIC_API_KEY environment variable not set.")

# Load metadata
with open(META_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["text"] for item in data]

# ✅ Initialize embedding model
embedding_model = NomicEmbeddings(model="nomic-embed-text-v1")

# Get embeddings
print(f"🔍 Embedding {len(texts)} discourse entries...")
embeddings = embedding_model.embed_documents(texts)
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save index
faiss.write_index(index, INDEX_FILE)
print(f"✅ Saved {len(texts)} discourse embeddings to {INDEX_FILE}")
