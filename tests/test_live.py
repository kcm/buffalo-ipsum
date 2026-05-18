"""Tests for the live LLM-backed mode. Uses a fake client — never hits the network."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pytest

from buffaloipsum import live


@dataclass
class _FakeBlock:
    text: str


@dataclass
class _FakeResponse:
    content: List[_FakeBlock]


class _FakeMessages:
    def __init__(self, replies: List[str]):
        self._replies = list(replies)
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        reply = self._replies.pop(0) if self._replies else "buffalo"
        return _FakeResponse(content=[_FakeBlock(text=reply)])


class _FakeClient:
    def __init__(self, replies: List[str] | None = None):
        self.messages = _FakeMessages(replies or [])


def test_word_clean_response():
    client = _FakeClient(["buffalo"])
    assert live.word(client=client) == "buffalo"
    assert len(client.messages.calls) == 1


def test_word_normalizes_punctuation_and_case():
    client = _FakeClient(['  "Buffalo!"  '])
    assert live.word(client=client) == "buffalo"


def test_word_handles_extra_words():
    client = _FakeClient(["buffalo buffalo buffalo"])
    assert live.word(client=client) == "buffalo"


def test_word_handles_empty_response():
    client = _FakeClient([""])
    assert live.word(client=client) == "buffalo"


def test_words_makes_one_call_per_buffalo():
    client = _FakeClient(["buffalo"] * 5)
    out = live.words(5, client=client)
    assert out == ["buffalo"] * 5
    assert len(client.messages.calls) == 5


def test_words_zero_skips_calls():
    client = _FakeClient([])
    assert live.words(0, client=client) == []
    assert client.messages.calls == []


def test_words_rejects_negative():
    with pytest.raises(ValueError):
        live.words(-1, client=_FakeClient())


def test_model_is_passed_through():
    client = _FakeClient(["buffalo"])
    live.word(client=client, model="claude-opus-4-7")
    assert client.messages.calls[0]["model"] == "claude-opus-4-7"


def test_verbose_prints_to_stderr(capsys):
    client = _FakeClient(["buffalo"])
    live.word(client=client, verbose=True)
    err = capsys.readouterr().err
    assert "[buffaloipsum.live]" in err
    assert "request" in err
    assert "response" in err


def test_verbose_quiet_by_default(capsys):
    client = _FakeClient(["buffalo"])
    live.word(client=client)
    assert capsys.readouterr().err == ""
