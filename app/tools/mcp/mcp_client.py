from typing import Dict, Any
from app.config.settings import settings

class MCPClient:
    def __init__(self):
        self.enabled = settings.MCP_ENABLED
        self.server_url = settings.MCP_SERVER_URL

    async def ping(self) -> Dict[str, Any]:
        if not self.enabled:
            return {"status": "disabled", "message": "MCP is disabled in configuration."}
        return {"status": "ready", "server": self.server_url}

    async def call_tool(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if not self.enabled:
            raise RuntimeError("Cannot execute MCP tool: MCP layer is disabled.")
        return {"status": "success", "mcp_tool": name, "result": "MCP mocked response"}

mcp_client = MCPClient()