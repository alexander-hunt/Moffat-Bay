# Project scripts

These scripts are run from the repository root with Python 3.12.

## `bootstrap.py`

Creates the local `.venv` virtual environment, upgrades pip, installs the development dependencies from `requirements-dev.txt`, and creates `.env` from `.env.example` when `.env` does not already exist.

Run it once when setting up the project, or run it again to install updated development dependencies:

```bash
python scripts/bootstrap.py
```

On Windows, use:

```powershell
py -3.12 scripts/bootstrap.py
```

The script never overwrites an existing `.env` file. Activate the environment after it finishes:

```bash
# macOS or Linux
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

## `setup_databases.py`

Creates the configured local application database and the disposable `moffat_bay_test`
database when they do not already exist. When `MYSQL_USER` is not `root`, it creates that local
account if needed and grants it access to both databases. It applies all Alembic migrations and
reloads the fictional development seed data. The test database remains empty for pytest to
isolate its database tests.

Set `MYSQL_ROOT_PASSWORD` in the operating-system environment before running the script. The
password is used only to provision local MySQL databases and accounts; it is not written to
`.env`. The script stores `TEST_DATABASE_URL` in the ignored `.env` file so database-marked
pytest tests can use `moffat_bay_test`.

```bash
python scripts/setup_databases.py
```

On Windows PowerShell, set the password for the current session and run:

```powershell
$env:MYSQL_ROOT_PASSWORD = "your-local-root-password"
py -3.12 scripts/setup_databases.py
```

It is safe to run again: it never drops a database, applies pending migrations, and upserts the
fixed development seed data.

## `validate.py`

Runs the project's validation checks in order:

1. Ruff linting
2. Ruff formatting check
3. The full pytest test suite

The script stops and returns an error as soon as a check fails. Run it before pushing changes:

```bash
python scripts/validate.py
```

Run this command with the project's virtual environment activated.