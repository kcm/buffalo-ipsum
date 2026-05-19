# buffalo-ipsum

Filler text generator composed entirely of the word "buffalo".

```
Buffalo buffalo Buffalo buffalo buffalo buffalo buffalo buffalo buffalo buffalo.
Buffalo buffalo buffalo buffalo buffalo. Buffalo buffalo Buffalo buffalo buffalo
buffalo buffalo buffalo buffalo buffalo buffalo buffalo.
```

Inspired by the [linguistically valid English sentence](https://en.wikipedia.org/wiki/Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo) that uses "buffalo" eight times. This package brings that energy to your placeholder text needs.

## Install

```bash
pip install buffalo-ipsum
```

## Usage

**CLI:**

```bash
buffalo-ipsum                        # 3 paragraphs (default)
buffalo-ipsum -t sentences -n 5      # 5 sentences
buffalo-ipsum -t words -n 10         # 10 words
buffalo-ipsum --famous               # the canonical 8-buffalo sentence
buffalo-ipsum -t art --cols 3        # ASCII art herd
```

**Python API:**

```python
import buffaloipsum

buffaloipsum.word()                  # "buffalo"
buffaloipsum.words(5)                # ["buffalo", "buffalo", ...]
buffaloipsum.sentence()              # "Buffalo buffalo buffalo buffalo buffalo."
buffaloipsum.sentence(famous=True)   # "Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo."
buffaloipsum.paragraph()
buffaloipsum.text(3)
buffaloipsum.ascii_art(cols=2, rows=1)
```

## Modes

### Static mode (default)

Generates buffalo text locally with no dependencies and no network calls. All randomness is seeded from Python's `random` module; pass `seed=N` for reproducible output.

### Live mode

Each word is fetched via a real Claude API call. The result is always "buffalo" — the point is that an LLM confirmed it.

```bash
pip install 'buffalo-ipsum[live]'
export ANTHROPIC_API_KEY=sk-ant-...
buffalo-ipsum --live -t words -n 3
```

```python
from buffaloipsum import live

live.word()     # -> "buffalo"  (one API call)
live.words(5)   # -> ["buffalo", ...] (five API calls)
```

Uses `claude-haiku-4-5-20251001` by default. Override with `--model` on the CLI or `model=` in Python.

## Famous sentence

> **Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo.**

A grammatically valid English sentence. "Buffalo" serves simultaneously as a proper noun (Buffalo, NY), a common noun (the animal), and a verb (to bully). `--famous` / `famous=True` emits it verbatim.

## License

MIT
