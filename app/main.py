from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config.settings import settings
from app.database.database import init_db
from app.api.routes import router as api_router

def create_application() -> FastAPI:
    # Initialize SQLite Database tables
    init_db()

    app = FastAPI(
        title=settings.APP_NAME,
        description="Dual-path isolated AI service platform for local private RAG and external tasks.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API Routing
    app.include_router(api_router)

    # Static Frontend
    frontend_path = os.path.abspath("./frontend")
    if os.path.exists(frontend_path):
        app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

    return app

app = create_application()