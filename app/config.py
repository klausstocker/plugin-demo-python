"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "plugindemo"
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "info"
    swagger_ui_path: str = "/plugindemo/swagger-ui"
    openapi_url: str = "/plugindemo/v3/api-docs"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
