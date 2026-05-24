"""Buffalo ipsum — filler text composed entirely of the word "buffalo".

The "famous" mode emits the canonical grammatically-valid sentence:
    Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo.
See https://en.wikipedia.org/wiki/Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo
"""

from __future__ import annotations

import random
from typing import List, Optional

__all__ = [
    "FAMOUS_SENTENCE",
    "BUFFALO_ART",
    "word",
    "words",
    "sentence",
    "sentences",
    "paragraph",
    "paragraphs",
    "text",
    "ascii_art",
]

__version__ = "0.1.4"

FAMOUS_SENTENCE = "Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo"

_RAW_BUFFALO = """
    \\                  /
     \\                /
      \\              /
       \\,          ,/
        '\\,______,/'
       ,'          '.
      /              \\
     |   o            \\______________
     |                                \\
      \\                               \\____
       \\                                   \\
        '-,------,------,------,------------'
           |      |      |      |            \\,
           |      |      |      |             `~-.
"""


def _build_art() -> tuple[str, ...]:
    lines = _RAW_BUFFALO.strip("\n").splitlines()
    width = max(len(line) for line in lines)
    return tuple(line.ljust(width) for line in lines)


BUFFALO_ART: tuple[str, ...] = _build_art()


def _rng(seed: Optional[int]) -> random.Random:
    return random.Random(seed) if seed is not None else random


def word() -> str:
    return "buffalo"


def words(count: int = 5) -> List[str]:
    if count < 0:
        raise ValueError("count must be non-negative")
    return ["buffalo"] * count


def sentence(
    min_words: int = 4,
    max_words: int = 12,
    *,
    famous: bool = False,
    seed: Optional[int] = None,
) -> str:
    if famous:
        return FAMOUS_SENTENCE + "."
    if min_words < 1:
        raise ValueError("min_words must be at least 1")
    if max_words < min_words:
        raise ValueError("max_words must be >= min_words")
    n = _rng(seed).randint(min_words, max_words)
    parts = ["Buffalo"] + ["buffalo"] * (n - 1)
    return " ".join(parts) + "."


def sentences(
    count: int = 3,
    *,
    famous: bool = False,
    seed: Optional[int] = None,
) -> List[str]:
    if count < 0:
        raise ValueError("count must be non-negative")
    rng = _rng(seed)
    return [
        sentence(famous=famous, seed=rng.randrange(2**32))
        for _ in range(count)
    ]


def paragraph(
    min_sentences: int = 3,
    max_sentences: int = 7,
    *,
    famous: bool = False,
    seed: Optional[int] = None,
) -> str:
    if min_sentences < 1:
        raise ValueError("min_sentences must be at least 1")
    if max_sentences < min_sentences:
        raise ValueError("max_sentences must be >= min_sentences")
    rng = _rng(seed)
    n = rng.randint(min_sentences, max_sentences)
    return " ".join(
        sentence(famous=famous, seed=rng.randrange(2**32)) for _ in range(n)
    )


def paragraphs(
    count: int = 3,
    *,
    famous: bool = False,
    seed: Optional[int] = None,
) -> List[str]:
    if count < 0:
        raise ValueError("count must be non-negative")
    rng = _rng(seed)
    return [
        paragraph(famous=famous, seed=rng.randrange(2**32))
        for _ in range(count)
    ]


def text(
    paragraphs_count: int = 3,
    *,
    famous: bool = False,
    seed: Optional[int] = None,
    separator: str = "\n\n",
) -> str:
    return separator.join(
        paragraphs(paragraphs_count, famous=famous, seed=seed)
    )


def ascii_art(cols: int = 1, rows: int = 1, gap: int = 2) -> str:
    """Render a `cols` x `rows` grid of ASCII-art buffalo.

    `gap` controls both the horizontal spacing (in columns) between
    neighboring buffalo and the vertical spacing (in blank lines)
    between rows. Use gap=0 to butt them up against each other.
    """
    if cols < 1:
        raise ValueError("cols must be at least 1")
    if rows < 1:
        raise ValueError("rows must be at least 1")
    if gap < 0:
        raise ValueError("gap must be non-negative")

    h_spacer = " " * gap
    row_block = "\n".join(h_spacer.join([line] * cols) for line in BUFFALO_ART)
    return ("\n" * (gap + 1)).join([row_block] * rows)
