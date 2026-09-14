# -*- coding: utf-8 -*-
"""Web — any URL via Jina Reader. Always available.

OpenCLI is the general fallback for sites Jina Reader cannot read (login
walls, Cloudflare challenges, JS-only pages). Channel status stays driven by
Jina so the web channel remains usable with zero configuration.
"""

import urllib.request

from agent_reach.utils.url import normalize_public_http_url

from .base import Channel

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
_MAX_RESPONSE_BYTES = 5 * 1024 * 1024
_ANTIBOT_SCAN_BYTES = 4096
#: Keep doctor fast: the OpenCLI fallback line is informational only.
_OPENCLI_PROBE_TIMEOUT = 5

OPENCLI_INSTALL_HINT = (
    "Yedek (isteğe bağlı): giriş/Cloudflare/JS engelli siteler için "
    "`agent-reach install --system --channels opencli` + Chrome eklentisi"
)


def _is_antibot_page(body: bytes) -> bool:
    """Recognize high-confidence Jina/Cloudflare challenge responses."""
    sample = body[:_ANTIBOT_SCAN_BYTES].decode("utf-8", errors="ignore").casefold()

    jina_captcha_warning = "warning:" in sample and "requiring captcha" in sample
    challenge_structure = any(
        marker in sample
        for marker in (
            "title: just a moment...",
            "## performing security verification",
            "title: attention required! | cloudflare",
        )
    )
    cloudflare_block = "title: attention required! | cloudflare" in sample and (
        "ray id" in sample or "/cdn-cgi/challenge-platform/" in sample
    )
    return (jina_captcha_warning and challenge_structure) or cloudflare_block


def _opencli_fallback_line() -> str:
    """Describe the OpenCLI fallback state without side effects.

    Reuses the shared side-effect-free probe; any failure degrades to the
    install hint so the web channel itself can never error because of it.
    """
    from agent_reach.backends.opencli import opencli_status, opencli_summary

    try:
        st = opencli_status(timeout=_OPENCLI_PROBE_TIMEOUT)
    except Exception:  # noqa: BLE001 — fallback info must never break web
        return OPENCLI_INSTALL_HINT
    if not st.installed:
        return OPENCLI_INSTALL_HINT
    if st.broken:
        return f"Yedek uyarısı: {opencli_summary(st)}"
    if st.ready:
        return "Erişilemeyen siteler için yedek: OpenCLI hazır (Chrome eklentisi bağlı)"
    return (
        "Yedek OpenCLI kurulu ama Chrome eklentisi bağlı değil — "
        "chrome://extensions içinden OpenCLI'ı aç"
    )


class WebChannel(Channel):
    name = "web"
    description = "Herhangi bir web sayfası"
    backends = ["Jina Reader", "OpenCLI"]
    tier = 0

    def can_handle(self, url: str) -> bool:
        return True  # Fallback — handles any URL

    def check(self, config=None):
        # Always-available fallback channel: Jina Reader needs no local command
        # and no network probe, so status stays "ok". The OpenCLI line is
        # informational (general fallback for blocked sites).
        self.active_backend = self.backends[0]
        return "ok", (
            "Jina Reader ile herhangi bir web sayfası okunur "
            "(curl https://r.jina.ai/URL)\n"
            + _opencli_fallback_line()
        )

    def read(self, url: str) -> str:
        """Read a web page via Jina Reader and return the full Markdown."""
        url = normalize_public_http_url(url)
        jina_url = f"https://r.jina.ai/{url}"
        req = urllib.request.Request(
            jina_url,
            headers={"User-Agent": _UA, "Accept": "text/plain"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read(_MAX_RESPONSE_BYTES + 1)
        if len(body) > _MAX_RESPONSE_BYTES:
            raise ValueError(
                f"Jina Reader response exceeds {_MAX_RESPONSE_BYTES} byte limit"
            )
        if _is_antibot_page(body):
            raise RuntimeError(
                "Jina Reader bot doğrulama sayfası döndürdü, hedef içerik alınamadı; "
                "siteye özel bir araç, OpenCLI veya tarayıcı ile oku"
            )
        return body.decode("utf-8")
