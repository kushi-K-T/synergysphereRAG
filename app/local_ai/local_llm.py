from typing import Dict, Any, List, Optional
from app.local_ai.ollama_client import ollama_client

class LocalLLM:
    def __init__(self):
        self.client = ollama_client

    async def execute(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        raw_response = await self.client.generate_response(prompt=prompt, system_prompt=system_prompt)
        return {
            "text": raw_response.strip(),
            "model": self.client.model,
            "engine": "ollama"
        }

local_llm = LocalLLM()