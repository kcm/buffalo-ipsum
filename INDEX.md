# Project index

| Path | Purpose |
|------|---------|
| [pyproject.toml](pyproject.toml) | Package metadata, dependencies, build config, CLI entry point |
| [CHANGELOG.md](CHANGELOG.md) | Release notes (Keep a Changelog format) |
| [CLAUDE.md](CLAUDE.md) | Project context for Claude Code |
| [src/buffaloipsum/__init__.py](src/buffaloipsum/__init__.py) | Static API: word/sentence/paragraph/text generators, `BUFFALO_ART`, `ascii_art()` |
| [src/buffaloipsum/__main__.py](src/buffaloipsum/__main__.py) | CLI entry point (`buffalo-ipsum`) |
| [src/buffaloipsum/live.py](src/buffaloipsum/live.py) | Optional `live.word()` / `live.words(n)` that fetch each buffalo via the Anthropic API |
| [src/buffaloipsum/mcp_server.py](src/buffaloipsum/mcp_server.py) | Optional MCP server (`buffalo-ipsum-mcp`) exposing the generators as MCP tools |
| [tests/test_buffaloipsum.py](tests/test_buffaloipsum.py) | Tests for the static API and ASCII art |
| [tests/test_live.py](tests/test_live.py) | Tests for the live module (uses a fake client; no network) |
| [tests/test_mcp_server.py](tests/test_mcp_server.py) | Tests for the MCP server tools (skipped if `mcp` not installed) |
