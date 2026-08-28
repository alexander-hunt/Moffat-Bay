"""Tests for the project validation gate."""

from subprocess import CompletedProcess
from unittest.mock import call

from scripts import validate


def test_main_runs_all_checks_in_order(monkeypatch):
    calls = []

    def run(*arguments, **kwargs):
        calls.append(call(*arguments, **kwargs))
        return CompletedProcess(arguments, 0)

    monkeypatch.setattr(validate.subprocess, "run", run)

    assert validate.main() == 0

    assert calls == [
        call([validate.sys.executable, *arguments], cwd=validate.REPOSITORY_ROOT)
        for _, arguments in validate.CHECKS
    ]


def test_main_stops_after_first_failed_check(monkeypatch, capsys):
    results = iter((CompletedProcess([], 0), CompletedProcess([], 7)))
    calls = []

    def run(*arguments, **kwargs):
        calls.append(call(*arguments, **kwargs))
        return next(results)

    monkeypatch.setattr(validate.subprocess, "run", run)

    assert validate.main() == 7

    assert calls == [
        call([validate.sys.executable, *validate.CHECKS[0][1]], cwd=validate.REPOSITORY_ROOT),
        call([validate.sys.executable, *validate.CHECKS[1][1]], cwd=validate.REPOSITORY_ROOT),
    ]
    assert "Ruff format failed." in capsys.readouterr().err
