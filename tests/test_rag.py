import pytest
from app.rag.chunker import RecursiveChunker
from app.rag.context_builder import LocalContextBuilder

def test_chunker_splitting():
    chunker = RecursiveChunker(chunk_size=100, chunk_overlap=20)
    text = "SynergySphere is an enterprise AI solution designed for strict local-first privacy. " * 5
    chunks = chunker.split_text(text)
    assert len(chunks) > 1

def test_context_builder_structures_prompt():
    chunks = [{"content": "Private architecture chunk", "metadata": {"filename": "arch.pdf", "page": 2}}]
    sys_prompt, user_prompt = LocalContextBuilder.build_local_prompt("What is arch?", chunks)
    assert "arch.pdf" in user_prompt
    assert "Private architecture chunk" in user_prompt
    assert "Secure Local AI Assistant" in sys_prompt
