import os
from typing import List, Union

from dotenv import load_dotenv
from pydantic import BaseSettings, validator

load_dotenv()


class Settings(BaseSettings):
    debug: bool = os.environ.get("DEBUG")
    FASTAPI_CONFIG: str = os.environ.get("FASTAPI_CONFIG")

    # FB_TYPE: str = os.environ.get("FB_TYPE")
    # FB_PROJECT_ID: str = os.environ.get("FB_PROJECT_ID")
    # FB_PRIVATE_KEY_ID: str = os.environ.get("FB_PRIVATE_KEY_ID")
    # FB_PRIVATE_KEY: str = os.environ.get("FB_PRIVATE_KEY")
    # FB_CLIENT_EMAIL: str = os.environ.get("FB_CLIENT_EMAIL")
    # FB_CLIENT_ID: str = os.environ.get("FB_CLIENT_ID")
    # FB_AUTH_URL: str = os.environ.get("FB_AUTH_URL")
    # FB_TOKEN_URL: str = os.environ.get("FB_TOKEN_URL")
    # FB_AUTH_PROVIDER_URL: str = os.environ.get("FB_AUTH_PROVIDER_URL")
    # FB_CLIENT_URL: str = os.environ.get("FB_CLIENT_URL")

    # POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    # POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    # POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER")
    # POSTGRES_DB: str = os.environ.get("POSTGRES_DB")

    AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    # OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    # IMAGE_ENHANCER_URL = os.environ.get("IMAGE_ENHANCER_URL")
    # IMAGE_ENHANCER_API_KEY = os.environ.get("IMAGE_ENHANCER_API_KEY")
    # OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
    # TYPESENSE_ADMIN_API_KEY: str = os.environ.get("TYPESENSE_ADMIN_API_KEY")

    # CHARGEBEE_SITE_NAME = os.environ.get("CHARGEBEE_SITE_NAME")
    # CHARGEBEE_ACCESS_TOKEN = os.environ.get("CHARGEBEE_ACCESS_TOKEN")
    # CHARGEBEE_HOOK_USERNAME = os.environ.get("CHARGEBEE_HOOK_USERNAME")
    # CHARGEBEE_HOOK_PASSWORD = os.environ.get("CHARGEBEE_HOOK_PASSWORD")
    BACKEND_CORS_ORIGINS: List = []

    @validator("BACKEND_CORS_ORIGINS", pre=True, allow_reuse=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # def assemble_db_connection(self):
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=self.POSTGRES_USER,
    #         password=self.POSTGRES_PASSWORD,
    #         host=self.POSTGRES_SERVER,
    #         path=f"/{self.POSTGRES_DB or ''}",
    #     )

    SENTRY_DSN: str = os.environ.get("SENTRY_DSN")


settings = Settings()
