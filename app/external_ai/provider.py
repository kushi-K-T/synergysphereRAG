import httpx
from typing import Dict, Any, Optional
from app.config.settings import settings
from app.external_ai.base_provider import BaseExternalProvider

class OpenAICompatibleProvider(BaseExternalProvider):
    def __init__(self):
        self.enabled = settings.EXTERNAL_AI_ENABLED
        self.api_key = settings.EXTERNAL_AI_API_KEY
        self.model = settings.EXTERNAL_AI_MODEL
        self.base_url = settings.EXTERNAL_AI_BASE_URL.rstrip('/')
        self.timeout = settings.EXTERNAL_AI_TIMEOUT

    async def is_available(self) -> Dict[str, Any]:
        if not self.enabled:
            return {"status": "disabled", "reason": "EXTERNAL_AI_ENABLED is false"}
        if not self.api_key:
            return {"status": "misconfigured", "reason": "EXTERNAL_AI_API_KEY is missing"}
        return {"status": "configured", "provider": settings.EXTERNAL_AI_PROVIDER, "model": self.model}

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        if not self.enabled:
            raise RuntimeError("External AI provider is disabled in settings (EXTERNAL_AI_ENABLED=false).")
        if not self.api_key:
            raise RuntimeError("External AI API key is not configured.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    return {
                        "text": content.strip(),
                        "model": self.model,
                        "provider": settings.EXTERNAL_AI_PROVIDER
                    }
                raise RuntimeError(f"External AI returned HTTP status {res.status_code}: {res.text}")
        except httpx.ConnectError:
            raise RuntimeError(f"External AI unavailable: Connection to {self.base_url} failed.")
        except httpx.TimeoutException:
            raise RuntimeError(f"External AI timeout: Request exceeded {self.timeout}s.")
        except Exception as ex:
            raise RuntimeError(f"External AI failure: {str(ex)}")

external_provider = OpenAICompatibleProvider()