# Development guide

## Prerequisites

- Python 3.12
- MySQL Community Server 8.4 LTS for database-backed development
- Git

## First-time setup

```bash
python scripts/bootstrap.py
source .venv/bin/activate
```

On Windows, start the script with `py -3.12 scripts/bootstrap.py` and activate with
`.\.venv\Scripts\Activate.ps1`.

The script creates `.venv`, upgrades pip, installs `requirements-dev.txt`, and copies
`.env.example` to `.env` when that file does not already exist. Re-running it is safe and never
overwrites an existing `.env`.

Edit `.env` with local MySQL Community Server 8.4 LTS values. Do not commit it.

Database-backed features require a running MySQL server and configured application connection
values. Set `MYSQL_ROOT_PASSWORD` in the operating-system environment, then provision both the
development and disposable test databases:

```bash
python scripts/setup_databases.py
```

On Windows PowerShell, set `$env:MYSQL_ROOT_PASSWORD` for the current session before running the
script. It creates the configured application database and `moffat_bay_test` if needed, creates
and grants a non-root configured `MYSQL_USER` access to both, applies pending Alembic migrations,
and (re)loads the fixed fictional development dataset. Re-running it is safe: it does not drop
databases or tables.

The helper writes `TEST_DATABASE_URL` to the ignored `.env` file. It must target the disposable
`moffat_bay_test` database; database-marked pytest tests use it and clear their data after every
test. Never configure this URL for production data. Use `flask db migrate -m "message"` after
changing models in `moffat_bay/models.py`, then rerun `python scripts/setup_databases.py` to apply
the new revision locally.

## Daily development

Create a feature or bugfix branch.

Before pushing:

```bash
python scripts/validate.py
```

The validation gate runs Ruff linting, Ruff formatting verification, and the full pytest suite in that order. It stops at the first failing check.

Without `TEST_DATABASE_URL`, database-marked tests are skipped, so the automated gate does not
require MySQL by default. After `python scripts/setup_databases.py` configures the disposable test
database, `python scripts/validate.py` includes those integration tests. In a configured local
database environment, run `flask db-ping` to separately confirm application connectivity.

Ruff can automatically fix safe lint issues with `python -m ruff check . --fix` and formatting drift with `python -m ruff format .`; review all resulting changes before committing.

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

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Local root shortcut (optional)

For solo local development you can connect as MySQL `root` instead of creating a
least-privilege `moffat_app` user, and keep the root password out of `.env` entirely:

1. Set `MYSQL_ROOT_PASSWORD` in your own OS environment (not in `.env`). On macOS or Linux,
   export it from your shell profile; in PowerShell, use
   `[Environment]::SetEnvironmentVariable('MYSQL_ROOT_PASSWORD', '<password>', 'User')`.
2. In `.env`, set `MYSQL_USER=root` and `MYSQL_PASSWORD=${MYSQL_ROOT_PASSWORD}`.
   `python-dotenv` expands `${VAR}` references against your OS environment when loading `.env`.
3. Run `flask db-ping` to confirm the application can reach MySQL with these values.

## Architecture boundaries

- `public` owns routes that never require authentication.
- `auth` owns registration, login, logout, and session behavior.
- `reservations` owns room selection, calculations, confirmation, persistence, and lookup.
- Shared configuration stays in `config.py`; shared SQLAlchemy/Migrate setup stays in `db.py`.
- ORM models live in `moffat_bay/models.py`; database automation CLI commands live in `moffat_bay/cli.py`.
- Templates extend `base.html` so navigation and accessibility improvements remain consistent.

Blueprints for `auth` and `reservations` should be registered only when those tasks add working routes. Avoid placeholder endpoints that imply incomplete features are available.

## Troubleshooting

- `flask` is not recognized: activate `.venv` and reinstall `requirements-dev.txt`.
- Imports fail: run commands from the repository root.
- MySQL refuses the connection: verify the server is running and compare `.env` with the local user/database.
- Port 5000 is busy: run `flask --app run.py run --debug --port 5001`.

