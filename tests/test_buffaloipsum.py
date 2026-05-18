import re

import pytest

import buffaloipsum as bi


def test_word():
    assert bi.word() == "buffalo"


def test_words():
    assert bi.words(0) == []
    assert bi.words(4) == ["buffalo"] * 4


def test_sentence_shape():
    s = bi.sentence(seed=0)
    assert s.endswith(".")
    assert s.startswith("Buffalo ")
    tokens = s[:-1].split()
    assert tokens[0] == "Buffalo"
    assert all(t == "buffalo" for t in tokens[1:])
    assert 4 <= len(tokens) <= 12


def test_sentence_famous():
    assert bi.sentence(famous=True) == bi.FAMOUS_SENTENCE + "."


def test_sentences_count_and_determinism():
    out_a = bi.sentences(5, seed=42)
    out_b = bi.sentences(5, seed=42)
    assert out_a == out_b
    assert len(out_a) == 5


def test_paragraph_has_multiple_sentences():
    p = bi.paragraph(seed=7)
    assert p.count(".") >= 3


def test_paragraphs_all_buffalo():
    only_buffalo = re.compile(r"^[Bb]uffalo$")
    out = bi.text(2, seed=1)
    for tok in out.replace("\n", " ").replace(".", "").split():
        assert only_buffalo.match(tok), tok


def test_text_separator():
    out = bi.text(3, separator="\n---\n", seed=2)
    assert out.count("\n---\n") == 2


def test_invalid_counts():
    with pytest.raises(ValueError):
        bi.words(-1)
    with pytest.raises(ValueError):
        bi.sentence(min_words=0)
    with pytest.raises(ValueError):
        bi.sentence(min_words=5, max_words=2)


def test_buffalo_art_uniform_width():
    widths = {len(line) for line in bi.BUFFALO_ART}
    assert len(widths) == 1, f"art lines have mismatched widths: {widths}"


def test_ascii_art_single():
    art = bi.ascii_art()
    lines = art.splitlines()
    assert len(lines) == len(bi.BUFFALO_ART)
    assert lines[0] == bi.BUFFALO_ART[0]


def test_ascii_art_tile_grid():
    cols, rows, gap = 3, 2, 2
    art = bi.ascii_art(cols=cols, rows=rows, gap=gap)
    lines = art.splitlines()
    art_h = len(bi.BUFFALO_ART)
    art_w = len(bi.BUFFALO_ART[0])

    expected_total_lines = rows * art_h + (rows - 1) * gap
    assert len(lines) == expected_total_lines

    expected_width = cols * art_w + (cols - 1) * gap
    first_row_top = lines[0]
    assert len(first_row_top) == expected_width


def test_ascii_art_gap_zero_butts_rows():
    art = bi.ascii_art(cols=2, rows=3, gap=0)
    lines = art.splitlines()
    assert len(lines) == 3 * len(bi.BUFFALO_ART)


def test_ascii_art_invalid():
    with pytest.raises(ValueError):
        bi.ascii_art(cols=0)
    with pytest.raises(ValueError):
        bi.ascii_art(rows=0)
    with pytest.raises(ValueError):
        bi.ascii_art(gap=-1)
