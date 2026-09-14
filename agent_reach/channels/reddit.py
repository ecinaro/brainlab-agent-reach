# -*- coding: utf-8 -*-
"""Reddit — multi-backend: OpenCLI / rdt-cli. Login is mandatory.

Honest tiering (live-verified 2026-06): there is NO zero-config path.
Anonymous .json endpoints are blocked (403 anti-bot, all variants), and
the official API closed self-service registration in 2025-11 (manual
approval, individual scripts rarely granted — PRAW is only an option for
users who already hold credentials). Every working backend rides a
logged-in session: OpenCLI reuses the browser's, rdt-cli imports cookies.
"""

import json
import shutil
import time
from pathlib import Path

from agent_reach.utils.paths import (
    PrivatePathError,
    read_small_text_no_follow,
)

from .base import Channel

_CREDENTIAL_FILE = "~/.config/rdt-cli/credential.json"
_CREDENTIAL_TTL_SECONDS = 7 * 86400
_MAX_CREDENTIAL_BYTES = 1024 * 1024
# Pinned to the 0.4.2 state — PyPI still only has 0.4.1 (upstream issue #10).
_RDT_GIT_SOURCE = "git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66"

class RedditChannel(Channel):
    name = "reddit"
    description = "Reddit gönderileri ve yorumları"
    backends = ["OpenCLI", "rdt-cli"]
    tier = 1  # no zero-config path exists — see module docstring

    def can_handle(self, url: str) -> bool:
        from agent_reach.utils.url import host_matches

        return host_matches(url, "reddit.com", "redd.it")

    def check(self, config=None):
        """Probe candidates in order; first fully-usable backend wins."""
        self.active_backend = None
        findings = []

        for backend in self.ordered_backends(config):
            if backend == "OpenCLI":
                result = self._check_opencli()
            else:
                result = self._check_rdt()
            if result is None:
                continue
            findings.append((backend, *result))

        for wanted in ("ok", "warn"):
            for backend, status, message in findings:
                if status == wanted:
                    self.active_backend = backend if status == "ok" else None
                    return status, message

        if findings:
            return "error", "\n".join(m for _, _, m in findings)

        return "off", (
            "Hiçbir Reddit backend'i kurulu değil. Not: Reddit için kurulumsuz bir yol yok "
            "(anonim .json engellendi, resmi API manuel onay istiyor), giriş yapılmış "
            "oturum şart. Önerilen:\n"
            "  Masaüstü: agent-reach install --system --channels opencli\n"
            "       (Chrome oturumunu kullanır, reddit.com'a giriş yaptıysan yeterli)\n"
            f"  Sunucu/mevcut kurulum: pipx install '{_RDT_GIT_SOURCE}'\n"
            "       ardından `rdt login` veya Cookie'yi elle yaz (doctor ipuçlarına bak)\n"
            "Çin anakarasından Reddit erişimi için proxy gerekir"
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
                "OpenCLI köprüsü bağlı, ancak Reddit giriş durumu ve gerçek komutlar canlı "
                "doğrulanmadı; Doctor platform komutu çalıştırmadığı için kanal şimdilik "
                "kullanılabilir olarak işaretlenmiyor."
            )
        return "warn", st.hint

    def _check_rdt(self):
        """Inspect rdt's saved credential without invoking its auto-refresh."""
        if not shutil.which("rdt"):
            return None

        credential_path = Path.home() / ".config" / "rdt-cli" / "credential.json"
        try:
            payload = read_small_text_no_follow(
                credential_path,
                max_bytes=_MAX_CREDENTIAL_BYTES,
            )
        except PrivatePathError as exc:
            return "warn", (
                f"rdt-cli kurulu, ancak credential.json güvenli şekilde okunamadı: {exc}."
            )
        except OSError:
            return "warn", (
                "rdt-cli kurulu, ancak credential.json güvenli şekilde okunamadı; "
                "Doctor, Cookie'yi otomatik yenileyen `rdt status` komutunu çalıştırmadı."
            )
        if payload is None:
            return "warn", self._rdt_login_hint()
        try:
            data = json.loads(payload)
        except (UnicodeError, json.JSONDecodeError, ValueError):
            return "warn", (
                "rdt-cli kurulu, ancak kayıtlı credential.json güvenli şekilde ayrıştırılamadı; "
                "Doctor, Cookie'yi otomatik yenileyen `rdt status` komutunu çalıştırmadı."
            )
        if not isinstance(data, dict):
            return "warn", self._rdt_login_hint()
        cookies = data.get("cookies")
        if not isinstance(cookies, dict) or not cookies.get("reddit_session"):
            return "warn", self._rdt_login_hint()

        saved_at = data.get("saved_at")
        if isinstance(saved_at, (int, float)) and (
            time.time() - saved_at > _CREDENTIAL_TTL_SECONDS
        ):
            return "warn", (
                "rdt-cli kurulu, kayıtlı Cookie 7 günden eski; Doctor upstream aracın "
                "tarayıcıyı otomatik okumasına veya dosyayı yenilemesine izin vermez, "
                "Cookie-Editor ile elle güncelle."
            )
        return "warn", (
            "rdt-cli kurulu ve açıkça kaydedilmiş bir Reddit Cookie'si bulundu; Doctor, "
            "upstream aracın tarayıcı Cookie'lerini otomatik yenilemesini önlemek için "
            "`rdt status` çalıştırmaz, bu yüzden canlı doğrulanmadı."
        )

    @staticmethod
    def _rdt_login_hint():
        return (
            "rdt-cli kurulu ama kullanılabilir açık bir Cookie yok. Cookie-Editor kullan:\n"
            "  1. Chrome Web Mağazası'ndan Cookie-Editor eklentisini kur:\n"
            "     https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm\n"
            "  2. Tarayıcıda reddit.com'u aç (giriş yaptığından emin ol)\n"
            "  3. Cookie-Editor simgesine tıkla, `reddit_session` değerini bul ve Value'yu kopyala\n"
            f"  4. Aşağıdaki içeriği {_CREDENTIAL_FILE} dosyasına yaz:\n"
            '     {"cookies": {"reddit_session": "<Value yapıştır>"}, '
            '"source": "manual", "username": "<kullanıcı adın>", '
            '"modhash": null, "saved_at": 0, "last_verified_at": null}\n\n'
            "Doctor, tarayıcıyı otomatik okuyup dosya yazan `rdt status` komutunu çalıştırmaz."
        )
