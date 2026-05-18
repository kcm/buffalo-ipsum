# buffalo-ipsum

Filler-text generator composed entirely of the word "buffalo". Modeled loosely
on npm's hipsteripsum.

## Layout

- `src/buffaloipsum/__init__.py` — static API: words/sentences/paragraphs/text,
  `FAMOUS_SENTENCE`, `BUFFALO_ART`, `ascii_art(cols, rows, gap)`.
- `src/buffaloipsum/__main__.py` — CLI entry point (`buffalo-ipsum`).
- `src/buffaloipsum/live.py` — optional LLM-backed generator (`live.word()`,
  `live.words(n)`). Imports `anthropic` lazily; the package's base install has
  no runtime dependencies.
- `tests/` — pytest suite. `test_live.py` uses a fake client; tests never hit
  the network.

The PyPI distribution is `buffalo-ipsum` (hyphenated). The Python import name
is `buffaloipsum` (Python identifiers cannot contain hyphens). The CLI command
is `buffalo-ipsum`.

## Common commands

```bash
# Setup
python3 -m venv .venv
.venv/bin/pip install -e '.[live]' pytest build twine

# Test
.venv/bin/pytest -q

# Build
rm -rf dist && .venv/bin/python -m build && .venv/bin/twine check dist/*

# Publish (requires PyPI token in TWINE_PASSWORD with TWINE_USERNAME=__token__)
.venv/bin/twine upload dist/*
```

## Conventions

- Version lives in `pyproject.toml` and `src/buffaloipsum/__init__.py:__version__`.
  Bump both when releasing.
- New user-facing features get a line under `## [Unreleased]` in `CHANGELOG.md`.
- The live mode is a real feature, not a gimmick — describe it deadpan in user
  docs and CLI help. No "joke mode" framing.
- The ASCII art lives as a raw triple-quoted string in `__init__.py` and is
  padded to uniform width at import time by `_build_art()`. If you edit it,
  the `test_buffalo_art_uniform_width` test will catch line-length mistakes.
