"""Centralised endpoint path constants matching the Java Endpoint class."""


class Endpoint:
    servicepath = "/plugindemo"
    open = servicepath + "/open"
    LOCAL_API = "/open"
    EXTERN_API = servicepath + "/auth/user"
    EXTERN_OPEN = servicepath + "/api/open"

    # Info endpoints
    ping = "/ping"
    pingopen = open + "/ping"
    INFO = "/info"
    INFO_OPEN = open + "/info"
    VERSION = open + "/version"

    # Plugin endpoints
    getPluginList = "/pluginlist"
    getPluginGeneralInfoList = "/generalinfolist"
    getPluginGeneralInfo = "/generalinfo"
    getHTML = "/gethtml"
    getAngabe = "/angabe"
    generateDatasets = "/generatedatasets"
    getMaxima = "/maxima"
    getImage = "/image"
    getImageUrl = "/imageurl"
    getImageTemplates = "/imagetemplates"
    parserPlugin = "/parserplugin"
    parserPluginEinheit = "/parserplugineinheit"
    score = "/score"
    getVars = "/getvars"
    modifyAngabe = "/modifyangabe"
    modifyAngabeTextkomplett = "/modifyangabetextkomplett"
    updatePluginstringJavascript = "/updatepluginstringjavascript"
    loadPluginDto = "/loadplugindto"
    reloadPluginDto = "/reloadplugindto"
    renderLatex = "/renderlatex"
    renderPluginResult = "/renderpluginresult"
    configurationInfo = "/configurationinfo"
    configurationHttp = "/confighttp"
    setConfigurationData = "/setconfigurationdata"
    getConfiguration = "/getconfiguration"

    iframeConfig = open + configurationHttp
