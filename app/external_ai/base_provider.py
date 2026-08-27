from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseExternalProvider(ABC):
    @abstractmethod
    async def is_available(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        pass