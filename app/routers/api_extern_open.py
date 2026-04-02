"""External open API controller – endpoints under /plugindemo/api/open."""

from typing import List

from fastapi import APIRouter, Body, HTTPException

from app.models.dto import (
    LoadPluginRequestDto,
    PluginDto,
    PluginGeneralInfo,
    PluginGeneralInfoList,
)
from app.services.plugin_configuration import plugin_configuration

router = APIRouter(prefix="/plugindemo/api/open", tags=["External Open API"])


@router.get("/pluginlist", response_model=List[str])
async def plugin_list() -> List[str]:
    return plugin_configuration.get_plugin_list()


@router.get("/generalinfolist", response_model=PluginGeneralInfoList)
async def plugin_general_info_list() -> PluginGeneralInfoList:
    return plugin_configuration.get_plugin_general_info_list()


@router.post("/generalinfo", response_model=PluginGeneralInfo)
async def plugin_general_info(plugintyp: str = Body(..., media_type="text/plain")) -> PluginGeneralInfo:
    info = plugin_configuration.get_plugin_general_info(plugintyp)
    if info is None:
        raise HTTPException(status_code=404, detail=f"Plugin type '{plugintyp}' not found")
    return info


@router.post("/reloadplugindto", response_model=PluginDto)
async def reload_plugin_dto(r: LoadPluginRequestDto) -> PluginDto:
    plugin = plugin_configuration.create_plugin_service(r.typ or "", r.name or "", r.config or "")
    if plugin is None:
        raise HTTPException(status_code=404, detail=f"Plugin type '{r.typ}' not found")
    return plugin.reload_plugin_dto(r.params or "", r.q, r.nr)
