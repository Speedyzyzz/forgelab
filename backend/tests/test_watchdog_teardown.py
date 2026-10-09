import time
from app.provisioner.watchdog import EnvironmentWatchdog

def test_watchdog_leak_proof_teardown():
    watchdog = EnvironmentWatchdog(default_ttl_seconds=1)
    env = watchdog.register_environment(
        env_id="env_ephemeral_01",
        agent_id="agent_runner_1",
        resources=["/tmp/forgelab_data/clones/c1.db", "port_8080"],
        ttl_seconds=1
    )
    assert watchdog.get_active_count() == 1

    # Simulate agent crash without calling teardown
    time.sleep(1.1)

    # Watchdog sweeps expired environments
    swept = watchdog.sweep_expired_environments()
    assert swept == 1
    assert watchdog.get_active_count() == 0
    assert "/tmp/forgelab_data/clones/c1.db" in watchdog.reaped_resources
