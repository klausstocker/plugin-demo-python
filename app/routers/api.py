"""Main API controller – all endpoints under /open (LOCAL_API)."""

from typing import List

from fastapi import APIRouter, Body, HTTPException

from fastapi.responses import HTMLResponse

from app.models.dto import (
    ImageBase64Dto,
    ImageUrlDto,
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


@router.get(
    "/pluginlist",
    response_model=List[str],
    summary="List available plugins",
    description="Return the names of all registered plugin types.",
)
async def plugin_list() -> List[str]:
    return plugin_configuration.get_plugin_list()


@router.get(
    "/generalinfolist",
    response_model=PluginGeneralInfoList,
    summary="General info for all plugins",
    description="Return a ``PluginGeneralInfoList`` containing general metadata "
    "for every registered plugin.",
)
async def plugin_general_info_list() -> PluginGeneralInfoList:
    return plugin_configuration.get_plugin_general_info_list()


@router.post(
    "/generalinfo",
    response_model=PluginGeneralInfo,
    summary="General info for a single plugin",
    description="Return general metadata (version, help URL, JavaScript settings, …) "
    "for the requested plugin type.",
)
async def plugin_general_info(plugintyp: str = Body(..., media_type="text/plain")) -> PluginGeneralInfo:
    info = plugin_configuration.get_plugin_general_info()
    if info is None:
        raise HTTPException(status_code=404, detail="No plugin registered")
    return info


@router.post(
    "/gethtml",
    response_model=str,
    summary="Get plugin HTML",
    description="Generate the HTML representation of the plugin for the given "
    "parameters and question context.",
)
async def get_html(r: PluginRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_html(r.params or "", r.q)


@router.post(
    "/angabe",
    response_model=str,
    summary="Get plugin statement text (Angabe)",
    description="Return the textual statement (Angabe) the plugin produces for "
    "the given parameters and question.",
)
async def get_angabe(r: PluginRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_angabe(r.params or "", r.q)


@router.post(
    "/generatedatasets",
    response_model=PluginDatasetListDto,
    summary="Generate datasets",
    description="Generate a list of dataset definitions the plugin requires.",
)
async def generate_datasets(r: PluginRequestDto) -> PluginDatasetListDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.generate_datasets(r.params or "", r.q)


@router.post(
    "/maxima",
    response_model=str,
    summary="Get Maxima expression",
    description="Return the Maxima CAS expression produced by the plugin.",
)
async def get_maxima(r: PluginRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_maxima(r.params or "", r.q)


@router.post(
    "/image",
    response_model=ImageBase64Dto,
    summary="Get plugin image (Base64)",
    description="Return the plugin-generated image as a Base64-encoded string "
    "together with image metadata.",
)
async def get_image(r: PluginRequestDto) -> ImageBase64Dto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_image_dto(r.params or "", r.q)


@router.post(
    "/imageurl",
    response_model=ImageUrlDto,
    summary="Get plugin image URL",
    description="Return a URL pointing to the plugin-generated image together "
    "with image metadata.",
)
async def get_image_url(r: PluginRequestDto) -> ImageUrlDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_image_url(r.params or "", r.q)


@router.post(
    "/imagetemplates",
    response_model=List[List[str]],
    summary="Get image templates",
    description="Return the list of image templates supported by the plugin.",
)
async def get_image_templates(r: PluginRequestDto) -> List[List[str]]:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_image_templates()


@router.post(
    "/parserplugin",
    response_model=CalcErgebnisDto,
    summary="Parser plugin calculation",
    description="Execute the plugin's parser calculation with the supplied "
    "variables and calculation parameters, returning a ``CalcErgebnisDto``.",
)
async def parser_plugin(r: PluginParserRequestDto) -> CalcErgebnisDto:
    plugin = _create_plugin(r.name, r.config)
    result = plugin.parser_plugin(r.vars, r.cp, *r.p)
    return result or CalcErgebnisDto()


@router.post(
    "/parserplugineinheit",
    response_model=str,
    summary="Parser plugin unit (Einheit)",
    description="Return the unit string produced by the plugin's parser for "
    "the given parameters.",
)
async def parser_plugin_einheit(r: PluginEinheitRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    result = plugin.parser_plugin_einheit(*r.p)
    return result or ""


@router.post(
    "/score",
    response_model=PluginScoreInfoDto,
    summary="Score a student answer",
    description="Evaluate a student's answer against the expected result and "
    "return scoring information including achieved/maximum points and feedback.",
)
async def score(r: PluginScoreRequestDto) -> PluginScoreInfoDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.score(r.pluginDto, r.antwort, r.toleranz, r.varsQuestion, r.answerDto, r.grade)


@router.post(
    "/getvars",
    response_model=List[str],
    summary="Get plugin variables",
    description="Return the list of variable names used by the plugin.",
)
async def get_vars(r: PluginRequestDto) -> List[str]:
    plugin = _create_plugin(r.name, r.config)
    return plugin.get_vars() or []


@router.post(
    "/modifyangabe",
    response_model=str,
    summary="Modify statement text (Angabe)",
    description="Apply plugin-specific modifications to the given statement text.",
)
async def modify_angabe(r: PluginAngabeRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.modify_angabe(r.text, r.q)


@router.post(
    "/modifyangabetextkomplett",
    response_model=str,
    summary="Modify full statement text",
    description="Apply plugin-specific modifications to the complete statement text "
    "including all surrounding markup.",
)
async def modify_angabe_textkomplett(r: PluginAngabeRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.modify_angabe_textkomplett(r.text, r.q)


@router.post(
    "/updatepluginstringjavascript",
    response_model=str,
    summary="Update plugin string via JavaScript result",
    description="Update the plugin definition string by incorporating the result "
    "returned from the client-side JavaScript execution.",
)
async def update_pluginstring_javascript(r: PluginUpdateJavascriptRequestDto) -> str:
    plugin = _create_plugin(r.name, r.config)
    return plugin.update_pluginstring_javascript(r.pluginDef, r.jsResult)


@router.post(
    "/loadplugindto",
    response_model=PluginDto,
    summary="Load plugin DTO",
    description="Create and return a ``PluginDto`` for the given parameters, "
    "question context and dataset number.",
)
async def load_plugin_dto(r: LoadPluginRequestDto) -> PluginDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.load_plugin_dto(r.params or "", r.q, r.nr)


@router.post(
    "/reloadplugindto",
    response_model=PluginDto,
    summary="Reload plugin DTO",
    description="Reload and return a ``PluginDto`` – similar to ``loadplugindto`` "
    "but forces regeneration of the plugin state.",
)
async def reload_plugin_dto(r: LoadPluginRequestDto) -> PluginDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.reload_plugin_dto(r.params or "", r.q, r.nr)


@router.post(
    "/renderlatex",
    response_model=PluginRenderDto,
    summary="Render LaTeX",
    description="Render the plugin content as LaTeX source, optionally including "
    "referenced images.",
)
async def render_latex(r: PluginRenderLatexRequestDto) -> PluginRenderDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.render_latex(r.pluginDto, r.answer, r.mode)


@router.post(
    "/renderpluginresult",
    response_model=PluginRenderDto,
    summary="Render plugin result",
    description="Render the scored plugin result (student answer + evaluation) "
    "as HTML or LaTeX source.",
)
async def render_plugin_result(r: PluginRenderResultRequestDto) -> PluginRenderDto:
    plugin = _create_plugin(r.name, r.config)
    return plugin.render_plugin_result(
        r.pluginDto, r.antwort, r.toleranz, r.varsQuestion, r.answerDto, r.grade, r.tex
    )


@router.post(
    "/configurationinfo",
    response_model=PluginConfigurationInfoDto,
    summary="Get configuration info",
    description="Return configuration metadata for the plugin, including the URL "
    "for the configuration iframe and the configuration mode.",
)
async def configuration_info(r: PluginConfigurationInfoRequestDto) -> PluginConfigurationInfoDto:
    configuration_id = r.configurationID or ""
    typ = r.typ or ""
    result = plugin_configuration.configuration_info(
        typ, r.name or "", r.config or "", configuration_id, r.timeout
    )
    result.configurationUrl = (
        plugin_configuration.base_uri_extern
        + plugin_configuration.IFRAME_CONFIG
        + "?typ=" + typ
        + "&configurationID=" + configuration_id
    )
    return result


@router.post(
    "/setconfigurationdata",
    response_model=PluginConfigDto,
    summary="Set configuration data",
    description="Store or update the configuration for a specific configuration ID "
    "and return the resulting ``PluginConfigDto``.",
    responses={404: {"description": "Configuration ID not found."}},
)
async def set_configuration_data(r: PluginSetConfigurationDataRequestDto) -> PluginConfigDto:
    result = plugin_configuration.set_configuration_data(
        r.configurationID or "", r.configuration or "", r.questionDto
    )
    if result is None:
        raise HTTPException(status_code=404, detail=f"Configuration '{r.configurationID}' not found")
    return result


@router.post(
    "/getconfiguration",
    response_model=str,
    summary="Get configuration string",
    description="Retrieve the raw configuration string for the given configuration ID.",
    responses={404: {"description": "Configuration ID not found."}},
)
async def get_configuration(r: PluginConfigurationRequestDto) -> str:
    result = plugin_configuration.get_configuration(r.configurationID or "")
    if result is None:
        raise HTTPException(status_code=404, detail=f"Configuration '{r.configurationID}' not found")
    return result


@router.get(
    "/confighttp",
    response_class=HTMLResponse,
    summary="Configuration HTML page",
    description="Serve the HTML configuration page intended to be displayed "
    "inside an iframe for interactive plugin configuration.",
)
async def config_http() -> str:
    """Serve an HTML configuration page for the plugin (iframe target)."""
    return "<html><body><h1>Plugin Configuration</h1></body></html>"
