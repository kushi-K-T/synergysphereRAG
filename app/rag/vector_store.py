import os
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from app.config.settings import settings
from app.rag.embeddings import embedding_service

class LocalVectorStore:
    def __init__(self):
        os.makedirs(settings.CHROMA_PATH, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PATH,
            settings=ChromaSettings(anonymized_telemetry=False, allow_reset=True)
        )
        self.collection_name = settings.CHROMA_COLLECTION
        self._ensure_collection()

    def _ensure_collection(self):
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, ids: List[str], documents: List[str], metadatas: List[Dict[str, Any]]) -> None:
        if not documents:
            return
        embeddings = embedding_service.embed_documents(documents)
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = embedding_service.embed_query(query_text)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        output: List[Dict[str, Any]] = []
        if not results or not results["documents"] or not results["documents"][0]:
            return output

        for i in range(len(results["documents"][0])):
            doc_text = results["documents"][0][i]
            meta = results["metadatas"][0][i] if results["metadatas"] else {}
            dist = results["distances"][0][i] if results["distances"] else 0.0
            output.append({
                "content": doc_text,
                "metadata": meta,
                "score": float(1.0 - dist)
            })
        return output

    def count(self) -> int:
        return self.collection.count()

    def reset(self) -> None:
        self.client.delete_collection(self.collection_name)
        self._ensure_collection()

vector_store = LocalVectorStore()