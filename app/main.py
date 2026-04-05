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
    plugin_configuration.register_plugin("Uhr1", PluginUhr)
    plugin_configuration.register_plugin_in_setup()
    yield


tags_metadata = [
    {
        "name": "Info",
        "description": "Health-check and service information endpoints.",
    },
    {
        "name": "API",
        "description": "Internal plugin API – all endpoints under ``/open``.",
    },
    {
        "name": "External Open API",
        "description": "Externally accessible plugin API – endpoints under ``/plugindemo/api/open``.",
    },
]

app = FastAPI(
    title=settings.app_name,
    version=plugin_configuration.VERSION,
    description=(
        "REST API for the **LeTTo Plugin Demo** service.\n\n"
        "This service exposes plugin operations such as generating HTML, "
        "images, datasets, scoring student answers and managing plugin "
        "configurations.  The Swagger UI can be used to explore and try "
        "out every endpoint interactively."
    ),
    docs_url=settings.swagger_ui_path,
    openapi_url=settings.openapi_url,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Include routers
# ---------------------------------------------------------------------------

app.include_router(info.router)
app.include_router(api.router)
app.include_router(api_extern_open.router)
