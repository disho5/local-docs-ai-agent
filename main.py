# api/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
import os
import shutil
from core.rag_engine import RAGEngine

app = FastAPI(title="LocalDocs AI", description="A private AI assistant for your documents")

# Engine initialization
engine = RAGEngine()

# Folders
UPLOAD_DIR = "./docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Distribution of static
app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("../static/index.html")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".txt", ".md")):
        raise HTTPException(status_code=400, detail="Only supported .pdf, .txt, .md")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        doc_id = engine.add_document(file_path)
        return {"message": f"Документ '{doc_id}' successfully added!", "doc_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(chat_id: str = Form(...), message: str = Form(...)):
    try:
        response = engine.query(chat_id, message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{chat_id}")
async def get_history(chat_id: str):
    history = engine.chat_history.load_history(chat_id)
    return {"history": history}
