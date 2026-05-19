# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2026-05-18

### Added
- `README.md` with project overview, usage examples, and mode descriptions.

## [0.1.1] - 2026-05-18

### Added
- `CHANGELOG.md`, `CLAUDE.md`, and `INDEX.md` at the project root.
- Expanded `.gitignore` covering common editor (vim/emacs/VS Code/JetBrains/Sublime),
  env, and OS metadata files.

### Changed
- No runtime behavior changes versus 0.1.0; this release exists to ship the
  updated project metadata in the sdist.

## [0.1.0] - 2026-05-18

### Added
- Initial release.
- Static API: `word`, `words`, `sentence`, `sentences`, `paragraph`, `paragraphs`, `text`.
- `FAMOUS_SENTENCE` constant and `--famous` flag for the canonical 8-buffalo sentence
  (see https://en.wikipedia.org/wiki/Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo).
- `ascii_art(cols, rows, gap)` and `BUFFALO_ART` for tiled ASCII-art buffalos.
- CLI `buffalo-ipsum` with `-t {words,sentences,paragraphs,asciiart,art}`
  (`art` is an alias for `asciiart`), plus `--seed`, `--cols`, `--rows`, `--gap`,
  and `-v/--verbose`.
- Optional `[live]` extra exposing `buffaloipsum.live.word()` and `.words(n)`,
  which fetch each buffalo via a network round-trip to Claude. Requires
  `ANTHROPIC_API_KEY`.
