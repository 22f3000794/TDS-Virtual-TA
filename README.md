license: mit  
title: TDS-Virtual-TA  
sdk: docker  
emoji: 🔥  
colorFrom: blue  
colorTo: indigo  
short_description: A virtual TA for TDS course  

# TDS Virtual TA 🤖📘

This is a Virtual Teaching Assistant (TA) for the **Tools in Data Science (TDS)** course (Jan–Apr 2025).  
It answers student questions based on course content and instructor replies on the TDS Discourse forum.

## 🔍 Features

- Accepts natural language questions from students
- Returns clear, concise answers (like a smart TA)
- Uses two knowledge bases:
  - 📘 TDS course materials (scraped from [tds.s-anand.net](https://tds.s-anand.net))
  - 💬 Instructor/TA replies from Discourse (Jan–Apr 2025)
- Optionally supports image input (e.g. screenshots of questions)
- Provides source links to course/discourse pages
- Powered by [AI Pipe](https://aiproxy.s-anand.net) for answer generation
- Uses Nomic Embeddings for semantic similarity

## 🚀 How it works

When a question is sent:

1. It is embedded using `nomic-embed-text-v1` via Nomic API
2. It is searched against course and forum content using FAISS (cosine similarity)
3. The most relevant context is sent to AI Pipe
4. The final summarized answer is returned, with helpful source links

## 🧠 Model + Embeddings

- **Embeddings:** `nomic-embed-text-v1` via [Nomic API](https://docs.nomic.ai/)
- **Answer Generation:** `gpt-4.1-nano` via [AI Pipe](https://aiproxy.s-anand.net)
- **Vector Search:** FAISS (cosine similarity)
- **Caching:** Local index files (`.index` and `.json`)

## 🛠 API Usage

### `POST /api/`

Send a POST request with the following JSON:

```json
{
  "question": "What is CORS?",
  "image": "optional base64 image string"
}

{
  "answer": "Summarized answer...",
  "links": [
    {
      "url": "https://tds.s-anand.net/...",
      "text": "Answer from course content"
    }
  ]
}

🌐 Deployment

Deployed on Hugging Face Spaces using FastAPI + Docker.
Make sure to call the /api/ endpoint via POST request.

👩‍💻 Developer:

Developed by Garima 
For the TDS Jan–Apr 2025 course project.


