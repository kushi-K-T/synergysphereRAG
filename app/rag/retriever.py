from typing import List, Dict, Any
from app.config.settings import settings
from app.rag.vector_store import vector_store

class LocalRetriever:
    def __init__(self):
        self.store = vector_store

    def retrieve(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        k = top_k or settings.TOP_K
        return self.store.query(query_text=query, top_k=k)

local_retriever = LocalRetriever()