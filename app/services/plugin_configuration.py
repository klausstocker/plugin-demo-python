"""PluginConfiguration – manages the single plugin and its lifecycle."""

from __future__ import annotations

import logging
import platform
import socket
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Type

import httpx


def _to_date_integer(dt: datetime) -> int:
    """Convert a datetime to a Java Datum 'DateInteger' (seconds since 1 Jan year 0).

    Java's ``Datum.toDateInteger(LocalDateTime)`` returns ``days * 86400 + time_of_day``
    where *days* is counted from 1 January of year 0 (ISO proleptic Gregorian, i.e. 1 BCE).
    Python's ``date.toordinal()`` starts at 1 for 1 Jan year 1, so year 0 contributes
    an extra 366 days (year 0 is a proleptic leap year: 366 days).
    """
    days_since_year0 = dt.date().toordinal() + 365  # ordinal(0001-01-01)==1; add 365 to account for year 0's 366 days
    time_of_day = dt.hour * 3600 + dt.minute * 60 + dt.second
    return days_since_year0 * 86400 + time_of_day


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
    """Manages a single plugin type and its lifecycle."""

    SERVICE_NAME = "letto-plugindemo"
    VERSION = "1.0"
    AUTHOR = "LeTTo GmbH"
    LICENSE = "OpenSource"

    def __init__(self) -> None:
        self._plugin_class: Optional[Type[PluginService]] = None
        self._plugin_name: str = ""
        self._plugin_info: Optional[PluginGeneralInfo] = None
        self._active_configurations: Dict[str, PluginService] = {}
        self._start_time: float = time.time()

    def register_plugin(self, name: str, plugin_class: Type[PluginService]) -> None:
        """Register the plugin implementation under the given type name."""
        self._plugin_class = plugin_class
        self._plugin_name = name
        plugin = plugin_class(name="", params="")
        info = plugin.get_plugin_general_info()
        info.typ = name
        info.pluginType = f"{plugin_class.__module__}.{plugin_class.__qualname__}"
        self._plugin_info = info

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

        now_ms = _to_date_integer(datetime.now())

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
            uriIntern=settings.letto_plugin_uri_intern or f"http://{settings.network_letto_address}:{settings.port}/open",
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
            serviceStartTime=_to_date_integer(datetime.fromtimestamp(self._start_time)),
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

    def create_plugin(self, name: str, config: str) -> PluginService:
        """Create a new instance of the registered plugin."""
        if self._plugin_class is None:
            raise RuntimeError("No plugin registered – call register_plugin() first")
        return self._plugin_class(name=name or "", params=config or "")

    def get_plugin_list(self) -> List[str]:
        if self._plugin_name:
            return [self._plugin_name]
        return []

    def get_plugin_general_info(self) -> Optional[PluginGeneralInfo]:
        return self._plugin_info

    def get_plugin_general_info_list(self) -> PluginGeneralInfoList:
        if self._plugin_info is None:
            return PluginGeneralInfoList(pluginInfos=[])
        return PluginGeneralInfoList(pluginInfos=[self._plugin_info])

    # ------------------------------------------------------------------
    # Configuration session management
    # ------------------------------------------------------------------

    def configuration_info(
        self, name: str, config: str, configuration_id: str, timeout: int
    ) -> PluginConfigurationInfoDto:
        plugin = self.create_plugin(name, config)
        info = plugin.configuration_info(configuration_id)
        self._active_configurations[configuration_id] = plugin
        return info

    def set_configuration_data(
        self, configuration_id: str, configuration: str, question_dto
    ) -> Optional[PluginConfigDto]:
        plugin = self._active_configurations.get(configuration_id)
        if plugin is None:
            plugin = self.create_plugin("", configuration)
        return plugin.set_configuration_data(configuration, question_dto)

    def get_configuration(self, configuration_id: str) -> Optional[str]:
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
