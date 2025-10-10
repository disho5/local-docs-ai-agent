import chromadb
from chromadb.utils import embedding_functions
import requests
import os

#Using Ollama for embeddings and generation
OLLAMA_URL = "http://localhost:11434/api"
MODEL_NAME = "phi3"  # или "mistral", "llama3"

class RAGEngine:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        # Using Ollama for embeddings
        self.embedding_func = embedding_functions.OllamaEmbeddingFunction(
            model_name=MODEL_NAME,
            url=f"{OLLAMA_URL}/embed"
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=self.embedding_func
        )

    def add_document(self, doc_id: str, text: str):
        """Adds a document to a vector database."""
        self.collection.add(
            ids=[doc_id],
            documents=[text]
        )
        print(f"document {doc_id} added to the database.")

    def query(self, question: str, n_results=3) -> str:
        """Makes a RAG request to LLM"""
        # Find relevant fragments
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )
        
        context = "\n\n".join(results['documents'][0])
        
        # Generate a prompt
        prompt = f"""Use only the following context to answer the question.
If there is no answer in context, say, "I don't know."

Context:
{context}

Question: {question}

Answer:"""

        # Send to Ollama
        response = requests.post(
            f"{OLLAMA_URL}/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7}
            }
        )
        
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            raise Exception(f"Error Ollama: {response.text}")
