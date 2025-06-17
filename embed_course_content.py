import os
import re
import glob
import json
import numpy as np
import faiss
from datetime import datetime
from langchain_nomic import NomicEmbeddings

# ✅ Ensure API key is set
if not os.getenv("NOMIC_API_KEY"):
    raise EnvironmentError("❌ NOMIC_API_KEY environment variable not set.")

# CONFIG
MD_DIR = "markdown_files"
INDEX_FILE = "course_content.index"
META_FILE = "course_content_meta.json"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ✅ Specify the model name here
model = NomicEmbeddings(model="nomic-embed-text-v1")  # You can use "nomic-embed-text-v1" or another supported name

def clean_ui_artifacts(text):
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[\]\([^\)]*\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\(\#?\)', r'\1', text)
    text = text.replace("Copy to clipboard", "").replace("ErrorCopied", "").replace("Code snippet", "")
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_links(text):
    return re.findall(r'https:\/\/[^\s\)]+', text)

def extract_frontmatter(md_text):
    match = re.match(r'^---\n(.*?)\n---\n(.*)', md_text, flags=re.DOTALL)
    if match:
        frontmatter_raw, content = match.groups()
        frontmatter = {}
        for line in frontmatter_raw.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"')
        return frontmatter, content
    else:
        return {}, md_text

def chunk_text(text, max_len=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_len, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = end - overlap
    return chunks

# Embedding logic
all_chunks = []
metadata = []

for filepath in glob.glob(os.path.join(MD_DIR, "*.md")):
    with open(filepath, "r", encoding="utf-8") as f:
        md_text = f.read()

    frontmatter, content = extract_frontmatter(md_text)
    cleaned = clean_ui_artifacts(content)
    chunks = chunk_text(cleaned)

    for i, chunk in enumerate(chunks):
        links = extract_links(chunk)
        all_chunks.append(chunk)
        metadata.append({
            "source_file": os.path.basename(filepath),
            "text": chunk,
            "original_url": frontmatter.get("original_url", "URL not available"),
            "extra_links": links
        })

print(f"🔍 Embedding {len(all_chunks)} chunks...")

embeddings = model.embed_documents(all_chunks)
embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, INDEX_FILE)
with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print(f"✅ Done. Index: {INDEX_FILE}, Metadata: {META_FILE}")
