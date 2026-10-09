from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class LLMResponse(BaseModel):
    content: Optional[str] = None
    model: str = "offline"

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: List[Dict[str, Any]], **kwargs: Any) -> LLMResponse:
        pass
