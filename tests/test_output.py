import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "src"


@pytest.fixture
def repo(tmp_path):
    env = {
        **os.environ,
        "PYTHONPATH": str(SOURCE),
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Synthetic Contributor",
        "GIT_COMMITTER_NAME": "Synthetic Contributor",
        "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
    }
    for args in [
        ["init", "-q"],
        ["add", "."],
        ["-c", "commit.gpgsign=false", "commit", "-qm", "fixture"],
    ]:
        (tmp_path / "app.py").write_text("value = 1\n")
        subprocess.run(["git", *args], cwd=tmp_path, env=env, check=True, capture_output=True)
    (tmp_path / "app.py").write_text("value = 2\n")

    def run(*args):
        return subprocess.run(
            [sys.executable, "-m", "diffnote", *args],
            cwd=tmp_path,
            env=env,
            text=True,
            capture_output=True,
        )

    return tmp_path, run


@pytest.mark.parametrize("option", ["--output", "--save"])
def test_report_is_saved_without_stdout_or_existing_file_overwrite(repo, option):
    path, run = repo
    result = run("--json", option, "report.json")
    assert result.returncode == 0, result.stderr
    assert result.stdout == ""
    target = path / "report.json"
    data = json.loads(target.read_text())
    assert data["total_files"] == 1
    original = target.read_bytes()
    assert target.stat().st_mode & 0o077 == 0
    result = run("--json", option, "report.json")
    assert result.returncode == 2
    assert target.read_bytes() == original
    assert not list(path.glob(".diffnote-*"))


def test_failed_analysis_does_not_create_output(repo):
    path, run = repo
    result = run("--base", "missing-ref", "--markdown", "--output", "draft.md")
    assert result.returncode == 2
    assert not (path / "draft.md").exists()


def test_output_symlink_does_not_change_its_target(repo):
    path, run = repo
    target = path / "keep.txt"
    target.write_text("keep")
    (path / "draft.md").symlink_to(target)
    assert run("--markdown", "--save", "draft.md").returncode == 2
    assert target.read_text() == "keep"
