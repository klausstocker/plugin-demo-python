"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.config import settings
from app.routers import api, api_extern_open, info
from app.services.plugin_configuration import plugin_configuration
from app.services.plugins.plugin_uhr import PluginUhr


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    plugin_configuration.init()
    plugin_configuration.register_plugin("Uhr1", PluginUhr)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1",
    docs_url=settings.swagger_ui_path,
    openapi_url=settings.openapi_url,
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Include routers
# ---------------------------------------------------------------------------

app.include_router(info.router)
app.include_router(api.router)
app.include_router(api_extern_open.router)
