"""Abstract base implementation of PluginService with default behaviours."""

from __future__ import annotations

import base64
import io
import math as _math
from abc import abstractmethod
from typing import List, Optional

from PIL import Image, ImageDraw, ImageFont

from app.models.dto import (
    CalcErgebnisDto,
    CalcParamsDto,
    ImageBase64Dto,
    ImageInfoDto,
    ImageUrlDto,
    JavascriptLibrary,
    PluginAnswerDto,
    PluginConfigDto,
    PluginConfigurationInfoDto,
    PluginDatasetListDto,
    PluginDto,
    PluginGeneralInfo,
    PluginImageResultDto,
    PluginQuestionDto,
    PluginRenderDto,
    PluginScoreInfoDto,
    ToleranzDto,
    VarHashDto,
)
from app.models.enums import CALCERGEBNISTYPE, InputElement, Score
from app.services.plugin_service import PluginService


_DEFAULT_CONFIGURATION_MODE = 1  # CONFIGMODE_JSF


class BasePlugin(PluginService):
    """Base class with default implementations for all plugin methods."""

    def __init__(self, name: str, params: str) -> None:
        self.name: str = name
        self.config: str = params
        self.typ: str = ""
        self.version: str = "1.0"
        self.wiki_help: str = "Plugins"
        self.help_url: str = ""
        self.default_plugin_config: bool = False
        self.width: int = 400
        self.height: int = 400
        self.image_width_prozent: int = 100
        self.math: bool = False
        self.helpfiles: List[str] = ["plugins/plugin.html"]
        self.javascript_libs: List[str] = ["plugins/plugintools.js"]
        self.init_plugin_js: str = ""
        self.java_script: bool = False
        self.cacheable: bool = True
        self.use_question: bool = True
        self.use_vars: bool = True
        self.use_cvars: bool = True
        self.use_maxima_vars: bool = True
        self.use_mvars: bool = True
        self.configuration_mode: int = _DEFAULT_CONFIGURATION_MODE
        self.add_data_set: bool = True
        self.extern_url: bool = False
        self.calc_maxima: bool = True
        self.config_plugin_js: str = "configPlugin"
        self.plugin_service_url: str = ""

    # ------------------------------------------------------------------
    # PluginService interface – informational getters
    # ------------------------------------------------------------------

    def get_wiki_help(self) -> str:
        return self.wiki_help

    def get_help_url(self) -> str:
        return self.help_url

    def get_help(self) -> str:
        return "<h1>Plugin-Template</h1>Help is not configured yet!"

    def get_plugin_type(self) -> str:
        return type(self).__name__

    def get_plugin_version(self) -> str:
        return self.version

    def get_name(self) -> str:
        return self.name

    def is_default_plugin_config(self) -> bool:
        return self.default_plugin_config

    def is_math(self) -> bool:
        return self.math

    def get_config(self) -> Optional[str]:
        return self.config

    def get_tag(self) -> str:
        return f'[PI {self.name} {self.typ} "{self.config}"]'

    def get_image_width_prozent(self) -> int:
        return self.image_width_prozent

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_input_element(self) -> InputElement:
        return InputElement.TextField

    def javascript_libraries(self) -> List[JavascriptLibrary]:
        return [JavascriptLibrary(library=lib) for lib in self.javascript_libs]

    def javascript_libraries_local(self) -> List[JavascriptLibrary]:
        return []

    def get_plugin_general_info(self) -> PluginGeneralInfo:
        return PluginGeneralInfo(
            typ=self.typ,
            version=self.version,
            wikiHelp=self.wiki_help,
            helpUrl=self.help_url,
            help=self.get_help(),
            defaultPluginConfig=self.default_plugin_config,
            math=self.math,
            pluginType=self.get_plugin_type(),
            initPluginJS=self.init_plugin_js,
            javaScript=self.java_script,
            javascriptLibraries=self.javascript_libraries(),
            javascriptLibrariesLocal=self.javascript_libraries_local(),
            inputElement=self.get_input_element().value,
            cacheable=self.cacheable,
            useVars=self.use_vars,
            useCVars=self.use_cvars,
            useVarsMaxima=self.use_maxima_vars,
            useMVars=self.use_mvars,
            pluginServiceURL=self.plugin_service_url,
        )

    # ------------------------------------------------------------------
    # Default plugin operations (may be overridden)
    # ------------------------------------------------------------------

    def get_angabe(self, params: str, q: Optional[PluginQuestionDto]) -> str:
        return ""

    def generate_datasets(self, params: str, q: Optional[PluginQuestionDto]) -> PluginDatasetListDto:
        return PluginDatasetListDto()

    def get_vars(self) -> Optional[List[str]]:
        return None

    def get_html(self, params: str, q: Optional[PluginQuestionDto]) -> str:
        return ""

    def get_maxima(self, params: str, q: Optional[PluginQuestionDto]) -> str:
        return ""

    def get_image_dto(self, params: str, q: Optional[PluginQuestionDto]) -> ImageBase64Dto:
        result_dto = PluginImageResultDto()
        self.parse_draw_params(params, q, result_dto)
        img = Image.new("RGB", (self.width, self.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        self.paint(draw, result_dto)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        info = ImageInfoDto(
            pluginTyp=self.typ,
            width=self.width,
            height=self.height,
        )
        return ImageBase64Dto(base64Image=encoded, imageInfoDto=info)

    def get_image_url(self, params: str, q: Optional[PluginQuestionDto]) -> ImageUrlDto:
        return ImageUrlDto(error="Not implemented")

    def get_image_templates(self) -> List[List[str]]:
        return []

    @abstractmethod
    def parse_draw_params(self, params: str, q: Optional[PluginQuestionDto], result: PluginImageResultDto) -> None:
        ...

    @abstractmethod
    def paint(self, draw: ImageDraw.Draw, result: PluginImageResultDto) -> None:
        ...

    def parser_plugin(self, vars: Optional[VarHashDto], cp: Optional[CalcParamsDto], *p: CalcErgebnisDto) -> Optional[CalcErgebnisDto]:
        return None

    def parser_plugin_einheit(self, *p: str) -> Optional[str]:
        return None

    def load_plugin_dto(self, params: str, q: Optional[PluginQuestionDto], nr: int) -> PluginDto:
        image_dto = self.get_image_dto(params, q)
        return PluginDto(
            imageUrl=image_dto.base64Image,
            tagName=self.name,
            width=self.width,
            height=self.height,
        )

    def reload_plugin_dto(self, params: str, q: Optional[PluginQuestionDto], nr: int) -> PluginDto:
        return self.load_plugin_dto(params, q, nr)

    def render_latex(self, plugin_dto: Optional[PluginDto], answer: Optional[str], mode: Optional[str]) -> PluginRenderDto:
        return PluginRenderDto(source="")

    def render_plugin_result(
        self,
        plugin_dto: Optional[PluginDto],
        antwort: Optional[str],
        toleranz: Optional[ToleranzDto],
        vars_question: Optional[VarHashDto],
        answer_dto: Optional[PluginAnswerDto],
        grade: float,
        tex: bool,
    ) -> PluginRenderDto:
        return PluginRenderDto(source="")

    def score(
        self,
        plugin_dto: Optional[PluginDto],
        antwort: Optional[str],
        toleranz: Optional[ToleranzDto],
        vars_question: Optional[VarHashDto],
        plugin_answer_dto: Optional[PluginAnswerDto],
        grade: float,
    ) -> PluginScoreInfoDto:
        return PluginScoreInfoDto(
            schuelerErgebnis=CalcErgebnisDto(string=antwort, type=CALCERGEBNISTYPE.STRING),
            status=Score.NotScored,
            punkteSoll=grade,
        )

    def modify_angabe(self, text: Optional[str], q: Optional[PluginQuestionDto]) -> str:
        return text or ""

    def modify_angabe_textkomplett(self, text: Optional[str], q: Optional[PluginQuestionDto]) -> str:
        return text or ""

    def update_pluginstring_javascript(self, plugin_def: Optional[str], js_result: Optional[str]) -> str:
        return plugin_def or ""

def configuration_info(self, configuration_id: Optional[str]) -> PluginConfigurationInfoDto:
    return PluginConfigurationInfoDto(
        configurationID=configuration_id,
        javaScriptMethode=self.config_plugin_js,  # ← Add this (default is "configPlugin")
        configurationMode=self.configuration_mode,
        useQuestion=self.use_question,
        useVars=self.use_vars,
        useCVars=self.use_cvars,
        useMaximaVars=self.use_maxima_vars,
        useMVars=self.use_mvars,
        addDataSet=self.add_data_set,
        calcMaxima=self.calc_maxima,
        externUrl=self.extern_url,
    )

    def set_configuration_data(self, configuration: Optional[str], question_dto: Optional[PluginQuestionDto]) -> PluginConfigDto:
        return PluginConfigDto(typ=self.typ, name=self.name, config=configuration or self.config)

    def get_configuration(self) -> str:
        return self.config or ""
