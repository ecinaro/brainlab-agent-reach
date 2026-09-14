# -*- coding: utf-8 -*-
"""Xiaoyuzhou Podcast — transcribe podcasts via Groq Whisper API."""

import os

from agent_reach.config import Config
from agent_reach.probe import probe_command

from .base import Channel


class XiaoyuzhouChannel(Channel):
    name = "xiaoyuzhou"
    description = "Xiaoyuzhou podcast'lerini yazıya dökme"
    backends = ["groq-whisper", "ffmpeg"]
    tier = 1

    def can_handle(self, url: str) -> bool:
        from agent_reach.utils.url import host_matches

        return host_matches(url, "xiaoyuzhoufm.com")

    def check(self, config=None):
        self.active_backend = None

        # Check ffmpeg — really execute it: a stale pip-installed ffmpeg shim
        # passes shutil.which() but cannot run
        probe = probe_command("ffmpeg", ["-version"], timeout=10, package="ffmpeg")
        if probe.status == "missing":
            return "off", (
                "ffmpeg gerekli (ses dönüştürme ve bölme). Kurulum:\n"
                "  Ubuntu/Debian: apt install -y ffmpeg\n"
                "  macOS: brew install ffmpeg"
            )
        if not probe.ok:
            return "error", (
                "ffmpeg çalıştırılamıyor, yeniden kur: brew install ffmpeg (macOS) / apt install ffmpeg (Linux)"
            )

        # Check script exists
        script = os.path.expanduser("~/.agent-reach/tools/xiaoyuzhou/transcribe.sh")
        if not os.path.isfile(script):
            return "off", (
                "Transkripsiyon betiği kurulu değil. Çalıştır:\n"
                "  agent-reach install --env=auto --system --channels=xiaoyuzhou\n"
                "  veya transcribe.sh dosyasını elle ~/.agent-reach/tools/xiaoyuzhou/ içine kopyala"
            )

        # Check GROQ_API_KEY — prefer env var, fall back to Agent Reach config
        has_key = bool(os.environ.get("GROQ_API_KEY"))
        if not has_key:
            try:
                cfg = config if config is not None else Config()
                has_key = bool(cfg.get("groq_api_key"))
            except Exception:
                has_key = False
        if not has_key:
            return "warn", (
                "Groq API Key yapılandırması gerekli (ücretsiz). Adımlar:\n"
                "  1. https://console.groq.com adresinde kayıt ol\n"
                "  2. Çalıştır: agent-reach configure groq-key (gizli giriş)"
            )

        self.active_backend = "groq-whisper"
        return "ok", "Tamamen kullanılabilir (podcast indirme + Whisper transkripsiyonu)"
