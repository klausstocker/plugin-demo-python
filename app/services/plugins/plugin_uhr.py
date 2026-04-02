"""PluginUhr – clock plugin demo (Python port of the Java PluginUhr)."""

from __future__ import annotations

import math
import re
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from app.models.dto import (
    CalcErgebnisDto,
    CalcParamsDto,
    PluginAnswerDto,
    PluginConfigDto,
    PluginConfigurationInfoDto,
    PluginDto,
    PluginImageResultDto,
    PluginQuestionDto,
    PluginScoreInfoDto,
    ToleranzDto,
    VarHashDto,
)
from app.models.enums import CALCERGEBNISTYPE, Score
from app.services.base_plugin import BasePlugin


def _parse_time(time_str: str) -> float:
    """Parse a time string (HH:MM or HH:MM:SS) into fractional hours."""
    parts = time_str.strip().split(":")
    if len(parts) < 2:
        raise ValueError(f"Cannot parse time: {time_str}")
    hours = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2]) if len(parts) > 2 else 0.0
    return hours + minutes / 60.0 + seconds / 3600.0


def _times_equal(a: float, b: float, toleranz: Optional[ToleranzDto]) -> bool:
    """Compare two time values within tolerance."""
    if toleranz is None:
        return abs(a - b) < 1e-9
    diff = abs(a - b)
    if toleranz.relativ():
        ref = max(abs(a), abs(b))
        return diff <= toleranz.toleranz * ref if ref > 0 else diff < 1e-9
    return diff <= toleranz.toleranz


class PluginUhr(BasePlugin):
    """Clock plugin demo."""

    def __init__(self, name: str, params: str) -> None:
        super().__init__(name, params)
        self.typ = "Uhr1"
        self.version = "1.0"
        self.helpfiles = ["plugins/uhr/Uhr.html"]
        self.javascript_libs = ["plugins/uhr/uhrScript.js", "plugins/uhr/uhrConfigScript.js"]
        self.java_script = True
        self.init_plugin_js = "initPluginUhr"
        self.config_plugin_js = "configPluginUhr"
        self.configuration_mode = 2  # CONFIGMODE_JAVASCRIPT
        self.wiki_help = "Plugins"
        self.help_url = ""
        self.width = 400
        self.height = 400
        self.image_width_prozent = 100
        self.math = False
        self.cacheable = True
        self.use_question = True
        self.use_vars = True
        self.use_cvars = True
        self.use_maxima_vars = True
        self.use_mvars = True
        self.add_data_set = True
        self.extern_url = True
        self.calc_maxima = True

        # Plugin-specific properties
        self.bgcolor: Tuple[int, int, int] = (255, 255, 255)  # white
        self.handcolor: str = "blue"
        self.config_message: str = ""

        self._parse_params(params)

    def _parse_params(self, params: str) -> None:
        for part in params.split(";"):
            p = part.strip()
            if not p:
                continue
            m = re.match(r"^[wW](\d+)$", p)
            if m:
                val = int(m.group(1))
                self.image_width_prozent = max(1, min(100, val))
                continue
            stripped = re.sub(r"\s+", "", p)
            if stripped == "mode=iframe":
                self.configuration_mode = 3  # CONFIGMODE_URL
            elif stripped == "mode=string":
                self.configuration_mode = 0  # CONFIGMODE_STRING
            elif stripped == "mode=jsf":
                self.configuration_mode = 1  # CONFIGMODE_JSF
            elif stripped == "mode=js":
                self.configuration_mode = 2  # CONFIGMODE_JAVASCRIPT
            else:
                self._parse_param(p)

    def _parse_param(self, p: str) -> None:
        m = re.match(r"^bgcolor=(.+)$", p)
        if m:
            color_name = m.group(1).strip()
            color_map = {
                "red": (255, 0, 0),
                "green": (0, 128, 0),
                "blue": (0, 0, 255),
                "gray": (128, 128, 128),
                "yellow": (255, 255, 0),
                "white": (255, 255, 255),
            }
            if color_name in color_map:
                self.bgcolor = color_map[color_name]
            else:
                self._add_config_message(f"bgcolor {color_name} not allowed")

    def _add_config_message(self, msg: str) -> None:
        if self.config_message:
            self.config_message += ", "
        self.config_message += msg

    # ------------------------------------------------------------------
    # Painting
    # ------------------------------------------------------------------

    def parse_draw_params(self, params: str, q: Optional[PluginQuestionDto], result: PluginImageResultDto) -> None:
        self.width = 500
        self.height = 500
        for part in params.split(","):
            m = re.match(r"^size=(\d+)x(\d+)$", part)
            if m:
                self.width = int(m.group(1))
                self.height = int(m.group(2))
                continue
            m = re.match(r"^size=(\d+)$", part)
            if m:
                v = int(m.group(1))
                self.width = v
                self.height = v

    def paint(self, draw: ImageDraw.Draw, result: PluginImageResultDto) -> None:
        x_mid = self.width // 2
        y_mid = self.height // 2
        radius = int(min(self.width, self.height) * 0.48)

        # Clock face
        draw.ellipse(
            [x_mid - radius, y_mid - radius, x_mid + radius, y_mid + radius],
            fill=self.bgcolor,
            outline=(0, 0, 0),
            width=2,
        )

        # Hour ticks and numbers
        for i in range(1, 13):
            alpha = math.pi / 2 - 2 * math.pi / 12 * i
            cos_a = math.cos(alpha)
            sin_a = math.sin(alpha)
            x1 = int(x_mid + radius * 0.9 * cos_a)
            y1 = int(y_mid - radius * 0.9 * sin_a)
            x2 = int(x_mid + radius * cos_a)
            y2 = int(y_mid - radius * sin_a)
            draw.line([x1, y1, x2, y2], fill=(0, 0, 255), width=4)

            # Hour number
            tx = int(x_mid + radius * 0.75 * cos_a)
            ty = int(y_mid - radius * 0.75 * sin_a)
            draw.text((tx, ty), str(i), fill=(0, 0, 0), anchor="mm")

        # Center dot
        dot_r = 7
        draw.ellipse(
            [x_mid - dot_r, y_mid - dot_r, x_mid + dot_r, y_mid + dot_r],
            fill=(0, 0, 0),
        )

    # ------------------------------------------------------------------
    # Variables
    # ------------------------------------------------------------------

    def get_vars(self) -> Optional[List[str]]:
        return None

    def get_image_templates(self) -> List[List[str]]:
        return [[f"Uhr ", f'[PIG {self.name} ""]', "Uhrblatt"]]

    # ------------------------------------------------------------------
    # Parser plugin
    # ------------------------------------------------------------------

    def parser_plugin(self, vars: Optional[VarHashDto], cp: Optional[CalcParamsDto], *p: CalcErgebnisDto) -> Optional[CalcErgebnisDto]:
        return None

    def parser_plugin_einheit(self, *p: str) -> Optional[str]:
        return None

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def score(
        self,
        plugin_dto: Optional[PluginDto],
        antwort: Optional[str],
        toleranz: Optional[ToleranzDto],
        vars_question: Optional[VarHashDto],
        plugin_answer_dto: Optional[PluginAnswerDto],
        grade: float,
    ) -> PluginScoreInfoDto:
        ze = plugin_answer_dto.ze if plugin_answer_dto else None
        answer_text = plugin_answer_dto.answerText if plugin_answer_dto else None

        info = PluginScoreInfoDto(
            schuelerErgebnis=CalcErgebnisDto(string=antwort, type=CALCERGEBNISTYPE.STRING),
            zielEinheit=ze,
            punkteIst=0.0,
            punkteSoll=grade,
            status=Score.FALSCH,
            htmlScoreInfo="",
            feedback="",
        )

        try:
            richtig = _parse_time(answer_text or "")
            eingabe = _parse_time(antwort or "")
            if _times_equal(richtig, eingabe, toleranz):
                info.status = Score.OK
                info.punkteIst = grade
        except Exception:
            pass

        info.htmlScoreInfo = f"Wert:{antwort}"
        return info

    # ------------------------------------------------------------------
    # load / reload PluginDto
    # ------------------------------------------------------------------

    def load_plugin_dto(self, params: str, q: Optional[PluginQuestionDto], nr: int) -> PluginDto:
        image_dto = self.get_image_dto(params, q)
        return PluginDto(
            imageUrl=image_dto.base64Image,
            tagName=self.name,
            width=self.width,
            height=self.height,
        )

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def configuration_info(self, configuration_id: Optional[str]) -> PluginConfigurationInfoDto:
        info = super().configuration_info(configuration_id)
        info.configurationMode = self.configuration_mode
        info.javaScriptMethode = self.config_plugin_js
        info.configurationID = configuration_id
        return info

    def set_configuration_data(self, configuration: Optional[str], question_dto: Optional[PluginQuestionDto]) -> PluginConfigDto:
        self.config = configuration or ""
        dto = PluginConfigDto()
        dto.params["TEST"] = "testinhalt"
        dto.params["help"] = self.get_help()
        dto.params["vars"] = str(question_dto.vars) if question_dto and question_dto.vars else "null"
        return dto

    def get_configuration(self) -> str:
        return self.config or ""
