# -*- coding: utf-8 -*-
"""Shared channel helper for OpenCLI browser-session-only platforms."""

from agent_reach.utils.url import host_matches

from .base import Channel


class OpenCLISiteChannel(Channel):
    """A platform served directly by OpenCLI.

    These channels are intentionally thin: Agent Reach only installs,
    health-checks, and routes. Agents call `opencli <site> ...` directly.
    """

    site: str = ""
    domains: tuple[str, ...] = ()
    usage: str = ""
    login_hint: str = ""

    backends = ["OpenCLI"]
    tier = 1

    def can_handle(self, url: str) -> bool:
        return host_matches(url, *self.domains)

    def check(self, config=None):
        from agent_reach.backends import opencli_status

        self.active_backend = None
        st = opencli_status()
        if not st.installed:
            return "off", (
                f"{self.description} backend'i kurulu değil. Kurulum:\n"
                "  agent-reach install --system --channels opencli\n"
                f"Ardından Chrome'da {self.login_hint} hesabına giriş yap"
            )
        if st.broken:
            return "error", st.hint

        if st.ready:
            return "warn", (
                f"OpenCLI köprüsü bağlı, ancak {self.description} giriş durumu ve "
                "gerçek komutlar canlı doğrulanmadı; Doctor platform komutu "
                "çalıştırmadığı için kanal şimdilik kullanılabilir olarak işaretlenmiyor. "
                f"Gerektiğinde önce Chrome'da {self.login_hint} hesabına giriş yap"
            )
        return "warn", st.hint
