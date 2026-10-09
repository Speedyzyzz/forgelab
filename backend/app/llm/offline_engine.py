from typing import Any, Dict, List
from app.llm.provider import LLMProvider, LLMResponse

class OfflineForgePatchLLM(LLMProvider):
    def __init__(self):
        self.model = "forgelab-offline-evaluator"

    async def generate(self, messages: List[Dict[str, Any]], **kwargs: Any) -> LLMResponse:
        return LLMResponse(
            content="Simulated agent patch candidate for test replica execution",
            model=self.model
        )
