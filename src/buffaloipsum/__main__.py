"""CLI: python -m buffaloipsum [-t TYPE] [-n N] [--famous] [--live] [-v]"""

from __future__ import annotations

import argparse
import sys

from . import ascii_art, paragraphs, sentences, words

_ART_ALIASES = {"asciiart", "art"}


def _log(verbose: bool, msg: str) -> None:
    if verbose:
        print(f"[buffaloipsum] {msg}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="buffalo-ipsum",
        description="Generate filler text made entirely of the word 'buffalo'.",
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=("words", "sentences", "paragraphs", "asciiart", "art"),
        default="paragraphs",
        help="output unit (default: paragraphs; 'art' is an alias for 'asciiart')",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=3,
        help="how many units to emit for words/sentences/paragraphs (default: 3)",
    )
    parser.add_argument(
        "--famous",
        action="store_true",
        help="use the canonical 8-buffalo sentence",
    )
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--cols",
        type=int,
        default=1,
        help="asciiart mode: buffalo count across (default: 1)",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=1,
        help="asciiart mode: buffalo count tall (default: 1)",
    )
    parser.add_argument(
        "--gap",
        type=int,
        default=2,
        help="asciiart mode: spacing between tiled buffalo (default: 2)",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help=(
            "fetch each buffalo via a live LLM API call. "
            "Only valid with --type words. Requires the [live] extra "
            "and an ANTHROPIC_API_KEY."
        ),
    )
    parser.add_argument(
        "--model",
        default=None,
        help="LLM model for --live mode (default: claude-haiku-4-5-20251001)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print debug info to stderr (LLM requests/responses, RNG choices, etc.)",
    )

    args = parser.parse_args(argv)

    if args.live and args.type != "words":
        parser.error("--live is only supported with --type words")

    _log(args.verbose, f"args: {vars(args)}")

    out_type = "asciiart" if args.type in _ART_ALIASES else args.type

    if out_type == "words":
        if args.live:
            from . import live
            model = args.model or live.DEFAULT_MODEL
            _log(args.verbose, f"live mode: model={model} count={args.count}")
            out = live.words(args.count, model=model, verbose=args.verbose)
        else:
            out = words(args.count)
        print(" ".join(out))
    elif out_type == "sentences":
        _log(args.verbose, f"seed={args.seed} famous={args.famous}")
        print(
            "\n".join(sentences(args.count, famous=args.famous, seed=args.seed))
        )
    elif out_type == "asciiart":
        _log(args.verbose, f"cols={args.cols} rows={args.rows} gap={args.gap}")
        print(ascii_art(cols=args.cols, rows=args.rows, gap=args.gap))
    else:  # paragraphs
        _log(args.verbose, f"seed={args.seed} famous={args.famous}")
        print(
            "\n\n".join(
                paragraphs(args.count, famous=args.famous, seed=args.seed)
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
