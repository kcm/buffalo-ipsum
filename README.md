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

`--famous` / `famous=True` emits the canonical 8-buffalo sentence — *Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo.* — verbatim. It's grammatically valid English; "Buffalo" serves as a proper noun (Buffalo, NY), a common noun (the animal), and a verb (to bully) all at once.

## Default mode

Generates buffalo text locally with no dependencies and no network calls. All randomness is seeded from Python's `random` module; pass `seed=N` for reproducible output.

## AI Native

Two integrations with the modern AI stack: a live mode that fetches each buffalo from a large language model, and an MCP server that exposes the generators as tools for autonomous agents.

### Live mode

Routes every word through the Anthropic API. The output is always `"buffalo"`, with each token validated end-to-end by a frontier model.

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

Uses `claude-haiku-4-5-20251001` by default. Override with `--model` on the CLI or `model=` in Python. Pass `verbose=True` (or `-v` on the CLI) to log requests, responses, and token usage to stderr.

### MCP server

Exposes the buffalo-ipsum generators as Model Context Protocol tools so any MCP-compatible client — Claude Code, IDE assistants, custom agents — can invoke them.

```bash
pip install 'buffalo-ipsum[mcp]'
```

Wire it into Claude Code's `settings.json`:

```json
{
  "mcpServers": {
    "buffalo-ipsum": {
      "command": "buffalo-ipsum-mcp"
    }
  }
}
```

Tools exposed:

| Tool | Description |
|------|-------------|
| `generate_words(count)` | Space-separated buffalos. |
| `generate_sentences(count, famous)` | One sentence per line. |
| `generate_paragraphs(count, famous)` | Blank-line-separated paragraphs. |
| `generate_ascii_art(cols, rows, gap)` | Tiled ASCII-art herd. |
| `famous_sentence()` | The canonical 8-buffalo sentence. |

The server speaks stdio. To launch it directly (e.g., for debugging):

```bash
buffalo-ipsum-mcp
```

## License

MIT
