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


@router.get(
    "/pluginlist",
    response_model=List[str],
    summary="List available plugins (external)",
    description="Return the names of all registered plugin types.  "
    "This is the externally accessible variant of ``/open/pluginlist``.",
)
async def plugin_list() -> List[str]:
    return plugin_configuration.get_plugin_list()


@router.get(
    "/generalinfolist",
    response_model=PluginGeneralInfoList,
    summary="General info for all plugins (external)",
    description="Return a ``PluginGeneralInfoList`` containing general metadata "
    "for every registered plugin.  "
    "Externally accessible variant of ``/open/generalinfolist``.",
)
async def plugin_general_info_list() -> PluginGeneralInfoList:
    return plugin_configuration.get_plugin_general_info_list()


@router.post(
    "/generalinfo",
    response_model=PluginGeneralInfo,
    summary="General info for a single plugin (external)",
    description="Return general metadata (version, help URL, JavaScript settings, …) "
    "for the requested plugin type.  "
    "Externally accessible variant of ``/open/generalinfo``.",
)
async def plugin_general_info(plugintyp: str = Body(..., media_type="text/plain")) -> PluginGeneralInfo:
    info = plugin_configuration.get_plugin_general_info()
    if info is None:
        raise HTTPException(status_code=404, detail="No plugin registered")
    return info


@router.post(
    "/reloadplugindto",
    response_model=PluginDto,
    summary="Reload plugin DTO (external)",
    description="Reload and return a ``PluginDto`` for the given request.  "
    "Externally accessible variant of ``/open/reloadplugindto``.",
)
async def reload_plugin_dto(r: LoadPluginRequestDto) -> PluginDto:
    plugin = plugin_configuration.create_plugin(r.name or "", r.config or "")
    return plugin.reload_plugin_dto(r.params or "", r.q, r.nr)
