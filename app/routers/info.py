"""Info endpoints (/ping, /info, /plugindemo/open/ping, /plugindemo/open/info)."""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.models.dto import ServiceInfoDTO
from app.services.plugin_configuration import plugin_configuration

router = APIRouter()


@router.get("/open/ping", response_class=PlainTextResponse)
async def ping() -> str:
    return "pong"


@router.get("/plugindemo/open/ping", response_class=PlainTextResponse)
async def ping_open() -> str:
    return "pong"


@router.get("/open/info", response_model=ServiceInfoDTO)
async def info() -> ServiceInfoDTO:
    return plugin_configuration.get_service_info_dto()


@router.get("/plugindemo/open/info", response_model=ServiceInfoDTO)
async def info_open() -> ServiceInfoDTO:
    return plugin_configuration.get_service_info_dto()
