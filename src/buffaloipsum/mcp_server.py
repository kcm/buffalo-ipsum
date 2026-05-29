"""MCP server exposing buffalo-ipsum's generators as tools.

Run as:

    buffalo-ipsum-mcp
    # or
    python -m buffaloipsum.mcp_server

Or wire it into an MCP client (e.g., Claude Code's settings.json):

    {
      "mcpServers": {
        "buffalo-ipsum": {
          "command": "buffalo-ipsum-mcp"
        }
      }
    }

Requires the [mcp] extra:

    pip install 'buffalo-ipsum[mcp]'

Tools exposed:

    generate_words(count)
    generate_sentences(count, famous)
    generate_paragraphs(count, famous)
    generate_ascii_art(cols, rows, gap)
    famous_sentence()
"""

from __future__ import annotations

from . import (
    FAMOUS_SENTENCE,
    ascii_art as _ascii_art,
    paragraphs as _paragraphs,
    sentences as _sentences,
    words as _words,
)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:  # pragma: no cover - exercised manually
    raise ImportError(
        "buffaloipsum.mcp_server requires the 'mcp' package. "
        "Install with: pip install 'buffalo-ipsum[mcp]'"
    ) from e


mcp = FastMCP("buffalo-ipsum")


@mcp.tool()
def generate_words(count: int = 5) -> str:
    """Generate `count` instances of the word 'buffalo', space-separated."""
    try:
        return " ".join(_words(count))
    except ValueError as e:
        return f"Error: {e}"


@mcp.tool()
def generate_sentences(count: int = 3, famous: bool = False) -> str:
    """Generate `count` sentences of buffalo filler text, one per line.

    If `famous` is True, every sentence is the canonical grammatically-valid
    8-buffalo sentence.
    """
    try:
        return "\n".join(_sentences(count, famous=famous))
    except ValueError as e:
        return f"Error: {e}"


@mcp.tool()
def generate_paragraphs(count: int = 3, famous: bool = False) -> str:
    """Generate `count` paragraphs of buffalo filler text, separated by blank lines."""
    try:
        return "\n\n".join(_paragraphs(count, famous=famous))
    except ValueError as e:
        return f"Error: {e}"


@mcp.tool()
def generate_ascii_art(cols: int = 1, rows: int = 1, gap: int = 2) -> str:
    """Render a `cols` x `rows` grid of ASCII-art buffalo."""
    try:
        return _ascii_art(cols=cols, rows=rows, gap=gap)
    except ValueError as e:
        return f"Error: {e}"


@mcp.tool()
def famous_sentence() -> str:
    """Return the canonical 8-buffalo grammatically-valid sentence.

    "Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo."
    See https://en.wikipedia.org/wiki/Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo
    """
    return FAMOUS_SENTENCE + "."


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
