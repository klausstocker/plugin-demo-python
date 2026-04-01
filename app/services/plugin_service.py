"""Plugin service interface (abstract base class)."""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.dto import (
    CalcErgebnisDto,
    CalcParamsDto,
    ImageBase64Dto,
    ImageUrlDto,
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
from app.models.enums import InputElement


class PluginService(ABC):
    """Abstract interface that every plugin must implement."""

    @abstractmethod
    def get_wiki_help(self) -> str:
        ...

    @abstractmethod
    def get_help_url(self) -> str:
        ...

    @abstractmethod
    def get_help(self) -> str:
        ...

    @abstractmethod
    def get_plugin_type(self) -> str:
        ...

    @abstractmethod
    def get_plugin_version(self) -> str:
        ...

    @abstractmethod
    def get_name(self) -> str:
        ...

    @abstractmethod
    def is_default_plugin_config(self) -> bool:
        ...

    @abstractmethod
    def is_math(self) -> bool:
        ...

    @abstractmethod
    def get_config(self) -> Optional[str]:
        ...

    @abstractmethod
    def get_tag(self) -> str:
        ...

    @abstractmethod
    def get_image_width_prozent(self) -> int:
        ...

    @abstractmethod
    def get_width(self) -> int:
        ...

    @abstractmethod
    def get_height(self) -> int:
        ...

    @abstractmethod
    def get_angabe(self, params: str, q: Optional[PluginQuestionDto]) -> str:
        ...

    @abstractmethod
    def generate_datasets(self, params: str, q: Optional[PluginQuestionDto]) -> PluginDatasetListDto:
        ...

    @abstractmethod
    def get_vars(self) -> Optional[List[str]]:
        ...

    @abstractmethod
    def get_html(self, params: str, q: Optional[PluginQuestionDto]) -> str:
        ...

    @abstractmethod
    def get_maxima(self, params: str, q: Optional[PluginQuestionDto]) -> str:
        ...

    @abstractmethod
    def get_image_dto(self, params: str, q: Optional[PluginQuestionDto]) -> ImageBase64Dto:
        ...

    @abstractmethod
    def get_image_url(self, params: str, q: Optional[PluginQuestionDto]) -> ImageUrlDto:
        ...

    @abstractmethod
    def get_image_templates(self) -> List[List[str]]:
        ...

    @abstractmethod
    def parse_draw_params(self, params: str, q: Optional[PluginQuestionDto], result: PluginImageResultDto) -> None:
        ...

    @abstractmethod
    def parser_plugin(self, vars: Optional[VarHashDto], cp: Optional[CalcParamsDto], *p: CalcErgebnisDto) -> Optional[CalcErgebnisDto]:
        ...

    @abstractmethod
    def parser_plugin_einheit(self, *p: str) -> Optional[str]:
        ...

    @abstractmethod
    def load_plugin_dto(self, params: str, q: Optional[PluginQuestionDto], nr: int) -> PluginDto:
        ...

    @abstractmethod
    def reload_plugin_dto(self, params: str, q: Optional[PluginQuestionDto], nr: int) -> PluginDto:
        ...

    @abstractmethod
    def render_latex(self, plugin_dto: Optional[PluginDto], answer: Optional[str], mode: Optional[str]) -> PluginRenderDto:
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def score(
        self,
        plugin_dto: Optional[PluginDto],
        antwort: Optional[str],
        toleranz: Optional[ToleranzDto],
        vars_question: Optional[VarHashDto],
        plugin_answer_dto: Optional[PluginAnswerDto],
        grade: float,
    ) -> PluginScoreInfoDto:
        ...

    @abstractmethod
    def modify_angabe(self, text: Optional[str], q: Optional[PluginQuestionDto]) -> str:
        ...

    @abstractmethod
    def modify_angabe_textkomplett(self, text: Optional[str], q: Optional[PluginQuestionDto]) -> str:
        ...

    @abstractmethod
    def update_pluginstring_javascript(self, plugin_def: Optional[str], js_result: Optional[str]) -> str:
        ...

    @abstractmethod
    def configuration_info(self, configuration_id: Optional[str]) -> PluginConfigurationInfoDto:
        ...

    @abstractmethod
    def set_configuration_data(self, configuration: Optional[str], question_dto: Optional[PluginQuestionDto]) -> PluginConfigDto:
        ...

    @abstractmethod
    def get_configuration(self) -> str:
        ...

    @abstractmethod
    def get_plugin_general_info(self) -> PluginGeneralInfo:
        ...

    @abstractmethod
    def get_input_element(self) -> InputElement:
        ...
