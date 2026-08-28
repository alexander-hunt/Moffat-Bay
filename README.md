# Moffat Bay Lodge

Capstone project for a lodge reservation application built with Flask and MySQL.

## Five-minute setup

This quick path starts the public Flask application and verifies its smoke-test endpoints.

### Prerequisites

- Python 3.12
- MySQL Community Server 8.4 LTS for database-backed development
- Git

### Install and run

From the repository root, run the bootstrap script with Python 3.12. It creates `.venv`, installs the development dependencies, and copies `.env.example` to `.env` if that file does not already exist:

```bash
python scripts/bootstrap.py
source .venv/bin/activate
flask --app run.py run --debug
```

On Windows, start the script with `py -3.12 scripts/bootstrap.py` and activate with `.venv\Scripts\activate`.

Open `http://127.0.0.1:5000/` in a browser. The page should load as the Moffat Bay Lodge home page. You can also verify the health endpoint at `http://127.0.0.1:5000/health`, which should return:

```json
{"service":"moffat-bay","status":"ok"}
```

Stop the development server with `Ctrl+C`.

## MySQL configuration

Install and run MySQL Community Server 8.4 LTS before working on database-backed features. Edit the copied `.env` file with the local connection values:

| Variable | Example |
| --- | --- |
| `MYSQL_HOST` | `localhost` |
| `MYSQL_PORT` | `3306` |
| `MYSQL_DATABASE` | `moffat_bay` |
| `MYSQL_USER` | `moffat_app` |
| `MYSQL_PASSWORD` | Your local password |

Set `SECRET_KEY` to a long random local value. Never commit `.env`, passwords, production data, or personal customer information.

For solo local development, you can instead connect as MySQL `root` and keep the password out of `.env` entirely. See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md#local-root-shortcut-optional) for the root shortcut and the `flask db-ping` connectivity check.

## Development checks

With `.venv` activated, run:

```bash
python scripts/validate.py
```

This checks Ruff linting, Ruff formatting, and the full pytest suite. See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for the full development workflow, configuration details, architecture boundaries, and troubleshooting guidance.
