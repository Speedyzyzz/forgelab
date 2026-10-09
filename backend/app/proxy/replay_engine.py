import time
from typing import Optional, Tuple
from app.proxy.recorder import HTTPCassetteRecorder, HTTPInteraction

class HTTPReplayEngine:
    def __init__(self, recorder: HTTPCassetteRecorder):
        self.recorder = recorder
        self.fault_mode: Optional[str] = None # "timeout", "500_error", "latency"
        self.injected_latency_ms: int = 0

    def set_fault_injection(self, fault_mode: Optional[str] = None, latency_ms: int = 0) -> None:
        self.fault_mode = fault_mode
        self.injected_latency_ms = latency_ms

    def replay_request(self, method: str, url: str, body: Optional[str] = None) -> Tuple[int, str]:
        if self.injected_latency_ms > 0:
            time.sleep(self.injected_latency_ms / 1000.0)

        if self.fault_mode == "500_error":
            return 500, '{"error": "Injected Internal Server Error"}'
        elif self.fault_mode == "timeout":
            return 504, '{"error": "Injected Gateway Timeout"}'

        sig = self.recorder._request_signature(method, url, body)
        interaction = self.recorder.interactions.get(sig)
        if interaction:
            return interaction.status_code, interaction.response_body

        return 404, '{"error": "Cassette recording not found"}'
