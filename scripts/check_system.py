import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.local_ai.ollama_client import ollama_client
from app.external_ai.provider import external_provider
from app.rag.vector_store import vector_store

async def main():
    print("--- SynergySphere Diagnostics ---")
    ollama_status = await ollama_client.check_health()
    print(f"Local Ollama Status: {ollama_status}")
    
    ext_status = await external_provider.is_available()
    print(f"External Provider Status: {ext_status}")
    
    print(f"ChromaDB Chunks Indexed: {vector_store.count()}")

if __name__ == "__main__":
    asyncio.run(main())
