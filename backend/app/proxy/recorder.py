import json
import hashlib
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class HTTPInteraction(BaseModel):
    method: str
    url: str
    request_headers: Dict[str, str] = Field(default_factory=dict)
    request_body: Optional[str] = None
    status_code: int = 200
    response_body: str = ""
    response_headers: Dict[str, str] = Field(default_factory=dict)

class HTTPCassetteRecorder:
    def __init__(self):
        self.interactions: Dict[str, HTTPInteraction] = {}

    def _request_signature(self, method: str, url: str, body: Optional[str] = None) -> str:
        raw = f"{method.upper()}:{url}:{body or ''}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def record(self, method: str, url: str, status_code: int, response_body: str, headers: Optional[Dict[str, str]] = None, body: Optional[str] = None) -> str:
        # Sanitize authorization headers
        sanitized_headers = dict(headers or {})
        for h in ["authorization", "x-api-key", "cookie"]:
            if h in sanitized_headers:
                sanitized_headers[h] = "[REDACTED_BY_FORGELAB]"

        sig = self._request_signature(method, url, body)
        self.interactions[sig] = HTTPInteraction(
            method=method.upper(),
            url=url,
            request_headers=sanitized_headers,
            request_body=body,
            status_code=status_code,
            response_body=response_body,
            response_headers={"content-type": "application/json"}
        )
        return sig
