"""Application configuration loaded from environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "plugindemo"
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "info"
    swagger_ui_path: str = "/plugindemo/swagger-ui"
    openapi_url: str = "/plugindemo/v3/api-docs"

    # Setup-service registration
    letto_setup_uri: str = ""
    service_user_username: str = "user"
    service_user_password: str = ""
    network_letto_address: str = "letto-plugindemo"
    docker_container_name: str = "letto-plugindemo"
    letto_plugin_uri_intern: str = ""
    letto_plugin_uri_extern: str = ""

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
