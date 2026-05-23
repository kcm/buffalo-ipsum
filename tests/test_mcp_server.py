"""Tests for the MCP server tools.

Skipped automatically if the optional 'mcp' package is not installed.
The tools are tested as plain Python functions; the FastMCP transport layer
is the library's responsibility, not ours.
"""

from __future__ import annotations

import pytest

mcp_pkg = pytest.importorskip("mcp")

from buffaloipsum import FAMOUS_SENTENCE, mcp_server


def test_generate_words_default():
    out = mcp_server.generate_words()
    assert out.split() == ["buffalo"] * 5


def test_generate_words_count():
    assert mcp_server.generate_words(0) == ""
    assert mcp_server.generate_words(3).split() == ["buffalo"] * 3


def test_generate_sentences_count():
    out = mcp_server.generate_sentences(4)
    assert len(out.splitlines()) == 4
    for line in out.splitlines():
        assert line.startswith("Buffalo ")
        assert line.endswith(".")


def test_generate_sentences_famous():
    out = mcp_server.generate_sentences(2, famous=True)
    assert out.splitlines() == [FAMOUS_SENTENCE + "."] * 2


def test_generate_paragraphs_separator():
    out = mcp_server.generate_paragraphs(3)
    assert out.count("\n\n") == 2


def test_generate_ascii_art_shape():
    out = mcp_server.generate_ascii_art(cols=2, rows=1, gap=4)
    lines = out.splitlines()
    # Each row of the grid is one full buffalo tall.
    from buffaloipsum import BUFFALO_ART
    assert len(lines) == len(BUFFALO_ART)


def test_famous_sentence_constant():
    assert mcp_server.famous_sentence() == FAMOUS_SENTENCE + "."


def test_server_has_expected_tools():
    """Sanity check: the FastMCP instance lists the tools we registered."""
    # The internal layout has shifted across mcp SDK versions; try a few.
    server = mcp_server.mcp
    registered = set()
    for attr in ("_tool_manager", "_tools"):
        target = getattr(server, attr, None)
        if target is None:
            continue
        tools = getattr(target, "_tools", target)
        if isinstance(tools, dict):
            registered.update(tools.keys())
            break
    expected = {
        "generate_words",
        "generate_sentences",
        "generate_paragraphs",
        "generate_ascii_art",
        "famous_sentence",
    }
    # If we couldn't introspect, at least confirm the callables exist on the module.
    if not registered:
        for name in expected:
            assert callable(getattr(mcp_server, name)), name
    else:
        assert expected <= registered, f"missing: {expected - registered}"
