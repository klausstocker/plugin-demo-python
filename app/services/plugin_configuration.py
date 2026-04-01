"""PluginConfiguration – manages plugin registration and lifecycle."""

from __future__ import annotations

import logging
import platform
import socket
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Type

import httpx

from app.config import settings
from app.models.dto import (
    AdminInfoDto,
    ConfigServiceDto,
    PluginConfigDto,
    PluginConfigurationInfoDto,
    PluginGeneralInfo,
    PluginGeneralInfoList,
    RegisterServiceResultDto,
    ServiceInfoDTO,
)
from app.services.plugin_service import PluginService

logger = logging.getLogger(__name__)


class PluginConfiguration:
    """Central registry and factory for plugins."""

    SERVICE_NAME = "plugin-demo-python"
    VERSION = "0.1"
    AUTHOR = "letto.at"
    LICENSE = "Apache-2.0"

    def __init__(self) -> None:
        self._registry: Dict[str, Type[PluginService]] = {}
        self._active_configurations: Dict[str, PluginService] = {}
        self._start_time: float = time.time()

    def init(self) -> None:
        """Called once at application startup."""
        pass

    def register_plugin_in_setup(self) -> None:
        """Register this service with the external LeTTo setup service."""
        setup_uri = settings.letto_setup_uri
        if not setup_uri:
            logger.info("LETTO_SETUP_URI not configured – skipping setup-service registration")
            return

        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
        except OSError:
            ip = ""

        now_ms = int(time.time() * 1000)

        payload = ConfigServiceDto(
            name=self.SERVICE_NAME,
            version=self.VERSION,
            author=self.AUTHOR,
            license=self.LICENSE,
            bs=platform.system(),
            ip=ip,
            encoding=sys.getdefaultencoding(),
            programmingLanguage=f"Python {sys.version.split()[0]}",
            nwLettoAddress=settings.network_letto_address,
            dockerName=settings.docker_container_name,
            uriIntern=settings.letto_plugin_uri_intern or f"http://{settings.network_letto_address}:{settings.port}",
            uriInternOk=True,
            uriExtern=settings.letto_plugin_uri_extern or "",
            uriExternOk=bool(settings.letto_plugin_uri_extern),
            username=settings.service_user_username,
            password=settings.service_user_password,
            extern=False,
            plugin=True,
            scalable=False,
            stateless=True,
            usePluginToken=False,
            serviceStartTime=int(self._start_time * 1000),
            lastRegistrationTime=now_ms,
        )

        url = f"{setup_uri.rstrip('/')}/config/auth/user/registerplugin"
        try:
            response = httpx.post(
                url,
                json=payload.model_dump(),
                auth=httpx.BasicAuth(username=settings.service_user_username, password=settings.service_user_password),
                timeout=10.0,
            )
            response.raise_for_status()
            result = RegisterServiceResultDto.model_validate(response.json())
            if not result.registrationOK:
                logger.error("Setup service refused registration: %s", result.msg)
            else:
                status = "NEW" if result.newRegistered else "UPDATED"
                counter = (
                    f", {result.registrationCounter} instances"
                    if result.registrationCounter > 1
                    else ""
                )
                logger.info("Plugin registered in setup-service %s%s", status, counter)
        except httpx.HTTPStatusError as exc:
            logger.error("Setup service returned error %s: %s", exc.response.status_code, exc.response.text)
        except httpx.RequestError as exc:
            logger.error("Setup service cannot be reached at %s: %s", url, exc)

    def register_plugin(self, name: str, plugin_class: Type[PluginService]) -> None:
        """Register a plugin implementation under the given type name."""
        self._registry[name] = plugin_class

    def create_plugin_service(self, typ: str, name: str, config: str) -> Optional[PluginService]:
        """Instantiate a plugin by type."""
        cls = self._registry.get(typ)
        if cls is None:
            return None
        return cls(name=name or "", params=config or "")

    def get_plugin_list(self) -> List[str]:
        return list(self._registry.keys())

    def get_plugin_general_info(self, typ: str) -> Optional[PluginGeneralInfo]:
        plugin = self.create_plugin_service(typ, "", "")
        if plugin is None:
            return None
        return plugin.get_plugin_general_info()

    def get_plugin_general_info_list(self) -> PluginGeneralInfoList:
        infos = []
        for typ in self._registry:
            info = self.get_plugin_general_info(typ)
            if info:
                infos.append(info)
        return PluginGeneralInfoList(pluginInfos=infos)

    # ------------------------------------------------------------------
    # Configuration session management
    # ------------------------------------------------------------------

    def configuration_info(
        self, typ: str, name: str, config: str, configuration_id: str, timeout: int
    ) -> Optional[PluginConfigurationInfoDto]:
        plugin = self.create_plugin_service(typ, name, config)
        if plugin is None:
            return None
        info = plugin.configuration_info(configuration_id)
        self._active_configurations[configuration_id] = plugin
        return info

    def set_configuration_data(
        self, typ: str, configuration_id: str, configuration: str, question_dto
    ) -> Optional[PluginConfigDto]:
        plugin = self._active_configurations.get(configuration_id)
        if plugin is None:
            plugin = self.create_plugin_service(typ, "", configuration)
        if plugin is None:
            return None
        return plugin.set_configuration_data(configuration, question_dto)

    def get_configuration(self, typ: str, configuration_id: str) -> Optional[str]:
        plugin = self._active_configurations.get(configuration_id)
        if plugin is None:
            return None
        return plugin.get_configuration()

    # ------------------------------------------------------------------
    # Service info
    # ------------------------------------------------------------------

    def get_service_info_dto(self) -> ServiceInfoDTO:
        admin = AdminInfoDto(
            servicename=self.SERVICE_NAME,
            version=self.VERSION,
            betriebssystem=platform.system(),
            hostname=socket.gethostname(),
            ip=socket.gethostbyname(socket.gethostname()) if socket.gethostname() else "",
            startuptime=int(self._start_time * 1000),
            isLinux=platform.system().lower() == "linux",
            isWindows=platform.system().lower() == "windows",
            httpPort=8080,
        )
        return ServiceInfoDTO(
            serviceName=self.SERVICE_NAME,
            version=self.VERSION,
            author=self.AUTHOR,
            license=self.LICENSE,
            starttime=datetime.fromtimestamp(self._start_time).isoformat(),
            adminInfoDto=admin,
        )


# Singleton instance used across the application
plugin_configuration = PluginConfiguration()
