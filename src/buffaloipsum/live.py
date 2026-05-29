"""LLM-backed buffalo generation.

Each call to `word()` issues one network request to a large language model
and returns the resulting string. `words(n)` issues `n` such requests.

Requires the 'anthropic' package and an ANTHROPIC_API_KEY env var (or an
explicit api_key argument):

    pip install 'buffaloipsum[live]'
    export ANTHROPIC_API_KEY=sk-ant-...

Usage:

    from buffaloipsum import live
    live.word()       # -> "buffalo"
    live.words(5)     # -> ["buffalo", "buffalo", "buffalo", "buffalo", "buffalo"]
"""

from __future__ import annotations

import sys
import time
from typing import Any, List, Optional

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

_SYSTEM = (
    "Respond with exactly the word \"buffalo\" in lowercase, with no "
    "punctuation, no quotes, no preamble, no farewell, and no explanation. "
    "Just the seven letters: buffalo."
)

_USER = "Generate one buffalo."


def _make_client(api_key: Optional[str]) -> Any:
    try:
        from anthropic import Anthropic
    except ImportError as e:
        raise ImportError(
            "buffaloipsum.live requires the 'anthropic' package. "
            "Install with: pip install 'buffaloipsum[live]'"
        ) from e
    return Anthropic(api_key=api_key) if api_key else Anthropic()


def _normalize(raw: str) -> str:
    cleaned = raw.strip().strip("'\"`.!?,;: ").lower()
    if not cleaned:
        return "buffalo"
    result = cleaned.split()[0]
    if result != "buffalo":
        _vlog(f"warning: unexpected LLM response {raw!r} -> {result!r}")
    return result


def _vlog(msg: str) -> None:
    print(f"[buffaloipsum.live] {msg}", file=sys.stderr)


def word(
    *,
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
    client: Optional[Any] = None,
    verbose: bool = False,
) -> str:
    """Generate the word 'buffalo' via a network round-trip to Claude."""
    if client is None:
        client = _make_client(api_key)
    if verbose:
        _vlog(f"request model={model} user={_USER!r}")
    start = time.perf_counter()
    response = client.messages.create(
        model=model,
        max_tokens=10,
        system=_SYSTEM,
        messages=[{"role": "user", "content": _USER}],
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    raw = response.content[0].text
    normalized = _normalize(raw)
    if verbose:
        usage = getattr(response, "usage", None)
        usage_str = f" usage={usage}" if usage is not None else ""
        _vlog(
            f"response raw={raw!r} -> {normalized!r} "
            f"elapsed={elapsed_ms:.1f}ms{usage_str}"
        )
    return normalized


def words(
    count: int = 5,
    *,
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
    client: Optional[Any] = None,
    verbose: bool = False,
) -> List[str]:
    """Generate `count` buffalos via `count` separate API calls."""
    if count < 0:
        raise ValueError("count must be non-negative")
    if count == 0:
        return []
    if client is None:
        client = _make_client(api_key)
    if verbose:
        _vlog(f"requesting {count} buffalos via {count} API calls")
    return [
        word(model=model, client=client, verbose=verbose) for _ in range(count)
    ]
