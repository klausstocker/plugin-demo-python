from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.enums import (
    CALCERGEBNISTYPE,
    CALCMODE,
    IMAGEUNIT,
    InputElement,
    Score,
    SHOWPOTENZ,
    TOLERANZMODE,
)


# ---------------------------------------------------------------------------
# Basic value objects
# ---------------------------------------------------------------------------

class ToleranzDto(BaseModel):
    toleranz: float = 0.0
    mode: TOLERANZMODE = TOLERANZMODE.RELATIV

    def relativ(self) -> bool:
        return self.mode == TOLERANZMODE.RELATIV

    def absolut(self) -> bool:
        return self.mode == TOLERANZMODE.ABSOLUT


class CalcErgebnisDto(BaseModel):
    model_config = {"populate_by_name": True}

    string: Optional[str] = None
    json_data: Optional[str] = Field(default=None, alias="json")
    type: CALCERGEBNISTYPE = CALCERGEBNISTYPE.STRING


class CalcParamsDto(BaseModel):
    optmode: Optional[str] = None
    toleranz: Optional[ToleranzDto] = None
    rekursiv: bool = False
    symbolicMode: bool = False
    ausmultiplizieren: bool = False
    herausheben: bool = False
    forceOpt: bool = False
    showpotenz: SHOWPOTENZ = SHOWPOTENZ.AUTO
    calcmode: CALCMODE = CALCMODE.MAXIMA


class VarDto(BaseModel):
    calcErgebnisDto: Optional[CalcErgebnisDto] = None
    ze: Optional[str] = None
    cp: Optional[CalcParamsDto] = None


class VarHashDto(BaseModel):
    vars: Dict[str, VarDto] = Field(default_factory=dict)

    def get_string(self, key: str) -> Optional[str]:
        v = self.vars.get(key)
        if v and v.calcErgebnisDto:
            return v.calcErgebnisDto.string
        return None

    def get_calc_ergebnis_dto(self, key: str) -> Optional[CalcErgebnisDto]:
        v = self.vars.get(key)
        if v:
            return v.calcErgebnisDto
        return None


# ---------------------------------------------------------------------------
# Image DTOs
# ---------------------------------------------------------------------------

class ImageInfoDto(BaseModel):
    version: Optional[str] = None
    pluginTyp: Optional[str] = None
    filename: Optional[str] = None
    url: Optional[str] = None
    style: Optional[str] = None
    alternate: Optional[str] = None
    title: Optional[str] = None
    width: int = 0
    height: int = 0
    imageWidth: int = 0
    unit: IMAGEUNIT = IMAGEUNIT.px
    lifetime: int = 0

    def lifetime_outdated(self) -> bool:
        import time
        return self.lifetime > 0 and time.time() > self.lifetime


class ImageBase64Dto(BaseModel):
    base64Image: Optional[str] = None
    imageInfoDto: Optional[ImageInfoDto] = None
    error: Optional[str] = None


class ImageUrlDto(BaseModel):
    imageUrl: Optional[str] = None
    imageInfoDto: Optional[ImageInfoDto] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Javascript library
# ---------------------------------------------------------------------------

class JavascriptLibrary(BaseModel):
    library: Optional[str] = None
    name: Optional[str] = None
    globalName: Optional[str] = None
    local: Optional[str] = None
    js_code: Optional[str] = None

    LOCAL: str = Field(default="LOCAL", exclude=True)
    SERVER: str = Field(default="SERVER", exclude=True)
    JAVASCRIPT: str = Field(default="JAVASCRIPT", exclude=True)


# ---------------------------------------------------------------------------
# Plugin general info
# ---------------------------------------------------------------------------

class PluginGeneralInfo(BaseModel):
    typ: Optional[str] = None
    version: Optional[str] = None
    wikiHelp: Optional[str] = None
    helpUrl: Optional[str] = None
    help: Optional[str] = None
    defaultPluginConfig: bool = False
    math: bool = False
    pluginType: Optional[str] = None
    initPluginJS: Optional[str] = None
    javaScript: bool = False
    javascriptLibraries: List[JavascriptLibrary] = Field(default_factory=list)
    javascriptLibrariesLocal: List[JavascriptLibrary] = Field(default_factory=list)
    inputElement: Optional[str] = None
    cacheable: bool = True
    useVars: bool = True
    useCVars: bool = True
    useVarsMaxima: bool = True
    useMVars: bool = True
    pluginServiceURL: Optional[str] = None


class PluginGeneralInfoList(BaseModel):
    pluginInfos: List[PluginGeneralInfo] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Plugin configuration DTOs
# ---------------------------------------------------------------------------

class PluginConfigurationInfoDto(BaseModel):
    CONFIGMODE_STRING: int = Field(default=0, exclude=True)
    CONFIGMODE_JSF: int = Field(default=1, exclude=True)
    CONFIGMODE_JAVASCRIPT: int = Field(default=2, exclude=True)
    CONFIGMODE_URL: int = Field(default=3, exclude=True)

    configurationID: Optional[str] = None
    javaScriptMethode: Optional[str] = None
    configurationUrl: Optional[str] = None
    configurationMode: int = 1
    useQuestion: bool = True
    useVars: bool = True
    useCVars: bool = True
    useMaximaVars: bool = True
    useMVars: bool = True
    addDataSet: bool = True
    calcMaxima: bool = True
    externUrl: bool = False


# ---------------------------------------------------------------------------
# Question DTOs
# ---------------------------------------------------------------------------

class PluginSubQuestionDto(BaseModel):
    name: Optional[str] = None
    points: float = 0.0


class PluginQuestionDto(BaseModel):
    id: int = 0
    name: Optional[str] = None
    maximaDefs: Optional[str] = None
    moodlemac: Optional[str] = None
    maxima: Optional[str] = None
    points: float = 0.0
    dsNr: int = 0
    subQuestions: List[PluginSubQuestionDto] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
    imagesContent: List[str] = Field(default_factory=list)
    vars: Optional[VarHashDto] = None
    cvars: Optional[VarHashDto] = None
    varsMaxima: Optional[VarHashDto] = None
    mvars: Optional[VarHashDto] = None


# ---------------------------------------------------------------------------
# Plugin DTO
# ---------------------------------------------------------------------------

class PluginDto(BaseModel):
    imageUrl: Optional[str] = None
    tagName: Optional[str] = None
    jsonData: Optional[str] = None
    pig: bool = False
    result: bool = False
    width: int = 0
    height: int = 0
    params: Dict[str, str] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Dataset DTOs
# ---------------------------------------------------------------------------

class PluginDatasetDto(BaseModel):
    name: Optional[str] = None
    bereich: Optional[str] = None
    einheit: Optional[str] = None
    useTemplate: bool = False


class PluginDatasetListDto(BaseModel):
    datasets: List[PluginDatasetDto] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Answer / Score DTOs
# ---------------------------------------------------------------------------

class PluginAnswerDto(BaseModel):
    ergebnis: Optional[CalcErgebnisDto] = None
    answerText: Optional[str] = None
    ze: Optional[str] = None


class PluginScoreInfoDto(BaseModel):
    schuelerErgebnis: Optional[CalcErgebnisDto] = None
    zielEinheit: Optional[str] = None
    htmlScoreInfo: Optional[str] = None
    feedback: Optional[str] = None
    punkteIst: float = 0.0
    punkteSoll: float = 0.0
    status: Score = Score.NotScored


# ---------------------------------------------------------------------------
# Render DTOs
# ---------------------------------------------------------------------------

class PluginRenderDto(BaseModel):
    source: Optional[str] = None
    images: Dict[str, str] = Field(default_factory=dict)


class PluginImageResultDto(BaseModel):
    ok: bool = True
    messages: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Maxima calc mode
# ---------------------------------------------------------------------------

class PluginMaximaCalcModeDto(BaseModel):
    maxima: bool = False
    preCalc: bool = False


# ---------------------------------------------------------------------------
# Config DTO
# ---------------------------------------------------------------------------

class PluginConfigDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    tagName: Optional[str] = None
    configurationID: Optional[str] = None
    errorMsg: Optional[str] = None
    pluginDtoUri: Optional[str] = None
    pluginDtoToken: Optional[str] = None
    jsonData: Optional[str] = None
    width: int = 0
    height: int = 0
    pluginDto: Optional[PluginDto] = None
    params: Dict[str, str] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Request DTOs
# ---------------------------------------------------------------------------

class PluginRequestDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    params: Optional[str] = None
    q: Optional[PluginQuestionDto] = None
    pluginMaximaCalcMode: Optional[PluginMaximaCalcModeDto] = None


class LoadPluginRequestDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    params: Optional[str] = None
    configurationID: Optional[str] = None
    q: Optional[PluginQuestionDto] = None
    nr: int = 0


class PluginScoreRequestDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    antwort: Optional[str] = None
    pluginDto: Optional[PluginDto] = None
    toleranz: Optional[ToleranzDto] = None
    varsQuestion: Optional[VarHashDto] = None
    answerDto: Optional[PluginAnswerDto] = None
    grade: float = 0.0


class PluginRenderResultRequestDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    antwort: Optional[str] = None
    tex: bool = False
    pluginDto: Optional[PluginDto] = None
    toleranz: Optional[ToleranzDto] = None
    varsQuestion: Optional[VarHashDto] = None
    answerDto: Optional[PluginAnswerDto] = None
    grade: float = 0.0


class PluginRenderLatexRequestDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    answer: Optional[str] = None
    mode: Optional[str] = None
    pluginDto: Optional[PluginDto] = None


class PluginParserRequestDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    vars: Optional[VarHashDto] = None
    cp: Optional[CalcParamsDto] = None
    p: List[CalcErgebnisDto] = Field(default_factory=list)


class PluginAngabeRequestDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    text: Optional[str] = None
    q: Optional[PluginQuestionDto] = None


class PluginEinheitRequestDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    p: List[str] = Field(default_factory=list)


class PluginConfigurationInfoRequestDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    configurationID: Optional[str] = None
    timeout: int = 0


class PluginSetConfigurationDataRequestDto(BaseModel):
    typ: Optional[str] = None
    configurationID: Optional[str] = None
    configuration: Optional[str] = None
    questionDto: Optional[PluginQuestionDto] = None


class PluginConfigurationRequestDto(BaseModel):
    typ: Optional[str] = None
    configurationID: Optional[str] = None


class PluginUpdateJavascriptRequestDto(BaseModel):
    typ: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    pluginDef: Optional[str] = None
    jsResult: Optional[str] = None


# ---------------------------------------------------------------------------
# Service / Admin Info DTOs
# ---------------------------------------------------------------------------

class AdminInfoDto(BaseModel):
    servicename: Optional[str] = None
    pid: Optional[str] = None
    homedir: Optional[str] = None
    version: Optional[str] = None
    time: Optional[str] = None
    betriebssystem: Optional[str] = None
    ip: Optional[str] = None
    encoding: Optional[str] = None
    fileEncoding: Optional[str] = None
    fileSeparator: Optional[str] = None
    javaSpecificVersion: Optional[str] = None
    javaVendor: Optional[str] = None
    javaVersion: Optional[str] = None
    javaVersionNumber: Optional[str] = None
    hostname: Optional[str] = None
    language: Optional[str] = None
    linuxDescription: Optional[str] = None
    linuxDistribution: Optional[str] = None
    linuxRelease: Optional[str] = None
    serverUsername: Optional[str] = None
    serverVersion: Optional[str] = None
    systemHome: Optional[str] = None
    startuptime: int = 0
    updtime: int = 0
    isLinux: bool = False
    isUbuntu: bool = False
    isWindows: bool = False
    httpPort: int = 8080
    ajpPort: int = 0
    httpsPort: int = 0


class ServiceInfoDTO(BaseModel):
    serviceName: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    license: Optional[str] = None
    endpoints: Optional[str] = None
    jarfilename: Optional[str] = None
    starttime: Optional[str] = None
    adminInfoDto: Optional[AdminInfoDto] = None
    jarLibs: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Register / Config service DTOs
# ---------------------------------------------------------------------------

class RegisterServiceResultDto(BaseModel):
    registrationOK: bool = False
    newRegistered: bool = False
    registrationCounter: int = 0
    msg: Optional[str] = None


class ConfigServiceDto(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    license: Optional[str] = None
    bs: Optional[str] = None
    ip: Optional[str] = None
    encoding: Optional[str] = None
    programmingLanguage: Optional[str] = None
    nwLettoAddress: Optional[str] = None
    dockerName: Optional[str] = None
    uriIntern: Optional[str] = None
    uriInternOk: bool = False
    uriExtern: Optional[str] = None
    uriExternOk: bool = False
    username: Optional[str] = None
    password: Optional[str] = None
    extern: bool = False
    plugin: bool = False
    scalable: bool = False
    stateless: bool = False
    usePluginToken: bool = False
    serviceStartTime: int = 0
    lastRegistrationTime: int = 0
    params: Dict[str, str] = Field(default_factory=dict)
