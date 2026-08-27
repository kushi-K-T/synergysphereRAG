import pytest
from app.tools.registry import tool_registry

@pytest.mark.asyncio
async def test_tool_permission_isolation():
    with pytest.raises(PermissionError):
        await tool_registry.execute_tool_safely("document_search", route="external")
