import httpx
from typing import Dict, Any, Optional
from app.config.settings import settings

class OllamaClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip('/')
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT

    async def check_health(self) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    models = res.json().get("models", [])
                    available_model_names = [m.get("name") for m in models]
                    return {
                        "status": "available",
                        "model_configured": self.model,
                        "model_present": any(self.model in name for name in available_model_names),
                        "available_models": available_model_names
                    }
                return {"status": "error", "error": f"HTTP {res.status_code}"}
        except Exception as ex:
            return {"status": "unavailable", "error": str(ex)}

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(f"{self.base_url}/api/generate", json=payload)
                if res.status_code == 200:
                    return res.json().get("response", "")
                raise RuntimeError(f"Ollama server returned status code {res.status_code}: {res.text}")
        except httpx.ConnectError:
            raise RuntimeError(
                "Local AI unavailable: Could not establish connection to local Ollama server at "
                f"{self.base_url}. Verify Ollama is running."
            )
        except httpx.TimeoutException:
            raise RuntimeError(f"Local AI timeout: Ollama exceeded processing timeout of {self.timeout}s.")
        except Exception as ex:
            raise RuntimeError(f"Local AI failure: {str(ex)}")

ollama_client = OllamaClient()