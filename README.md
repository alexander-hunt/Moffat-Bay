# Moffat Bay Lodge

Capstone project for a lodge reservation application built with Flask and MySQL.

## Five-minute setup

This quick path starts the public Flask application and verifies its smoke-test endpoints.

### Prerequisites

- Python 3.12
- MySQL Community Server 8.4 LTS for database-backed development
- Git

### Install and run

From the repository root, run the bootstrap script with Python 3.12. It creates `.venv`, installs the development dependencies, and copies `.env.example` to `.env` if that file does not already exist. Edit `.env` with your local MySQL connection values, set `MYSQL_ROOT_PASSWORD` in your operating-system environment, then provision the local databases:

```bash
python scripts/bootstrap.py
source .venv/bin/activate
python scripts/setup_databases.py
flask --app run.py run --debug
```

On Windows, start the script with `py -3.12 scripts/bootstrap.py`, activate with
`.\.venv\Scripts\Activate.ps1`, set `$env:MYSQL_ROOT_PASSWORD` for the current PowerShell session,
and run `py -3.12 scripts/setup_databases.py`.

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

`setup_databases.py` creates the configured application database and a separate disposable
`moffat_bay_test` database for integration tests. It records the test connection as
`TEST_DATABASE_URL` in the ignored `.env` file; never point that value at production data.

## Development checks

With `.venv` activated, run:

```bash
python scripts/validate.py
```

This checks Ruff linting, Ruff formatting, and the full pytest suite. See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for the full development workflow, configuration details, architecture boundaries, and troubleshooting guidance.
