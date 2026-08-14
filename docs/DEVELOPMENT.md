# Development guide

## Prerequisites

- Python 3.12
- MySQL Community Server 8.4 LTS for database-backed development
- Git

## First-time setup on Windows

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Edit `.env` with local MySQL Community Server 8.4 LTS values. Do not commit it.

Database-backed features require a running MySQL server and a configured application database. 

## Daily development

Create a feature or bugfix branch.

Before pushing:

```powershell
ruff check .
pytest
```

Ruff can automatically fix safe formatting/import issues with `ruff check . --fix`; review all resulting changes before committing.

## Configuration

| Variable | Purpose | Local example |
| --- | --- | --- |
| `SECRET_KEY` | Protects sessions and CSRF tokens | Long random local value |
| `MYSQL_HOST` | MySQL hostname | `localhost` |
| `MYSQL_PORT` | MySQL TCP port | `3306` |
| `MYSQL_DATABASE` | Application database | `moffat_bay` |
| `MYSQL_USER` | Least-privilege application user | `moffat_app` |
| `MYSQL_PASSWORD` | Application user's password | Local secret |

Generate a local secret with:

```powershell
py -c "import secrets; print(secrets.token_hex(32))"
```

## Architecture boundaries

- `public` owns routes that never require authentication.
- `auth` owns registration, login, logout, and session behavior.
- `reservations` owns room selection, calculations, confirmation, persistence, and lookup.
- Shared configuration stays in `config.py`; shared connection handling stays in `db.py`.
- Templates extend `base.html` so navigation and accessibility improvements remain consistent.

Blueprints for `auth` and `reservations` should be registered only when those tasks add working routes. Avoid placeholder endpoints that imply incomplete features are available.

## Troubleshooting

- `flask` is not recognized: activate `.venv` and reinstall `requirements-dev.txt`.
- Imports fail: run commands from the repository root.
- MySQL refuses the connection: verify the server is running and compare `.env` with the local user/database.
- Port 5000 is busy: run `flask --app run.py run --debug --port 5001`.

