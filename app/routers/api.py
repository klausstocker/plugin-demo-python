"""Main API controller – all endpoints under /open (LOCAL_API)."""

from typing import List

from fastapi import APIRouter, Body, HTTPException

from app.models.dto import (
    ImageBase64Dto,
    LoadPluginRequestDto,
    PluginAngabeRequestDto,
    PluginConfigDto,
    PluginConfigurationInfoDto,
    PluginConfigurationInfoRequestDto,
    PluginConfigurationRequestDto,
    PluginDatasetListDto,
    PluginDto,
    PluginEinheitRequestDto,
    PluginGeneralInfo,
    PluginGeneralInfoList,
    PluginParserRequestDto,
    PluginRenderDto,
    PluginRenderLatexRequestDto,
    PluginRenderResultRequestDto,
    PluginRequestDto,
    PluginScoreInfoDto,
    PluginScoreRequestDto,
    PluginSetConfigurationDataRequestDto,
    PluginUpdateJavascriptRequestDto,
    CalcErgebnisDto,
)
from app.services.plugin_configuration import plugin_configuration

router = APIRouter(prefix="/open", tags=["API"])


def _create_plugin(name: str, config: str):
    return plugin_configuration.create_plugin(name or "", config or "")


@router.get("/pluginlist", response_model=List[str])
async def plugin_list() -> List[str]:
    return plugin_configuration.get_plugin_list()


@router.get("/generalinfolist", response_model=PluginGeneralInfoList)
async def plugin_general_info_list() -> PluginGeneralInfoList:
    return plugin_configuration.get_plugin_general_info_list()


@router.post("/generalinfo", response_model=PluginGeneralInfo)
async def plugin_general_info(plugintyp: str = Body(..., media_type="text/plain")) -> PluginGeneralInfo:
    return plugin_configuration.get_plugin_general_info()


@router.post("/gethtml", response_model=str)
async def get_html(r: PluginRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_html(r.params or "", r.q)


@router.post("/angabe", response_model=str)
async def get_angabe(r: PluginRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_angabe(r.params or "", r.q)


@router.post("/generatedatasets", response_model=PluginDatasetListDto)
async def generate_datasets(r: PluginRequestDto) -> PluginDatasetListDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.generate_datasets(r.params or "", r.q)


@router.post("/maxima", response_model=str)
async def get_maxima(r: PluginRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_maxima(r.params or "", r.q)


@router.post("/image", response_model=ImageBase64Dto)
async def get_image(r: PluginRequestDto) -> ImageBase64Dto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_image_dto(r.params or "", r.q)


@router.post("/imagetemplates", response_model=List[List[str]])
async def get_image_templates(r: PluginRequestDto) -> List[List[str]]:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_image_templates()


@router.post("/parserplugin", response_model=CalcErgebnisDto)
async def parser_plugin(r: PluginParserRequestDto) -> CalcErgebnisDto:
    plugin = _create_plugin(r.name, r.config)
    result = plugin.parser_plugin(r.vars, r.cp, *r.p)
    return result or CalcErgebnisDto()


@router.post("/parserplugineinheit", response_model=str)
async def parser_plugin_einheit(r: PluginEinheitRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    result = plugin.parser_plugin_einheit(*r.p)
    return result or ""


@router.post("/score", response_model=PluginScoreInfoDto)
async def score(r: PluginScoreRequestDto) -> PluginScoreInfoDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.score(r.pluginDto, r.antwort, r.toleranz, r.varsQuestion, r.answerDto, r.grade)


@router.post("/getvars", response_model=List[str])
async def get_vars(r: PluginRequestDto) -> List[str]:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_vars() or []


@router.post("/modifyangabe", response_model=str)
async def modify_angabe(r: PluginAngabeRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.modify_angabe(r.text, r.q)


@router.post("/modifyangabetextkomplett", response_model=str)
async def modify_angabe_textkomplett(r: PluginAngabeRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.modify_angabe_textkomplett(r.text, r.q)


@router.post("/updatepluginstringjavascript", response_model=str)
async def update_pluginstring_javascript(r: PluginUpdateJavascriptRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.update_pluginstring_javascript(r.pluginDef, r.jsResult)


@router.post("/loadplugindto", response_model=PluginDto)
async def load_plugin_dto(r: LoadPluginRequestDto) -> PluginDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.load_plugin_dto(r.params or "", r.q, r.nr)


@router.post("/reloadplugindto", response_model=PluginDto)
async def reload_plugin_dto(r: LoadPluginRequestDto) -> PluginDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.reload_plugin_dto(r.params or "", r.q, r.nr)


@router.post("/renderlatex", response_model=PluginRenderDto)
async def render_latex(r: PluginRenderLatexRequestDto) -> PluginRenderDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.render_latex(r.pluginDto, r.answer, r.mode)


@router.post("/renderpluginresult", response_model=PluginRenderDto)
async def render_plugin_result(r: PluginRenderResultRequestDto) -> PluginRenderDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.render_plugin_result(
        r.pluginDto, r.antwort, r.toleranz, r.varsQuestion, r.answerDto, r.grade, r.tex
    )


@router.post("/configurationinfo", response_model=PluginConfigurationInfoDto)
async def configuration_info(r: PluginConfigurationInfoRequestDto) -> PluginConfigurationInfoDto:
    return plugin_configuration.configuration_info(
        r.name, r.config, r.configurationID or "", r.timeout
    )


@router.post("/setconfigurationdata", response_model=PluginConfigDto)
async def set_configuration_data(r: PluginSetConfigurationDataRequestDto) -> PluginConfigDto:
    result = plugin_configuration.set_configuration_data(
        r.configurationID or "", r.configuration or "", r.questionDto
    )
    if result is None:
        raise HTTPException(status_code=404, detail=f"Configuration '{r.configurationID}' not found")
    return result


@router.post("/getconfiguration", response_model=str)
async def get_configuration(r: PluginConfigurationRequestDto) -> str:
    result = plugin_configuration.get_configuration(r.configurationID or "")
    if result is None:
        raise HTTPException(status_code=404, detail=f"Configuration '{r.configurationID}' not found")
    return result
