from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.local_ai.ollama_client import ollama_client
from app.rag.vector_store import vector_store

class SystemStatusTool(BaseTool):
    @property
    def name(self) -> str:
        return "system_status"

    @property
    def description(self) -> str:
        return "Checks Ollama, ChromaDB, and local vector capacity."

    @property
    def is_internal(self) -> bool:
        return True

    async def execute(self, **kwargs) -> Dict[str, Any]:
        ollama_health = await ollama_client.check_health()
        chroma_count = vector_store.count()
        return {
            "ollama": ollama_health,
            "chroma_chunks": chroma_count,
            "status": "operational"
        }