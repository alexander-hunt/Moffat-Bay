"""Run the project validation gate: Ruff linting, Ruff formatting, and pytest."""

import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

CHECKS = (
    ("Ruff lint", ["-m", "ruff", "check", "."]),
    ("Ruff format", ["-m", "ruff", "format", "--check", "."]),
    ("Pytest", ["-m", "pytest"]),
)


def main() -> int:
    for name, arguments in CHECKS:
        print(f"==> {name}", flush=True)
        # sys.executable keeps the checks on the active interpreter regardless of PATH.
        completed = subprocess.run([sys.executable, *arguments], cwd=REPOSITORY_ROOT)
        if completed.returncode != 0:
            print(f"{name} failed.", file=sys.stderr)
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
