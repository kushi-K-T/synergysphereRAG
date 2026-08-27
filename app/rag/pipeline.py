import os
from typing import Dict, Any, List
from app.rag.loaders import DocumentLoader
from app.rag.chunker import chunker
from app.rag.vector_store import vector_store
from app.database.database import SessionLocal
from app.database.models import DocumentRecord

class RAGPipeline:
    def ingest_file(self, file_path: str) -> Dict[str, Any]:
        filename = os.path.basename(file_path)
        doc_units = DocumentLoader.load_file(file_path)
        processed_chunks = chunker.process_document_units(doc_units, filename)

        if not processed_chunks:
            return {"filename": filename, "chunks_ingested": 0, "status": "empty"}

        ids = [c["id"] for c in processed_chunks]
        docs = [c["text"] for c in processed_chunks]
        metadatas = [c["metadata"] for c in processed_chunks]

        vector_store.add_chunks(ids=ids, documents=docs, metadatas=metadatas)

        # Update SQLite Metadata
        db = SessionLocal()
        try:
            record = db.query(DocumentRecord).filter(DocumentRecord.filename == filename).first()
            if not record:
                record = DocumentRecord(
                    filename=filename,
                    file_path=file_path,
                    file_type=os.path.splitext(filename)[1],
                    file_size_bytes=os.path.getsize(file_path),
                    chunk_count=len(processed_chunks),
                    ingested=True
                )
                db.add(record)
            else:
                record.chunk_count = len(processed_chunks)
                record.ingested = True
                record.file_size_bytes = os.path.getsize(file_path)
            db.commit()
        finally:
            db.close()

        return {
            "filename": filename,
            "chunks_ingested": len(processed_chunks),
            "status": "success"
        }

rag_pipeline = RAGPipeline()