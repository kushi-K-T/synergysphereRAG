import uuid
import datetime
from typing import List, Dict, Any
from app.config.settings import settings

class RecursiveChunker:
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    def split_text(self, text: str) -> List[str]:
        cleaned = " ".join(text.split())
        if len(cleaned) <= self.chunk_size:
            return [cleaned] if cleaned else []

        chunks = []
        start = 0
        while start < len(cleaned):
            end = start + self.chunk_size
            chunk = cleaned[start:end]
            if chunk:
                chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def process_document_units(self, doc_units: List[Dict[str, Any]], filename: str) -> List[Dict[str, Any]]:
        all_chunks = []
        for unit in doc_units:
            raw_text = unit.get("text", "")
            page = unit.get("page", 1)
            chunks = self.split_text(raw_text)

            for idx, c in enumerate(chunks):
                chunk_id = f"{filename}_p{page}_c{idx}_{uuid.uuid4().hex[:6]}"
                all_chunks.append({
                    "id": chunk_id,
                    "text": c,
                    "metadata": {
                        "filename": filename,
                        "page": page,
                        "chunk_id": chunk_id,
                        "source_path": unit.get("source", filename),
                        "timestamp": datetime.datetime.utcnow().isoformat()
                    }
                })
        return all_chunks

chunker = RecursiveChunker()