# -*- coding: utf-8 -*-
"""Exa Search — check if mcporter + Exa MCP is available."""

import shutil

from .base import Channel
from .mcporter import McporterConfigError, inspect_mcporter_config


class ExaSearchChannel(Channel):
    name = "exa_search"
    description = "Tüm web'de anlamsal arama"
    backends = ["Exa via mcporter"]
    tier = 0

    def can_handle(self, url: str) -> bool:
        return False  # Search-only channel

    def check(self, config=None):
        self.active_backend = None
        if not shutil.which("mcporter"):
            return "off", (
                "mcporter + Exa MCP gerekli. Kurulum:\n"
                "  npm install -g mcporter\n"
                "  mcporter config add exa https://mcp.exa.ai/mcp --scope home"
            )
        try:
            inspection = inspect_mcporter_config()
        except McporterConfigError as exc:
            return "error", f"mcporter yapılandırma kontrolü başarısız: {exc}"
        if "exa" in inspection.server_names:
            return "warn", (
                "Exa mcporter yapılandırmasına yazılmış, ancak Doctor uzak servisi "
                "başlatıp bağlantıyı doğrulamadı; yalnızca yapılandırmaya bakarak "
                "kullanılabilir denemez."
            )
        if inspection.imports_unchecked:
            return "warn", (
                "mcporter yerel yapılandırmasında Exa bulunamadı; yapılandırmada editor "
                "imports da açık, Doctor kimlik bilgisi okuma kapsamını genişletmemek için "
                "bunları açmadı, şimdilik doğrulanmadı."
            )
        return "off", (
            "mcporter kurulu ama Exa yapılandırılmamış. Çalıştır:\n"
            "  mcporter config add exa https://mcp.exa.ai/mcp --scope home"
        )
