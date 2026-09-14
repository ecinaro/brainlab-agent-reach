# -*- coding: utf-8 -*-
"""LinkedIn — check if mcp-server-linkedin is configured."""

import shutil

from .base import Channel
from .mcporter import McporterConfigError, inspect_mcporter_config

_LINKEDIN_SERVER_NAMES = {
    "linkedin",
    "linkedin-scraper",
    "linkedin-scraper-mcp",
    "mcp-server-linkedin",
}
_LOGIN_COMMAND = "uvx mcp-server-linkedin@latest --login"
_UV_INSTALL_URL = "https://docs.astral.sh/uv/getting-started/installation/"
_CONFIG_COMMAND = (
    "mcporter config add linkedin --command uvx "
    "--arg mcp-server-linkedin@latest --env UV_HTTP_TIMEOUT=300 --scope home"
)


class LinkedInChannel(Channel):
    name = "linkedin"
    description = "LinkedIn profesyonel ağ"
    backends = ["mcp-server-linkedin", "Jina Reader"]
    tier = 2

    def can_handle(self, url: str) -> bool:
        from agent_reach.utils.url import host_matches

        return host_matches(url, "linkedin.com")

    def check(self, config=None):
        self.active_backend = None
        if not shutil.which("mcporter"):
            return "off", (
                "Temel içerik Jina Reader ile okunabilir. Tüm özellikler için:\n"
                f"  Önce uv/uvx kur: {_UV_INSTALL_URL}\n"
                f"  {_LOGIN_COMMAND}\n"
                f"  {_CONFIG_COMMAND}\n"
                "  Ayrıntılar: https://github.com/stickerdaniel/linkedin-mcp-server"
            )
        try:
            inspection = inspect_mcporter_config()
        except McporterConfigError as exc:
            return "error", f"mcporter yapılandırma kontrolü başarısız: {exc}"
        if inspection.server_names & _LINKEDIN_SERVER_NAMES:
            if not shutil.which("uvx"):
                return "warn", (
                    "LinkedIn MCP mcporter yapılandırmasına yazılmış, ancak uvx kurulu değil; "
                    "servis şu an başlatılamaz. Kurulum:\n"
                    f"  {_UV_INSTALL_URL}"
                )
            return "warn", (
                "LinkedIn MCP mcporter yapılandırmasına yazılmış, ancak Doctor yerel servisi "
                "başlatıp bağlantıyı doğrulamadı; yalnızca yapılandırmaya bakarak tam "
                "kullanılabilir denemez."
            )
        if inspection.imports_unchecked:
            return "warn", (
                "mcporter yerel yapılandırmasında LinkedIn MCP bulunamadı; yapılandırmada editor "
                "imports da açık, Doctor kimlik bilgisi okuma kapsamını genişletmemek için "
                "bunları açmadı, şimdilik doğrulanmadı."
            )
        return "off", (
            "mcporter kurulu ama LinkedIn MCP yapılandırılmamış. Çalıştır:\n"
            f"  Önce uv/uvx kur: {_UV_INSTALL_URL}\n"
            f"  {_LOGIN_COMMAND}\n"
            f"  {_CONFIG_COMMAND}"
        )
