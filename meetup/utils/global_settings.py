import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from meetup.utils.base import return_app_dir


def return_env_file_location():
    env_path = os.path.exists(f"{return_app_dir(__file__)}/.env")
    if not env_path:
        os.mkdir(env_path)
    return os.path.join(return_app_dir(__file__), ".env")


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=return_env_file_location(), env_file_encoding="utf-8", extra="allow"
    )


class EventBriteSettings(BaseAppSettings):
    eventbrite_private_key: str = Field(init=False)


class RedisSettings(BaseAppSettings):
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0)
    redis_password: Optional[str] = None
