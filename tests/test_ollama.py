import pytest
from unittest.mock import AsyncMock, patch
from app.local_ai.ollama_client import OllamaClient

@pytest.mark.asyncio
async def test_ollama_failure_raises_runtime_error():
    client = OllamaClient()
    with patch("httpx.AsyncClient.post", side_effect=Exception("Connection refused")):
        with pytest.raises(RuntimeError) as exc_info:
            await client.generate_response("Hello")
        assert "Local AI failure" in str(exc_info.value)
