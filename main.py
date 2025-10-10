import os
import sys
from pdf_parser import extract_text_from_pdf
from rag_engine import RAGEngine

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python main.py add <pdf_file>")
        print("  python main.py ask <question>")
        return

    command = sys.argv[1]
    engine = RAGEngine()

    if command == "add":
        pdf_path = sys.argv[2]
        if not os.path.exists(pdf_path):
            print("File not found!")
            return
        text = extract_text_from_pdf(pdf_path)
        doc_id = os.path.basename(pdf_path).replace(".pdf", "")
        engine.add_document(doc_id, text)
        print(f"✅ Document '{doc_id}' added!")

    elif command == "ask":
        question = " ".join(sys.argv[2:])
        try:
            answer = engine.query(question)
            print(f"🤖 Answer: {answer}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
