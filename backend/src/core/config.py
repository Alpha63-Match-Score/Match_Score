from functools import lru_cache
import os
from pathlib import Path
from typing import List, Union

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

cwd = os.getcwd()
possible_env_paths = [
    Path(cwd) / ".env",
    Path(cwd).parent / ".env",
    Path(__file__).parent.parent.parent / ".env",
]


for env_path in possible_env_paths:
    if env_path.exists():
        env_file = env_path
        load_dotenv(env_path)
        break


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "App"

    CORS_ALLOWED_HOSTS: list[str] = ["*"]

    @field_validator("CORS_ALLOWED_HOSTS", check_fields=False)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION: int
    BLACKLISTED_TOKENS: list[str] = []

    DATABASE_URL: str
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SECRET_KEY: str

    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_BUCKET_NAME: str
    AWS_REGION: str

    model_config = {
        "case_sensitive": True,
        "env_file": str(env_file),
        "env_file_encoding": "utf-8",
        "extra": "allow",
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
