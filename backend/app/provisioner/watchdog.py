import time
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class EphemeralEnvironment(BaseModel):
    env_id: str
    owner_agent_id: str
    allocated_resources: List[str] = Field(default_factory=list) # paths, container_ids, ports
    created_at_epoch: float = Field(default_factory=time.time)
    expires_at_epoch: float
    is_torn_down: bool = False

class EnvironmentWatchdog:
    def __init__(self, default_ttl_seconds: int = 60):
        self.default_ttl = default_ttl_seconds
        self.environments: Dict[str, EphemeralEnvironment] = {}
        self.reaped_resources: List[str] = []

    def register_environment(self, env_id: str, agent_id: str, resources: List[str], ttl_seconds: Optional[int] = None) -> EphemeralEnvironment:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        now = time.time()
        env = EphemeralEnvironment(
            env_id=env_id,
            owner_agent_id=agent_id,
            allocated_resources=resources,
            created_at_epoch=now,
            expires_at_epoch=now + ttl,
            is_torn_down=False
        )
        self.environments[env_id] = env
        return env

    def heartbeat(self, env_id: str) -> bool:
        env = self.environments.get(env_id)
        if not env or env.is_torn_down:
            return False
        env.expires_at_epoch = time.time() + self.default_ttl
        return True

    def teardown_environment(self, env_id: str) -> bool:
        env = self.environments.get(env_id)
        if not env or env.is_torn_down:
            return False

        # Reap all allocated resources
        for res in env.allocated_resources:
            self.reaped_resources.append(res)
        env.is_torn_down = True
        return True

    def sweep_expired_environments(self) -> int:
        now = time.time()
        swept_count = 0
        for env_id, env in list(self.environments.items()):
            if not env.is_torn_down and now > env.expires_at_epoch:
                self.teardown_environment(env_id)
                swept_count += 1
        return swept_count

    def get_active_count(self) -> int:
        return sum(1 for e in self.environments.values() if not e.is_torn_down)
