"""Create the local virtual environment, install dev dependencies, and seed .env."""

# Runs on the system interpreter before .venv exists, so it uses only the standard library.

import os
import shutil
import subprocess
import venv
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = REPOSITORY_ROOT / ".venv"


def venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def run(arguments: list[str]) -> int:
    completed = subprocess.run([str(venv_python()), *arguments], cwd=REPOSITORY_ROOT)
    return completed.returncode


def main() -> int:
    if VENV_DIR.exists():
        print(f"==> Using existing virtual environment at {VENV_DIR}")
    else:
        print(f"==> Creating virtual environment at {VENV_DIR}")
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)

    print("==> Upgrading pip")
    returncode = run(["-m", "pip", "install", "--upgrade", "pip"])
    if returncode != 0:
        return returncode

    print("==> Installing development dependencies")
    returncode = run(["-m", "pip", "install", "-r", "requirements-dev.txt"])
    if returncode != 0:
        return returncode

    env_file = REPOSITORY_ROOT / ".env"
    if env_file.exists():
        print("==> .env already exists; leaving it unchanged")
    else:
        shutil.copyfile(REPOSITORY_ROOT / ".env.example", env_file)
        print("==> Created .env from .env.example; edit it with local values")

    activate = ".venv\\Scripts\\activate" if os.name == "nt" else "source .venv/bin/activate"
    print(f"\nDone. Activate the environment with: {activate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
