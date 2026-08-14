# Moffat Bay Lodge

Capstone project for a lodge reservation application built with Flask and MySQL.

## Five-minute setup

This quick path starts the public Flask application and verifies its smoke-test endpoints.

### Prerequisites

- Python 3.12
- MySQL Community Server 8.4 LTS for database-backed development
- Git

### Install and run on Windows

From the repository root, open PowerShell and run:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
flask --app run.py run --debug
```

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

## Development checks

With `.venv` activated, run:

```powershell
ruff check .
pytest
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for the full development workflow, configuration details, architecture boundaries, and troubleshooting guidance.
