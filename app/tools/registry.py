from typing import Dict, List, Any
from app.tools.base_tool import BaseTool
from app.tools.internal.database_tool import ProjectDatabaseTool
from app.tools.internal.document_tool import DocumentTool
from app.tools.internal.system_status_tool import SystemStatusTool
from app.tools.external.weather_tool import WeatherTool
from app.security.permissions import is_tool_allowed_for_route

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register(ProjectDatabaseTool())
        self.register(DocumentTool())
        self.register(SystemStatusTool())
        self.register(WeatherTool())

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found in registry.")
        return self._tools[name]

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "is_internal": t.is_internal
            }
            for t in self._tools.values()
        ]

    async def execute_tool_safely(self, tool_name: str, route: str, **kwargs) -> Dict[str, Any]:
        if not is_tool_allowed_for_route(tool_name, route):
            raise PermissionError(f"Tool '{tool_name}' is forbidden for route '{route}'.")
        tool = self.get_tool(tool_name)
        return await tool.execute(**kwargs)

tool_registry = ToolRegistry()