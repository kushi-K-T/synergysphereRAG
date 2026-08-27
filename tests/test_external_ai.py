import pytest
from app.external_ai.provider import OpenAICompatibleProvider

@pytest.mark.asyncio
async def test_external_ai_disabled_raises_error():
    provider = OpenAICompatibleProvider()
    provider.enabled = False
    with pytest.raises(RuntimeError) as exc:
        await provider.generate("Hello world")
    assert "disabled in settings" in str(exc.value)
