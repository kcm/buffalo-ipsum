"""Tests for the CLI entry point (__main__.py)."""

from __future__ import annotations

import pytest

import buffaloipsum as bi
from buffaloipsum.__main__ import main


def test_cli_words(capsys):
    assert main(["--type", "words", "--count", "3"]) == 0
    assert capsys.readouterr().out.strip() == "buffalo buffalo buffalo"


def test_cli_sentences(capsys):
    assert main(["--type", "sentences", "--count", "2", "--seed", "0"]) == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 2
    assert all(line.endswith(".") for line in lines)


def test_cli_paragraphs_is_default(capsys):
    assert main(["--count", "2", "--seed", "1"]) == 0
    assert "\n\n" in capsys.readouterr().out


def test_cli_art_alias(capsys):
    assert main(["--type", "art"]) == 0
    assert len(capsys.readouterr().out.splitlines()) == len(bi.BUFFALO_ART)


def test_cli_asciiart_grid(capsys):
    assert main(["--type", "asciiart", "--cols", "2", "--rows", "1"]) == 0
    assert len(capsys.readouterr().out.splitlines()) == len(bi.BUFFALO_ART)


def test_cli_famous(capsys):
    assert main(["--type", "paragraphs", "--count", "1", "--famous"]) == 0
    assert "Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo." in capsys.readouterr().out


def test_cli_seed_reproducible(capsys):
    assert main(["--type", "sentences", "--count", "3", "--seed", "99"]) == 0
    out1 = capsys.readouterr().out
    assert main(["--type", "sentences", "--count", "3", "--seed", "99"]) == 0
    out2 = capsys.readouterr().out
    assert out1 == out2


def test_cli_live_requires_words():
    with pytest.raises(SystemExit) as exc:
        main(["--live", "--type", "sentences"])
    assert exc.value.code != 0
