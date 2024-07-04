from typing import Literal
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent/".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    ENVIRONMENT: Literal['local', 'dev', 'prod'] = 'local'
    EMAIL_MAILBOX: str = "inbox"
    REFRESH_INTERVAL_IN_MINUTES: int = 60
    LOG_FILE: str = "server.log"


config = Settings()
