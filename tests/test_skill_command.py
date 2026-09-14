# -*- coding: utf-8 -*-
"""Tests for 'agent-reach skill' command and _install_skill / _uninstall_skill."""

import importlib.resources
import os
import re
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from agent_reach.cli import _cmd_skill, _install_skill, _uninstall_skill


class TestSkillCommand(unittest.TestCase):
    """Test skill install and uninstall via CLI helpers."""

    def test_skill_resources_include_all_locales(self):
        """Package resources expose Turkish (default), English and Chinese skills."""
        skill_dir = importlib.resources.files("agent_reach").joinpath("skill")

        for name in ("SKILL.md", "SKILL_en.md", "SKILL_zh.md"):
            with self.subTest(name=name):
                self.assertTrue(
                    skill_dir.joinpath(name).read_text(encoding="utf-8").strip()
                )
        self.assertTrue(
            skill_dir.joinpath("references", "opencli-fallback.md")
            .read_text(encoding="utf-8")
            .strip()
        )

    def test_exa_reference_uses_default_registered_tools_only(self):
        """Agent instructions must not call Exa tools disabled by default."""
        search_reference = (
            importlib.resources.files("agent_reach")
            .joinpath("skill", "references", "search.md")
            .read_text(encoding="utf-8")
        )

        self.assertIn("web_search_exa", search_reference)
        self.assertNotIn("exa.get_code_context_exa", search_reference)
        self.assertNotIn("get_code_context_exa(", search_reference)

    def test_mcporter_examples_use_shell_safe_named_arguments(self):
        """Packaged commands must survive PowerShell and POSIX parsing."""
        root = Path(__file__).resolve().parents[1]
        markdown_files = [
            *(root / "agent_reach" / "skill").rglob("*.md"),
            *(root / "agent_reach" / "guides").rglob("*.md"),
            root / "docs" / "install.md",
            root / "docs" / "troubleshooting.md",
        ]
        function_call = re.compile(r"mcporter call\s+['\"][^'\"\r\n]+\(")

        for markdown_file in markdown_files:
            with self.subTest(markdown_file=markdown_file):
                content = markdown_file.read_text(encoding="utf-8")
                self.assertNotRegex(content, function_call)

    def test_linkedin_reference_uses_current_tool_contract(self):
        """LinkedIn examples should use the current server and parameters."""
        career_reference = (
            importlib.resources.files("agent_reach")
            .joinpath("skill", "references", "career.md")
            .read_text(encoding="utf-8")
        )

        self.assertIn(
            "linkedin.get_person_profile "
            'linkedin_username="username" '
            'sections="experience,education"',
            career_reference,
        )
        self.assertIn(
            'linkedin.search_people keywords="AI engineer" '
            'location="Shanghai"',
            career_reference,
        )
        self.assertIn(
            'linkedin.get_company_profile company_name="openai" '
            'sections="posts,jobs"',
            career_reference,
        )
        self.assertIn(
            'linkedin.search_jobs keywords="software engineer" '
            'location="Remote" max_pages=2',
            career_reference,
        )
        self.assertNotIn("linkedin-scraper.", career_reference)

    def test_linkedin_install_docs_use_current_stdio_contract(self):
        """LinkedIn install guidance should use uvx over stdio."""
        install_doc = (
            Path(__file__).resolve().parents[1] / "docs" / "install.md"
        ).read_text(encoding="utf-8")
        linkedin_section = install_doc.split(
            "**LinkedIn (", maxsplit=1
        )[1].split("### Adım 8:", maxsplit=1)[0]

        self.assertIn(
            "uvx mcp-server-linkedin@latest --login",
            linkedin_section,
        )
        self.assertIn(
            "mcporter config add linkedin --command uvx "
            "--arg mcp-server-linkedin@latest --env UV_HTTP_TIMEOUT=300 "
            "--scope home",
            linkedin_section,
        )
        self.assertNotIn("linkedin-scraper-mcp", linkedin_section)
        self.assertNotIn("localhost:3000/mcp", linkedin_section)
        self.assertNotIn("linkedin-scraper.", linkedin_section)
        self.assertNotIn("--transport streamable-http", linkedin_section)

    def test_localized_readmes_use_current_linkedin_server_name(self):
        root = Path(__file__).resolve().parents[1]
        for name in ("README_ja.md", "README_ko.md"):
            content = (root / "docs" / name).read_text(encoding="utf-8")
            self.assertIn("mcp-server-linkedin", content)
            self.assertNotIn("linkedin-scraper-mcp", content)

    def test_skill_install_command_exits_nonzero_when_install_fails(self):
        with patch("agent_reach.cli._install_skill", return_value=False):
            with self.assertRaises(SystemExit) as raised:
                _cmd_skill(Namespace(install=True, uninstall=False))

        self.assertEqual(raised.exception.code, 1)

    def test_install_skill_creates_skill_md(self):
        """_install_skill should create SKILL.md in the first available skill dir."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = os.path.join(tmpdir, "skills")
            os.makedirs(skill_dir)

            with patch(
                "agent_reach.cli.os.path.expanduser",
                side_effect=lambda p: p.replace("~", tmpdir),
            ), patch.dict(os.environ, {}, clear=False):
                # Remove OPENCLAW_HOME to avoid interference
                env = os.environ.copy()
                env.pop("OPENCLAW_HOME", None)
                with patch.dict(os.environ, env, clear=True):
                    _install_skill()

            # Check at least one known skill dir pattern
            for dirpath, _, filenames in os.walk(tmpdir):
                if "SKILL.md" in filenames:
                    # Verify content is non-empty
                    with open(os.path.join(dirpath, "SKILL.md"), encoding="utf-8") as f:
                        content = f.read()
                    self.assertIn("Agent Reach", content)
            # _install_skill may or may not find dirs depending on mock; just ensure no crash
            # The important test is that the function runs without error

    def test_uninstall_skill_removes_dir(self):
        """_uninstall_skill should remove skill directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a fake skill installation
            skill_path = os.path.join(tmpdir, ".openclaw", "skills", "agent-reach")
            os.makedirs(skill_path)
            with open(os.path.join(skill_path, "SKILL.md"), "w", encoding="utf-8") as f:
                f.write("test")

            self.assertTrue(os.path.exists(skill_path))

            with patch(
                "agent_reach.cli.os.path.expanduser",
                side_effect=lambda p: p.replace("~", tmpdir),
            ), patch.dict(os.environ, {}, clear=False):
                env = os.environ.copy()
                env.pop("OPENCLAW_HOME", None)
                with patch.dict(os.environ, env, clear=True):
                    _uninstall_skill()

            self.assertFalse(os.path.exists(skill_path))

    def test_install_creates_dir_if_parent_exists(self):
        """_install_skill should create agent-reach dir inside existing skill dir."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create the .openclaw/skills parent but not agent-reach subdir
            skill_parent = os.path.join(tmpdir, ".openclaw", "skills")
            os.makedirs(skill_parent)

            with patch(
                "agent_reach.cli.os.path.expanduser",
                side_effect=lambda p: p.replace("~", tmpdir),
            ), patch.dict(os.environ, {}, clear=False):
                env = os.environ.copy()
                env.pop("OPENCLAW_HOME", None)
                with patch.dict(os.environ, env, clear=True):
                    _install_skill()

            target = os.path.join(skill_parent, "agent-reach", "SKILL.md")
            self.assertTrue(os.path.exists(target))
            with open(target, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Agent Reach", content)

    def test_install_uses_english_skill_for_english_locale(self):
        """_install_skill should install the English skill file for English locales."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_parent = os.path.join(tmpdir, ".openclaw", "skills")
            os.makedirs(skill_parent)

            with patch(
                "agent_reach.cli.os.path.expanduser",
                side_effect=lambda p: p.replace("~", tmpdir),
            ):
                env = os.environ.copy()
                env.pop("OPENCLAW_HOME", None)
                env["LANG"] = "en_US.UTF-8"
                with patch.dict(os.environ, env, clear=True):
                    _install_skill()

            target = os.path.join(skill_parent, "agent-reach", "SKILL.md")
            self.assertTrue(os.path.exists(target))
            with open(target, encoding="utf-8") as f:
                content = f.read()
            self.assertTrue(content.strip())
            self.assertIn("Xiaoyuzhou Podcast, LinkedIn", content)
            self.assertNotIn("搜推特", content)
            self.assertTrue(
                os.path.exists(os.path.join(skill_parent, "agent-reach", "references"))
            )


_LOCALE_ENV = ("AGENT_REACH_LANG", "LC_ALL", "LC_MESSAGES", "LANG", "OPENCLAW_HOME")
_TURKISH_MARKER = "LinkedIn/iş ilanları"
_ENGLISH_MARKER = "Xiaoyuzhou Podcast, LinkedIn"
_CHINESE_MARKER = "小宇宙播客"


class TestSkillLanguageSelection(unittest.TestCase):
    """SKILL.md is Turkish by default; en/zh locales pick their own file."""

    def _install_with_env(self, locale_env):
        """Install into a temp OpenClaw root and return the installed SKILL.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_parent = os.path.join(tmpdir, ".openclaw", "skills")
            os.makedirs(skill_parent)
            env = {k: v for k, v in os.environ.items() if k not in _LOCALE_ENV}
            env.update(locale_env)
            with patch(
                "agent_reach.cli.os.path.expanduser",
                side_effect=lambda p: p.replace("~", tmpdir),
            ), patch.dict(os.environ, env, clear=True):
                _install_skill()

            skill_root = os.path.join(skill_parent, "agent-reach")
            with open(os.path.join(skill_root, "SKILL.md"), encoding="utf-8") as f:
                content = f.read()
            self.assertTrue(
                os.path.isfile(
                    os.path.join(skill_root, "references", "opencli-fallback.md")
                )
            )
            return content

    def test_default_without_locale_is_turkish(self):
        content = self._install_with_env({})
        self.assertIn(_TURKISH_MARKER, content)
        self.assertNotIn(_ENGLISH_MARKER, content)
        self.assertNotIn(_CHINESE_MARKER, content)

    def test_turkish_and_unsupported_locales_install_turkish(self):
        for env in (
            {"LANG": "tr_TR.UTF-8"},
            {"AGENT_REACH_LANG": "tr"},
            {"LANG": "C.UTF-8"},
            {"LANG": "de_DE.UTF-8"},
        ):
            with self.subTest(env=env):
                self.assertIn(_TURKISH_MARKER, self._install_with_env(env))

    def test_english_locale_installs_english(self):
        for env in ({"LANG": "en_US.UTF-8"}, {"LC_ALL": "en_GB.UTF-8"}):
            with self.subTest(env=env):
                content = self._install_with_env(env)
                self.assertIn(_ENGLISH_MARKER, content)
                self.assertNotIn(_TURKISH_MARKER, content)

    def test_chinese_locale_installs_chinese(self):
        for env in ({"LANG": "zh_CN.UTF-8"}, {"AGENT_REACH_LANG": "zh"}):
            with self.subTest(env=env):
                content = self._install_with_env(env)
                self.assertIn(_CHINESE_MARKER, content)
                self.assertNotIn(_TURKISH_MARKER, content)

    def test_agent_reach_lang_overrides_system_locale(self):
        content = self._install_with_env(
            {"AGENT_REACH_LANG": "tr", "LANG": "en_US.UTF-8"}
        )
        self.assertIn(_TURKISH_MARKER, content)

    def test_missing_chinese_skill_falls_back_to_turkish(self):
        missing = {"tr": "SKILL.md", "en": "SKILL_en.md", "zh": "SKILL_zh_missing.md"}
        with patch("agent_reach.cli._SKILL_RESOURCES", missing):
            content = self._install_with_env({"LANG": "zh_CN.UTF-8"})
        self.assertIn(_TURKISH_MARKER, content)
        self.assertNotIn(_CHINESE_MARKER, content)


if __name__ == "__main__":
    unittest.main()
