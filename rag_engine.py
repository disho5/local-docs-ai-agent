# core/rag_engine.py
import chromadb
from chromadb.utils import embedding_functions
import requests
from typing import List, Dict
from .document_loader import load_document
from .chat_history import ChatHistory

OLLAMA_URL = "http://localhost:11434/api"
MODEL_NAME = "phi3"

class RAGEngine:
    def __init__(self, persist_directory="./chroma_db", history_dir="./chat_history"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_func = embedding_functions.OllamaEmbeddingFunction(
            model_name=MODEL_NAME,
            url=f"{OLLAMA_URL}/embed"
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=self.embedding_func
        )
        self.chat_history = ChatHistory(history_dir)

    def add_document(self, file_path: str):
        """Adds a document of any supported format."""
        text = load_document(file_path)
        doc_id = os.path.splitext(os.path.basename(file_path))[0]
        self.collection.add(ids=[doc_id], documents=[text])
        return doc_id

    def query(self, chat_id: str, question: str) -> str:
        # We save the question in history
        self.chat_history.save_message(chat_id, "user", question)

        # Getting context from documents
        results = self.collection.query(query_texts=[question], n_results=3)
        context = "\n\n".join(results['documents'][0]) if results['documents'][0] else "Нет релевантных документов."

        # Getting chat history (only the last 4 messages for context)
        history = self.chat_history.load_history(chat_id)[-4:]
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

        # Forming a prompt with context and history
        prompt = f"""You're a helpful assistant. Answer questions using context and chat history.

Context from the documents:
{context}

Chat history:
{history_text}

New user question:
{question}

Answer briefly and to the point:"""

        # Request to Ollama
        response = requests.post(
            f"{OLLAMA_URL}/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7}
            },
            timeout=120
        )

        if response.status_code == 200:
            answer = response.json()["response"].strip()
            self.chat_history.save_message(chat_id, "assistant", answer)
            return answer
        else:
            error = response.json().get("error", "Unknown error")
            raise Exception(f"Ollama error: {error}")
