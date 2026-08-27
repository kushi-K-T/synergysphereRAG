import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.database import init_db
from app.rag.pipeline import rag_pipeline

def run():
    print("=== SynergySphere Document Ingestion ===")
    init_db()
    docs_path = "./data/documents"
    if not os.path.exists(docs_path):
        print(f"Error: Directory {docs_path} not found.")
        return

    files = [os.path.join(docs_path, f) for f in os.listdir(docs_path) if not f.startswith(".")]
    if not files:
        print("No documents found to ingest.")
        return

    for file_path in files:
        print(f"Ingesting: {file_path}")
        result = rag_pipeline.ingest_file(file_path)
        print(f" -> Result: {result}")

    print("Ingestion complete.")

if __name__ == "__main__":
    run()
