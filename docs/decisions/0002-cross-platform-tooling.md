# ADR 0002: Cross-platform Python tooling

- Status: Accepted
- Date: 2026-08-28
- Decision owner: Group B, led by Alexander Hunt

## Context

The validation gate and the setup documentation assumed Windows and PowerShell. Teammates who develop on macOS or Linux could not run the gate, and continuous integration ran on a Windows runner only to execute a PowerShell script. Python 3.12 is already a prerequisite for every contributor.

## Decision

Use standard-library Python scripts as the canonical developer entrypoints. `scripts/validate.py` runs Ruff linting, Ruff format verification, and pytest in that order, stopping at the first failure. `scripts/bootstrap.py` creates the virtual environment, installs development dependencies, and seeds `.env` from `.env.example`. `scripts/validate.ps1` is removed, and the Tests workflow runs on `ubuntu-latest`. Documentation presents one cross-platform command set with short notes for the few Windows-specific lines.

## Consequences

- Every contributor runs the same commands regardless of operating system.
- The scripts add no dependencies beyond the existing development requirements.
- Continuous integration is faster and cheaper on a Linux runner.
- Windows-only behavior is no longer validated in continuous integration; an OS matrix can be added later if a platform difference appears.
- New contributors reach a working environment with a single bootstrap command.

This decision can be revisited through another numbered architecture decision record if the team agrees that course or deployment constraints require a change.
