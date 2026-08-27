from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, json_schema_extra={"example": "Explain our project architecture"})

class SourceCitation(BaseModel):
    filename: str
    page: int
    chunk_id: str
    score: Optional[float] = 0.0

class QueryResponse(BaseModel):
    answer: str
    route: str
    model: str
    sources: List[SourceCitation] = []
    tools_used: List[str] = []
    reason: str
    latency_ms: int

class IngestResponse(BaseModel):
    filename: str
    chunks_ingested: int
    status: str

class HealthResponse(BaseModel):
    status: str
    ollama: str
    chromadb: str
    database: str
    external_ai: str
    mcp: str

class SystemStatusResponse(BaseModel):
    app_name: str
    environment: str
    ollama: Dict[str, Any]
    embedding_model: str
    chroma_collection: str
    vector_chunk_count: int
    external_ai: Dict[str, Any]
    mcp: Dict[str, Any]
    total_stored_documents: int
