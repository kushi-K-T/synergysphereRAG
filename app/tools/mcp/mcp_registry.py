from typing import List, Dict, Any
from app.tools.mcp.mcp_client import mcp_client

class MCPRegistry:
    def __init__(self):
        self.client = mcp_client

    def list_tools(self) -> List[Dict[str, Any]]:
        if not self.client.enabled:
            return []
        return [{"name": "mcp_generic_tool", "description": "External tool provided via MCP protocol"}]

mcp_registry = MCPRegistry()