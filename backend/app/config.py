from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field

class Settings(BaseSettings):
    model_config = ConfigDict(extra="allow", env_file=".env")

    PROJECT_NAME: str = "ForgeLab Runtime"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    DEFAULT_STORAGE_ROOT: str = "/tmp/forgelab_data"
    WATCHDOG_MAX_TTL_SECONDS: int = 300  # Auto-teardown after 5 minutes if unreleased
    DEFAULT_LLM_PROVIDER: str = "offline"

settings = Settings()
