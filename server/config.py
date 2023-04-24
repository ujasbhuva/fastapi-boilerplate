import os
from typing import List, Union

from dotenv import load_dotenv
from pydantic import BaseSettings, validator

load_dotenv()


class Settings(BaseSettings):
    debug: bool = os.environ.get("DEBUG")
    FASTAPI_CONFIG: str = os.environ.get("FASTAPI_CONFIG")

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")

    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

    CLIENT_URL = os.getenv("CLIENT_URL")

    BACKEND_CORS_ORIGINS: List = []

    @validator("BACKEND_CORS_ORIGINS", pre=True, allow_reuse=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SENTRY_DSN: str = os.environ.get("SENTRY_DSN")


settings = Settings()
