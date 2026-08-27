from typing import Set

ALLOWED_LOCAL_TOOLS: Set[str] = {
    "project_database",
    "document_search",
    "system_status"
}

ALLOWED_EXTERNAL_TOOLS: Set[str] = {
    "weather",
    "general_lookup"
}

def is_tool_allowed_for_route(tool_name: str, route: str) -> bool:
    if route == "local":
        return tool_name in ALLOWED_LOCAL_TOOLS
    elif route == "external":
        return tool_name in ALLOWED_EXTERNAL_TOOLS
    return False