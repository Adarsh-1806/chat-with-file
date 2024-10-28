from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import requests
import os
import chromadb 

app = FastAPI()

CHROMADB_HOST = os.getenv("CHROMADB_HOST", "chromadb")
CHROMADB_PORT = os.getenv("CHROMADB_PORT", "8000")
CHROMADB_URL = f"http://{CHROMADB_HOST}:{CHROMADB_PORT}"

# Example client setup
chroma_client = chromadb.AsyncHttpClient()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    responses: List[str]

@app.post("/chat", response_model=ChatResponse)
async def chat_interaction(chat: ChatMessage):
    try:
        # Convert message to vector (assuming you have some embedding function)
        embedding = get_embedding(chat.message)

        # Store the embedding
        chroma_client.add(embedding=embedding, text=chat.message)

        # Query similar responses
        results = chroma_client.query(embedding=embedding, top_k=5)
        responses = [result.text for result in results]

        return ChatResponse(responses=responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_embedding(text: str):
    # Placeholder function to get embeddings; replace with real embedding logic
    return [0.0] * 128  # Mock embedding
