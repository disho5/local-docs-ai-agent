# core/document_loader.py
import os
from pathlib import Path
from PyPDF2 import PdfReader

def load_document(file_path: str) -> str:
    """Loads text from PDF, TXT or MD file."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = file_path.suffix.lower()
    
    if ext == ".pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    
    elif ext in (".txt", ".md"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    else:
        raise ValueError(f"Unsupported format: {ext}. Supported: .pdf, .txt, .md")
