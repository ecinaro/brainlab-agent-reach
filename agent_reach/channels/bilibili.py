# -*- coding: utf-8 -*-
"""Bilibili — multi-backend: bili-cli / OpenCLI / search API.

yt-dlp was REMOVED from this channel (live-verified 2026-06): bilibili's
risk control 412-blocks yt-dlp's requests in every configuration we
tried — latest version, direct, proxied, with warmed cookies — while
bili-cli keeps working (search/hot/video detail without login) and
OpenCLI covers subtitles through the browser session. yt-dlp remains the
YouTube backend; it just no longer serves bilibili.
"""

import json
import urllib.request

from agent_reach.probe import probe_command

from .base import Channel

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
_TIMEOUT = 10
_SEARCH_API = "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=test&page=1"


def _search_api_ok() -> bool:
    """Return True if Bilibili search API responds with code 0."""
    req = urllib.request.Request(_SEARCH_API, headers={"User-Agent": _UA})
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            data = json.loads(resp.read())
            return data.get("code") == 0
    except Exception:
        return False


class BilibiliChannel(Channel):
    name = "bilibili"
    description = "Bilibili videoları, altyazıları ve arama"
    backends = ["bili-cli", "OpenCLI", "Bilibili Search API"]
    # Pre-localization name kept so existing `bilibili_backend` overrides still match.
    backend_aliases = {"B站搜索 API": "Bilibili Search API"}
    tier = 1

    def can_handle(self, url: str) -> bool:
        from agent_reach.utils.url import host_matches

        return host_matches(url, "bilibili.com", "b23.tv")

    def check(self, config=None):
        """Probe candidates in order; first fully-usable backend wins."""
        self.active_backend = None
        findings = []

        for backend in self.ordered_backends(config):
            if backend == "bili-cli":
                result = self._check_bili_cli()
            elif backend == "OpenCLI":
                result = self._check_opencli()
            else:
                result = self._check_search_api()
            if result is None:
                continue
            findings.append((backend, *result))

        # If a backend is broken, surface its fix even when another candidate works
        broken_notes = [m for _, s, m in findings if s == "error"]

        for wanted in ("ok", "warn"):
            for backend, status, message in findings:
                if status == wanted:
                    self.active_backend = backend if status == "ok" else None
                    if broken_notes:
                        message += "\n[Yedek backend hatası] " + "; ".join(broken_notes)
                    return status, message

        if findings:
            return "error", "\n".join(m for _, _, m in findings)

        return "off", (
            "Kullanılabilir Bilibili backend'i yok (arama API'sine de ulaşılamıyor, "
            "ağ sorunu olabilir). Önerilen:\n"
            "  pipx install bilibili-cli (arama/popüler/video detayı, giriş gerekmez)\n"
            "  veya masaüstünde OpenCLI kur (altyazıları da açar): "
            "agent-reach install --system --channels opencli"
        )

    def _check_bili_cli(self):
        """bili-cli candidate. None = not installed."""
        probe = probe_command("bili", ["--version"], timeout=10, package="bilibili-cli")
        if probe.status == "missing":
            return None
        if probe.status == "broken":
            return "error", "bili komutu var ama çalıştırılamıyor\n" + probe.hint
        if not probe.ok:
            return "warn", (
                f"bili-cli yoklaması başarısız ({probe.status}), "
                "ayrıntılar için `bili status` çalıştır"
            )
        return "ok", (
            "bili-cli kullanılabilir (arama/popüler/sıralama/video detayı/ses, giriş gerekmez; "
            "altyazılar için OpenCLI gerekli. Upstream 2026-03'ten beri güncellenmiyor)"
        )

    def _check_opencli(self):
        """OpenCLI candidate. None = not installed."""
        from agent_reach.backends import opencli_status

        st = opencli_status()
        if not st.installed:
            return None
        if st.broken:
            return "error", st.hint
        if st.ready:
            return "warn", (
                "OpenCLI köprüsü bağlı, ancak Bilibili sayfaları, giriş durumu ve gerçek "
                "komutlar canlı doğrulanmadı; Doctor platform komutu çalıştırmadığı için "
                "kanal şimdilik kullanılabilir olarak işaretlenmiyor."
            )
        return "warn", st.hint

    def _check_search_api(self):
        """Zero-dependency search API fallback. None = unreachable."""
        if not _search_api_ok():
            return None
        return "ok", (
            "Bilibili arama API'sine ulaşılabiliyor (yalnızca arama, doğrudan curl). "
            "Tüm özellikler için bili-cli kur: pipx install bilibili-cli"
        )
