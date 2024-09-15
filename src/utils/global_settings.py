import os
from pydantic_settings import BaseSettings, SettingsConfigDict

from base import return_app_dir

def return_env_file_dir():
    env_path =os.path.exists(f"{return_app_dir(__file__)}/.env")
    if not env_path:
        os.mkdir(env_path)

class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=return_env_file_dir()
    )
    app_name = "MeetUp Guru"



# class EventBriteSettings()