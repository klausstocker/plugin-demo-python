"""Info endpoints (/ping, /info, /plugindemo/open/ping, /plugindemo/open/info)."""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.models.dto import ServiceInfoDTO
from app.services.plugin_configuration import plugin_configuration

router = APIRouter(tags=["Info"])


@router.get(
    "/open/ping",
    response_class=PlainTextResponse,
    summary="Ping (internal)",
    description="Simple health-check endpoint that returns ``pong``.  "
    "Located under the internal ``/open`` prefix.",
)
async def ping() -> str:
    return "pong"


@router.get(
    "/version",
    response_class=PlainTextResponse,
    summary="Service version",
    description="Return the current version string of the plugin service.",
)
async def version() -> str:
    return plugin_configuration.VERSION


@router.get(
    "/info",
    response_model=ServiceInfoDTO,
    summary="Service information",
    description="Return detailed service metadata including name, version, "
    "author, license and runtime information.",
)
async def info() -> ServiceInfoDTO:
    return plugin_configuration.get_service_info_dto()


@router.get(
    "/plugindemo/open/ping",
    response_class=PlainTextResponse,
    summary="Ping (external)",
    description="Simple health-check endpoint that returns ``pong``.  "
    "Located under the external ``/plugindemo/open`` prefix.",
)
async def ping_open() -> str:
    return "pong"


@router.get(
    "/plugindemo/open/info",
    response_model=ServiceInfoDTO,
    summary="Service information (external)",
    description="Return detailed service metadata.  "
    "Same payload as ``/info`` but available under the external prefix.",
)
async def info_open() -> ServiceInfoDTO:
    return plugin_configuration.get_service_info_dto()
