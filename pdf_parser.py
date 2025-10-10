import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def save_text_to_file(text: str, output_path: str):
    """Saves text to a .txt file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    # Example of use
    pdf_file = "docs/sample.pdf"
    if os.path.exists(pdf_file):
        text = extract_text_from_pdf(pdf_file)
        save_text_to_file(text, "docs/sample.txt")
        print("The text has been extracted and saved. в docs/sample.txt")
    else:
        print("File not found. Put it down sample.pdf to the folder docs/")
