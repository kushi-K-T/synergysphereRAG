from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.database.database import SessionLocal
from app.database.models import DocumentRecord, QueryLog

class ProjectDatabaseTool(BaseTool):
    @property
    def name(self) -> str:
        return "project_database"

    @property
    def description(self) -> str:
        return "Fetches metadata on stored documents and system audit logs."

    @property
    def is_internal(self) -> bool:
        return True

    async def execute(self, **kwargs) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            doc_count = db.query(DocumentRecord).count()
            query_count = db.query(QueryLog).count()
            return {
                "status": "success",
                "registered_documents": doc_count,
                "total_queries_logged": query_count
            }
        except Exception as ex:
            return {"status": "error", "message": str(ex)}
        finally:
            db.close()