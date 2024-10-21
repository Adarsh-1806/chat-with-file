from fastapi import FastAPI, UploadFile, File
from vector_store import VectorStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

app = FastAPI()

# Initialize VectorStore (FAISS)
vector_store = VectorStore()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    vector_store.store_file(content, file.filename)
    return {"status": "File processed successfully"}

@app.post("/chat")
async def chat(query: dict):
    user_query = query["query"]
    response = vector_store.query(user_query)
    return {"answer": response}
