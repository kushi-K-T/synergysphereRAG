from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "SynergySphere"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Local Ollama Settings (increased timeout for local CPU/GPU generation)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:8b"
    OLLAMA_TIMEOUT: float = 300.0
    
    # Embedding Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # ChromaDB Configuration
    CHROMA_PATH: str = "./data/chroma"
    CHROMA_COLLECTION: str = "synergysphere_documents"
    
    # RAG Settings
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    TOP_K: int = 3
    
    # External AI Settings
    EXTERNAL_AI_ENABLED: bool = False
    EXTERNAL_AI_PROVIDER: str = "openai"
    EXTERNAL_AI_API_KEY: str = ""
    EXTERNAL_AI_MODEL: str = "gpt-4o-mini"
    EXTERNAL_AI_BASE_URL: str = "https://api.openai.com/v1"
    EXTERNAL_AI_TIMEOUT: float = 30.0
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./data/synergysphere.db"
    
    # MCP Settings
    MCP_ENABLED: bool = False
    MCP_SERVER_URL: str = ""
    
    # Security Settings
    MAX_UPLOAD_SIZE_MB: int = 10
    SENSITIVE_KEYWORDS: str = (
        "confidential,internal,project,architecture,secret,private,budget,"
        "proprietary,financial,database,client,ssn,credential,salary,api_key"
    )

    @property
    def sensitive_keyword_list(self) -> List[str]:
        return [k.strip().lower() for k in self.SENSITIVE_KEYWORDS.split(",") if k.strip()]

settings = Settings()
