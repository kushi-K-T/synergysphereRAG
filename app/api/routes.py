import os
import time
import shutil
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.database.database import get_db
from app.database.models import DocumentRecord, QueryLog
from app.api.schemas import (
    QueryRequest, QueryResponse, SourceCitation,
    IngestResponse, HealthResponse, SystemStatusResponse
)
from app.routing.query_router import query_router
from app.routing.route_types import RouteDestination
from app.security.validators import validate_file_extension, validate_file_size, sanitize_path
from app.local_ai.ollama_client import ollama_client
from app.local_ai.local_llm import local_llm
from app.external_ai.provider import external_provider
from app.external_ai.external_llm import external_llm
from app.rag.retriever import local_retriever
from app.rag.context_builder import context_builder
from app.rag.pipeline import rag_pipeline
from app.rag.vector_store import vector_store
from app.tools.registry import tool_registry
from app.tools.mcp.mcp_client import mcp_client

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    ollama_h = await ollama_client.check_health()
    ext_h = await external_provider.is_available()
    mcp_h = await mcp_client.ping()

    return HealthResponse(
        status="healthy",
        ollama=ollama_h.get("status", "unknown"),
        chromadb="available" if vector_store.count() >= 0 else "error",
        database="available",
        external_ai=ext_h.get("status", "unknown"),
        mcp=mcp_h.get("status", "unknown")
    )

@router.get("/system/status", response_model=SystemStatusResponse)
async def system_status(db: Session = Depends(get_db)):
    ollama_info = await ollama_client.check_health()
    ext_info = await external_provider.is_available()
    mcp_info = await mcp_client.ping()
    doc_count = db.query(DocumentRecord).count()

    return SystemStatusResponse(
        app_name=settings.APP_NAME,
        environment=settings.APP_ENV,
        ollama=ollama_info,
        embedding_model=settings.EMBEDDING_MODEL,
        chroma_collection=settings.CHROMA_COLLECTION,
        vector_chunk_count=vector_store.count(),
        external_ai=ext_info,
        mcp=mcp_info,
        total_stored_documents=doc_count
    )

@router.post("/query", response_model=QueryResponse)
async def process_query(req: QueryRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    decision = query_router.route_query(req.query)
    
    answer = ""
    model_name = ""
    citations: List[SourceCitation] = []
    tools_used: List[str] = []
    error_msg = None

    if decision.route == RouteDestination.LOCAL:
        try:
            chunks = local_retriever.retrieve(req.query, top_k=settings.TOP_K)
            for c in chunks:
                meta = c.get("metadata", {})
                citations.append(SourceCitation(
                    filename=meta.get("filename", "unknown"),
                    page=int(meta.get("page", 1)),
                    chunk_id=meta.get("chunk_id", ""),
                    score=c.get("score", 0.0)
                ))

            system_prompt, full_prompt = context_builder.build_local_prompt(
                query=req.query,
                retrieved_chunks=chunks,
                tool_results=[]
            )

            result = await local_llm.execute(prompt=full_prompt, system_prompt=system_prompt)
            answer = result["text"]
            model_name = f"ollama/{result['model']}"
        except Exception as ex:
            error_msg = str(ex)
            raise HTTPException(
                status_code=503,
                detail=f"Local AI execution failed: {error_msg}. Zero-fallback enforced for sensitive queries."
            )
    else:
        try:
            general_system_prompt = (
                "You are SynergySphere's General Assistant. Answer public and general questions accurately."
            )
            result = await external_llm.execute(prompt=req.query, system_prompt=general_system_prompt)
            answer = result["text"]
            model_name = f"{result.get('provider', 'external')}/{result['model']}"
        except Exception as ex:
            error_msg = str(ex)
            raise HTTPException(
                status_code=502,
                detail=f"External AI execution failed: {error_msg}. Zero-fallback enforced for general queries."
            )

    latency = int((time.time() - start_time) * 1000)

    log_entry = QueryLog(
        query_text=req.query,
        route_selected=decision.route.value,
        model_used=model_name,
        privacy_decision=decision.reason,
        sources_cited=[c.model_dump() for c in citations],
        tools_executed=tools_used,
        success=True,
        error_message=error_msg,
        latency_ms=latency
    )
    db.add(log_entry)
    db.commit()

    return QueryResponse(
        answer=answer,
        route=decision.route.value,
        model=model_name,
        sources=citations,
        tools_used=tools_used,
        reason=decision.reason,
        latency_ms=latency
    )

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    validate_file_extension(file.filename)
    safe_filename = sanitize_path(file.filename)
    
    os.makedirs("./data/documents", exist_ok=True)
    destination = os.path.join("./data/documents", safe_filename)

    file_size = 0
    with open(destination, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            file_size += len(chunk)
            validate_file_size(file_size, settings.MAX_UPLOAD_SIZE_MB)
            buffer.write(chunk)

    ingest_result = rag_pipeline.ingest_file(destination)

    return {
        "filename": safe_filename,
        "size_bytes": file_size,
        "ingest_result": ingest_result
    }

@router.post("/ingest", response_model=List[IngestResponse])
async def trigger_full_ingest():
    doc_dir = "./data/documents"
    if not os.path.exists(doc_dir):
        return []

    results = []
    for f in os.listdir(doc_dir):
        if not f.startswith("."):
            full_path = os.path.join(doc_dir, f)
            if os.path.isfile(full_path):
                res = rag_pipeline.ingest_file(full_path)
                results.append(IngestResponse(**res))
    return results

@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    return db.query(DocumentRecord).all()

@router.get("/tools")
async def get_tools():
    return tool_registry.list_tools()

@router.get("/models")
async def get_models():
    ollama_info = await ollama_client.check_health()
    return {
        "local_ollama": ollama_info,
        "embedding_model": settings.EMBEDDING_MODEL,
        "external_model": settings.EXTERNAL_AI_MODEL if settings.EXTERNAL_AI_ENABLED else "disabled"
    }

@router.get("/config/status")
async def get_config_status():
    return {
        "app_name": settings.APP_NAME,
        "ollama_base_url": settings.OLLAMA_BASE_URL,
        "embedding_model": settings.EMBEDDING_MODEL,
        "external_ai_enabled": settings.EXTERNAL_AI_ENABLED,
        "mcp_enabled": settings.MCP_ENABLED,
        "chunk_size": settings.CHUNK_SIZE,
        "top_k": settings.TOP_K
    }
