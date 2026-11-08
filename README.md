> **Current maintained source:** [open the Noah branch](https://github.com/LucasXlab/diffnote/tree/noah/diffnote#readme) · [简体中文](https://github.com/LucasXlab/diffnote/blob/noah/diffnote/README.zh-CN.md). This `main` branch retains the older 0.1 interface. Follow the explicit branch installation on the maintained README for the new-file report export and reviewed Git handling.

<p align="center"><img src="assets/logo.svg" width="72" height="72" alt="diffnote logo"></p>
<h1 align="center">diffnote</h1>
<p align="center"><strong>Turn local Git changes into a reviewable pull request summary.</strong></p>

[![CI](https://github.com/LucasXlab/diffnote/actions/workflows/ci.yml/badge.svg)](https://github.com/LucasXlab/diffnote/actions/workflows/ci.yml) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Version](https://img.shields.io/badge/source-v0.1.0-6b7280.svg)](https://github.com/LucasXlab/diffnote/blob/main/pyproject.toml) ![Runtime](https://img.shields.io/badge/Python-3.8%2B-3776ab.svg) [![Stars](https://img.shields.io/github/stars/LucasXlab/diffnote?style=flat)](https://github.com/LucasXlab/diffnote/stargazers)

[English](README.md) · [简体中文](README.zh-CN.md)

![Real CLI output on synthetic fixtures](assets/demo.gif)

The demo is captured from the real CLI using synthetic data. [Transcript](demo/terminal.txt) · regenerate with `python3 scripts/demo.py`.

## Why

Writing a PR description after the coding is finished is easy to postpone. diffnote groups a diff by area, highlights rule-based risk signals, and generates a starting point for the reviewer.

| Start with | Good for | Where diffnote helps |
|---|---|---|
| `git diff --stat` | Inspect change size | diffnote adds grouping and a PR-description draft. |
| Commit-log changelogs | Describe released commits | diffnote can also summarize tracked, uncommitted changes. |

## Quick start

```bash
git clone https://github.com/LucasXlab/diffnote.git && cd diffnote
python3 -m pip install .
python3 scripts/demo.py
```

Install from this checkout to use the reviewed source version. The installed tool has no third-party runtime dependencies; cloning and installation can require network access.

## Features

### Choose your diff

Summarize tracked working-tree changes, staged changes, a base ref, or a commit range.

### Group the work

Bucket source, tests, docs, configuration and migrations; surface file and line-change counts.

### Export a draft

Generate terminal, Markdown or JSON output. Save Markdown to a file with `--markdown --save body.md`; successful saving leaves stdout empty. Titles and risk signals are heuristics, not a semantic code review.

### Optional prose

`--llm` sends a bounded diff excerpt to the configured Ollama endpoint; the default is localhost and unavailable models fall back to rules.

![CLI result](assets/demo.png)

## Usage

```bash
diffnote --staged
diffnote --base main --markdown
diffnote --range main..HEAD --json
diffnote --commits 2
diffnote --markdown --save body.md
diffnote --color
diffnote --no-color
```

Terminal output uses ANSI colors only when stdout is a terminal. `--color` forces colors; `--no-color` disables them.

Breaking-change hints use `!:` subjects from the selected `--commits`, `--range`, or `--base` comparison, without a 25-commit cutoff. Working-tree and staged-only summaries do not reuse historical commit subjects. Public API path hints still apply in every mode.

## Architecture

```mermaid
flowchart LR
A[Local Git diff] --> B[Parse files and hunks]
B --> C[Group areas and risk signals]
C --> D[Terminal / Markdown / JSON]
B -. explicit --llm .-> E[Configured Ollama endpoint]
E --> D
```

## Privacy and limits

Default operation reads local Git data without network requests. `--llm` sends up to 6,000 diff characters and a suggested title to `DIFFNOTE_OLLAMA` (default `http://localhost:11434`). A remote setting sends that data off the machine. Reports can contain filenames and diff details. See [PRIVACY.md](PRIVACY.md) for data boundaries.

## Development

```bash
python3 -m pip install -e ".[test]"
python3 -m pytest -q
```

The demo uses a temporary fixture and does not inspect your personal repositories or agent homes.

## Roadmap

- [ ] Improve error messages for invalid refs and empty histories.
- [ ] Add configurable grouping rules.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Report reproducible problems in [Issues](https://github.com/LucasXlab/diffnote/issues). Follow [SECURITY.md](SECURITY.md) for sensitive reports.

## License

[MIT](LICENSE).
