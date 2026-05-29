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
    """Sanity check: the expected tool callables exist on the module."""
    expected = {
        "generate_words",
        "generate_sentences",
        "generate_paragraphs",
        "generate_ascii_art",
        "famous_sentence",
    }
    for name in expected:
        assert callable(getattr(mcp_server, name)), name


def test_generate_words_invalid():
    result = mcp_server.generate_words(-1)
    assert result.startswith("Error:")


def test_generate_sentences_invalid():
    result = mcp_server.generate_sentences(-1)
    assert result.startswith("Error:")


def test_generate_paragraphs_invalid():
    result = mcp_server.generate_paragraphs(-1)
    assert result.startswith("Error:")


def test_generate_ascii_art_invalid():
    result = mcp_server.generate_ascii_art(cols=0)
    assert result.startswith("Error:")
