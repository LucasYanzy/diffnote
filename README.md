<p align="center"><strong>English</strong> &nbsp;·&nbsp; <a href="README.zh-CN.md">简体中文</a></p>

<p align="center"><img src="assets/logo.svg" width="54" height="54" alt=""></p>
<h1 align="center">diffnote</h1>
<p align="center"><strong>A useful first draft for your next PR.</strong></p>
<p align="center">Turn local Git changes into a reviewable draft: changed areas, file metadata, line counts, and traceable review signals. No model or server is required.</p>
<p align="center"><a href="#quick-start">Quick start</a> &nbsp;·&nbsp; <a href="#usage">Usage</a> &nbsp;·&nbsp; <a href="docs/guide.md">Guide</a> &nbsp;·&nbsp; <a href="CONTRIBUTING.md">Contribute</a></p>

<p align="center"><a href="assets/demo.gif" title="Open the full-size usage demonstration"><img src="assets/demo.gif" width="860" alt="Working-tree and staged changes become drafts; the showcase also covers metadata, review signals, and JSON."></a></p>

Working-tree and staged changes become drafts; the showcase also covers metadata, review signals, and JSON. [Recording and reproduction](docs/showcase.md).

## Why diffnote?

The diff tells you what changed; a PR still needs a useful explanation. diffnote gives you a factual starting point from the selected changes. Add your intent and the verification you actually performed before publishing the draft.

## Quick start

Python 3.11+ and Git 2.31+ on macOS or Linux. The demo uses disposable synthetic Git data; installation may download build tools.

The `0.2` source is on `noah/diffnote`; the repository's `main` branch still contains the older `0.1` interface. Select the branch explicitly:

```bash
git clone --branch noah/diffnote https://github.com/LucasXlab/diffnote.git
cd diffnote
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
python scripts/demo.py
```

Keep the environment active, enter your project, and select the changes you want to describe:

```bash
cd /absolute/path/to/your/repo
git diff --cached --stat
diffnote --staged --markdown --output pr-draft.md
```

Open `pr-draft.md`, confirm the changed files and counts, then add **why** you made the change and the validation you ran. No selected changes produces an empty draft; it does not establish that the working tree is clean. `--output` (alias `--save`) creates a private new file and refuses to overwrite an existing file; analysis errors create no output. Use a different filename for the next draft.

The `0.2` interface runs without model calls and does not provide the old `--llm` or `--color` options. `--no-color`, Markdown and JSON remain available.

## Usage

### Describe the next commit

```bash
diffnote --staged --markdown
```

This selects the index. Without `--staged`, tracked working-tree changes include staged edits; untracked files enter the report only after staging.

### Select a branch comparison or structured output

```bash
diffnote --base main --markdown
diffnote --range main...feature --markdown
diffnote --staged --json
```

`A..B` compares committed endpoints; `A...B` compares the merge base to B. Working/staged titles come from current changed paths rather than an unrelated previous commit.

Exit `0` means supported analysis completed, not approval of the change. Exit `2` covers usage, Git, size, timeout, and parsing failures. No project tests are executed.

## Scope

A draft does not establish intent, semantic correctness, or safety. Unsupported patches and incomplete Git data fail explicitly. Reports contain actual paths and subjects; inspect before sharing. Global/helper configuration defenses do not sandbox a malicious Git executable.

See the [usage guide](docs/guide.md) for more examples, exact parameters, and technical boundaries.

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). Use synthetic reproductions and report the validation you actually ran.

[MIT License](LICENSE) · [简体中文](README.zh-CN.md)
