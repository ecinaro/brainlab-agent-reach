# CLAUDE.md

## Project
Agent Reach — Python CLI + library that gives AI agents read/search access to 15 internet platforms.
Positioning: installer + doctor + config tool. NOT a wrapper — after install, agents call upstream tools directly.
Repo: github.com/ecinaro/brainlab-agent-reach — Turkish-localized fork of
[Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) (upstream credit stays in README/CLI).
License: MIT | Version: 1.5.0

Fork specifics:
- User-facing CLI/doctor/channel text is Turkish. Commands, flags, paths, env vars and package names stay untranslated.
- `agent_reach/skill/SKILL.md` is Turkish (default); `SKILL_en.md` / `SKILL_zh.md` are picked by
  `AGENT_REACH_LANG` / `LC_ALL` / `LC_MESSAGES` / `LANG` (`en*` / `zh*`), falling back to `SKILL.md`.
- OpenCLI (user's real Chrome session) is the general fallback for sites Jina Reader cannot read
  (login walls, Cloudflare, JS-only). The `web` channel lists it as a second backend but its status
  always comes from Jina Reader (stays zero-config); see `skill/references/opencli-fallback.md`.
- Chinese text left in code is intentional only when matched against remote content, sent as a model
  prompt for Chinese audio, or kept as a legacy backend alias (`Channel.backend_aliases`).

## Commands
- `pip install -e .` — Dev install
- `pytest tests/ -v` — All tests
- `pytest tests/test_cli.py -v` — CLI tests only
- `bash test.sh` — Full integration test (creates venv, installs, runs doctor + channel tests)
- `python -m agent_reach.cli doctor` — Run diagnostics
- `python -m agent_reach.cli install --env=auto` — Auto-configure

## Structure
- `agent_reach/cli.py` — CLI entry point (argparse), installers, skill install
- `agent_reach/core.py` — `AgentReach` facade (doctor/health check only)
- `agent_reach/config.py` — Config management (YAML, env vars)
- `agent_reach/doctor.py` — Diagnostics engine
- `agent_reach/backends/opencli.py` — Side-effect-free OpenCLI probe (`opencli_status`, `opencli_summary`)
- `agent_reach/channels/` — One file per platform (twitter.py, reddit.py, youtube.py, web.py, etc.)
- `agent_reach/channels/base.py` — Base `Channel` class (all channels inherit from this)
- `agent_reach/integrations/mcp_server.py` — MCP server integration
- `agent_reach/skill/` — Agent skill files (SKILL.md tr, SKILL_en.md, SKILL_zh.md, references/)
- `agent_reach/guides/` — Setup guides
- `tests/` — pytest tests
- `config/mcporter.json` — MCP tool config

## Conventions
- Python 3.10+ with type hints
- Each channel is a single file in `channels/`, inherits from `Channel`
- Channel contract: set `name`, `description`, `backends`, `tier`; implement `can_handle(url)` and
  `check(config)` (returns `(status, message)` and sets `active_backend`). Channels do not read or
  search content — agents call the upstream tools directly (some channels keep small helper methods).
- Health checks must never trigger side effects (no `opencli doctor`, no upstream login/status commands
  that read browser cookies)
- Use `loguru` for logging, `rich` for CLI output
- Commit format: `type(scope): message` (one commit = one thing)
- All upstream tool calls go through public API/CLI, never hack internals

## Rules
- NEVER modify upstream open source projects' source code
- Agent Reach is a "glue layer" — only route and call, don't reimagine
- Version in THREE places must match: `pyproject.toml`, `__init__.py`, `tests/test_cli.py`
- Always new branch for changes, PR to main, never push to main directly
- Run `pytest tests/ -v` before committing — all tests must pass
- Cookie-based auth (Twitter, XHS): use Cookie-Editor export method only, no QR scan
- XHS login: Cookie-Editor browser export only (QR will hang)
- Tests that assert user-facing text must match the current Turkish strings in code/docs
