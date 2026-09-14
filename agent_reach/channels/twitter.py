# -*- coding: utf-8 -*-
"""Twitter/X — check if twitter-cli or bird CLI is available."""

import os
import shutil

from agent_reach.utils.url import host_matches

from .base import Channel


def twitter_cli_child_env(config=None) -> dict[str, str]:
    """Return saved credentials missing from the current process environment.

    The returned mapping is meant for a single child process.  Existing shell
    variables remain authoritative and ``os.environ`` is never mutated.
    """
    if config is None:
        return {}

    child_env = {}
    for env_name, config_key in (
        ("TWITTER_AUTH_TOKEN", "twitter_auth_token"),
        ("TWITTER_CT0", "twitter_ct0"),
    ):
        if env_name in os.environ:
            continue
        value = config.get(config_key)
        if value:
            child_env[env_name] = str(value)
    return child_env


class TwitterChannel(Channel):
    name = "twitter"
    description = "Twitter/X gönderileri"
    backends = ["twitter-cli", "OpenCLI", "bird CLI (legacy)"]
    tier = 1

    def can_handle(self, url: str) -> bool:
        return host_matches(url, "x.com", "twitter.com")

    def check(self, config=None):
        """Probe candidates in order; first fully-usable backend wins.

        Same two-pass scheme as other multi-backend channels: collect every
        candidate first, the first ok wins; only without an ok does the first
        warn win -- otherwise an installed-but-logged-out twitter-cli would
        shadow a fully usable OpenCLI later in the list.
        """
        self.active_backend = None
        findings = []

        for backend in self.ordered_backends(config):
            if backend == "twitter-cli":
                result = self._check_twitter_cli(config)
            elif backend == "OpenCLI":
                result = self._check_opencli()
            elif backend == "bird CLI (legacy)":
                result = self._check_bird()
            else:
                continue

            if result is None:
                continue  # not installed -- not a candidate
            findings.append((backend, *result))

        for wanted in ("ok", "warn"):
            for backend, status, message in findings:
                if status == wanted:
                    self.active_backend = backend if status == "ok" else None
                    return status, message

        if findings:  # only broken/timeout candidates left
            return "error", "\n".join(m for _, _, m in findings)

        return "warn", (
            "Twitter CLI kurulu değil. Kurulum:\n"
            "  pipx install twitter-cli\n"
            "veya:\n"
            "  uv tool install twitter-cli"
        )

    def _check_twitter_cli(self, config=None):
        """Inspect explicit credentials without starting twitter-cli.

        Upstream ``twitter status`` automatically reads browser cookies when
        credentials are missing *or invalid*. Doctor cannot disable that
        fallback, so executing it would violate the Cookie-Editor-only policy.
        """
        if not shutil.which("twitter"):
            return None

        child_env = twitter_cli_child_env(config)
        auth_token = os.environ.get("TWITTER_AUTH_TOKEN") or child_env.get(
            "TWITTER_AUTH_TOKEN"
        )
        ct0 = os.environ.get("TWITTER_CT0") or child_env.get("TWITTER_CT0")
        if auth_token and ct0:
            return "warn", (
                "twitter-cli kurulu ve Cookie-Editor kimlik bilgileri yapılandırılmış; "
                "Doctor `twitter status` çalıştırmaz, çünkü upstream araç doğrulama "
                "başarısız olursa tarayıcı Cookie'lerini otomatik okur. Açıkça onay "
                "verdiğinde elle doğrula."
            )
        return "warn", (
            "twitter-cli kurulu ama eksiksiz açık kimlik bilgisi yok. Cookie-Editor ile "
            "x.com'dan dışa aktardıktan sonra çalıştır:\n"
            "  agent-reach configure twitter-cookies\n"
            "Doctor tarayıcı Cookie'lerini otomatik okumaz."
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
                "OpenCLI köprüsü bağlı, ancak Twitter/X giriş durumu ve gerçek komutlar "
                "canlı doğrulanmadı; Doctor platform komutu çalıştırmadığı için kanal "
                "şimdilik kullanılabilir olarak işaretlenmiyor."
            )
        return "warn", st.hint

    def _check_bird(self):
        """Inspect legacy bird credentials without launching browser fallback."""
        for cmd in ("bird", "birdx"):
            if not shutil.which(cmd):
                continue
            if os.environ.get("AUTH_TOKEN") and os.environ.get("CT0"):
                return (
                    "warn",
                    f"{cmd} kurulu ve açık ortam kimlik bilgileri mevcut; Doctor upstream "
                    "aracın tarayıcı Cookie yedeğine düşmesini önlemek için `check` "
                    "çalıştırmaz, canlı doğrulanmadı.",
                )
            return "warn", (
                f"{cmd} kurulu ama açık AUTH_TOKEN/CT0 bulunamadı; "
                "yalnızca Cookie-Editor ile elle dışa aktarılan kimlik bilgilerini kullan."
            )
        return None
