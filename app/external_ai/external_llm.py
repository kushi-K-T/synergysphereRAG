from typing import Dict, Any, Optional
from app.external_ai.provider import external_provider

class ExternalLLM:
    def __init__(self):
        self.provider = external_provider

    async def execute(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        return await self.provider.generate(prompt=prompt, system_prompt=system_prompt)

external_llm = ExternalLLM()