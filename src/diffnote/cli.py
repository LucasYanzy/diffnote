"""Offline diffnote command line."""

import argparse
import os
import sys
import tempfile
from pathlib import Path

from . import __version__, analyze, gitutil, render
from .parser import ParseError


def build_parser():
    p = argparse.ArgumentParser(
        prog="diffnote",
        description="Turn local Git changes into a reviewable PR draft. No network or model calls.",
    )
    p.add_argument("--version", action="version", version=f"diffnote {__version__}")
    src = p.add_mutually_exclusive_group()
    src.add_argument(
        "--commits", type=int, metavar="N", help="Net changes in N first-parent commits (1..1000)."
    )
    src.add_argument(
        "--base", metavar="REF", help="Tracked working tree versus a verified local commit."
    )
    src.add_argument(
        "--range", metavar="A..B", help="A..B compares endpoints; A...B compares merge-base to B."
    )
    src.add_argument(
        "--staged",
        action="store_true",
        help="Index changes versus HEAD, or empty tree on an unborn branch.",
    )
    fmt = p.add_mutually_exclusive_group()
    fmt.add_argument("--markdown", action="store_true", help="Print a reviewable Markdown draft.")
    fmt.add_argument("--json", action="store_true", help="Print one JSON document.")
    p.add_argument(
        "--output",
        "--save",
        metavar="PATH",
        help="Save Markdown/JSON to a new file atomically; never overwrite an existing path.",
    )
    p.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors (also respects NO_COLOR/non-TTY).",
    )
    return p


def save_report(destination, text):
    """Publish complete output without truncating or replacing an existing file."""
    target = Path(destination).absolute()
    descriptor, temporary = tempfile.mkstemp(prefix=".diffnote-", dir=target.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        # link creates the final directory entry atomically and refuses existing
        # paths, including symlinks. The temporary file has private permissions.
        os.link(temporary, target)
    finally:
        os.unlink(temporary)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.output and not (args.markdown or args.json):
        parser.error("--output/--save requires --markdown or --json")
    try:
        cwd = gitutil.repo_root()
        patch, stats, messages, source = gitutil.read_selection(
            cwd=cwd, base=args.base, range_spec=args.range, commits=args.commits, staged=args.staged
        )
        files = analyze.parse_diff(patch)
        gitutil.verify_numstat(files, stats)
        summary = analyze.build_summary(files, messages, source)
    except (gitutil.GitError, ParseError) as exc:
        print(f"diffnote: {exc}", file=sys.stderr)
        return 2
    if args.output:
        text = render.render_json(summary) if args.json else render.render_markdown(summary)
        try:
            save_report(args.output, text)
        except OSError as exc:
            print(
                f"diffnote: cannot save report ({type(exc).__name__}); use a new writable path",
                file=sys.stderr,
            )
            return 2
    elif args.json:
        print(render.render_json(summary))
    elif args.markdown:
        print(render.render_markdown(summary))
    elif not files:
        print("diffnote: no changes detected in selected tracked changes.", file=sys.stderr)
    else:
        color = not args.no_color and "NO_COLOR" not in os.environ and sys.stdout.isatty()
        print(render.render_terminal(summary, use_color=color))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
