from app.proxy.recorder import HTTPCassetteRecorder
from app.proxy.replay_engine import HTTPReplayEngine

def test_http_recording_and_replay_with_fault_injection():
    recorder = HTTPCassetteRecorder()
    sig = recorder.record(
        method="GET",
        url="https://api.stripe.com/v1/customers",
        status_code=200,
        response_body='{"data": [{"id": "cus_123"}]}',
        headers={"authorization": "Bearer sec_live_12345"}
    )
    assert sig is not None
    # Authorization header must be sanitized
    assert recorder.interactions[sig].request_headers["authorization"] == "[REDACTED_BY_FORGELAB]"

    # Replay engine test
    engine = HTTPReplayEngine(recorder)
    status, body = engine.replay_request("GET", "https://api.stripe.com/v1/customers")
    assert status == 200
    assert "cus_123" in body

    # Fault injection test: simulate 500 error
    engine.set_fault_injection(fault_mode="500_error")
    status_err, _ = engine.replay_request("GET", "https://api.stripe.com/v1/customers")
    assert status_err == 500
