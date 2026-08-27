import os
from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.config.settings import settings

class DocumentTool(BaseTool):
    @property
    def name(self) -> str:
        return "document_search"

    @property
    def description(self) -> str:
        return "Inspects local file storage for available sensitive documents."

    @property
    def is_internal(self) -> bool:
        return True

    async def execute(self, **kwargs) -> Dict[str, Any]:
        doc_dir = "./data/documents"
        if not os.path.exists(doc_dir):
            return {"status": "error", "message": "Directory does not exist"}

        files = [f for f in os.listdir(doc_dir) if not f.startswith(".")]
        return {
            "status": "success",
            "document_count": len(files),
            "files": files
        }