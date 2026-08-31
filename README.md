# Moffat Bay Lodge

Capstone project for a lodge reservation application built with Flask and MySQL.

## Project structure

The running application starts at [run.py](run.py), which creates the Flask application through
the `moffat_bay` application factory. It uses feature-oriented Flask blueprints, SQLAlchemy
models, and Alembic migrations. Development quality checks use Ruff and pytest.

| Path | Purpose |
| --- | --- |
| [moffat_bay/](moffat_bay/) | Active Flask application package. [config.py](moffat_bay/config.py) loads environment-based configuration; [db.py](moffat_bay/db.py) configures SQLAlchemy and Flask-Migrate; [models.py](moffat_bay/models.py) defines the current data model; [cli.py](moffat_bay/cli.py) and [seeds.py](moffat_bay/seeds.py) provide database commands and fictional development data. |
| [moffat_bay/public/](moffat_bay/public/) | Public home-page and health-check routes. |
| [moffat_bay/auth/](moffat_bay/auth/) | Registration, login, logout, session helpers, and forms. |
| [moffat_bay/reservations/](moffat_bay/reservations/) | Ownership boundary for the future room-selection and reservation workflow; it does not currently expose application routes. |
| [moffat_bay/templates/](moffat_bay/templates/) | Jinja templates; feature templates extend [base.html](moffat_bay/templates/base.html). |
| [moffat_bay/static/](moffat_bay/static/) | Browser assets: CSS, JavaScript, and images. |
| [migrations/](migrations/) | Alembic migration environment and versioned schema revisions. Use this directory and `models.py` for active schema changes. |
| [scripts/](scripts/) | Cross-platform bootstrap, MySQL provisioning, and validation automation. |
| [tests/](tests/) | Pytest smoke, authentication, schema, seed/CLI, and script tests. |
| [docs/](docs/) | Development guide, contribution standards, and architecture decision records. |
| [.github/](.github/) | GitHub Actions CI, code-owner rules, issue templates, and pull-request template. |
| [pyproject.toml](pyproject.toml), [requirements.txt](requirements.txt), and [requirements-dev.txt](requirements-dev.txt) | Python tooling configuration plus runtime and development dependency definitions. |
| [.env.example](.env.example), [.editorconfig](.editorconfig), and [.gitignore](.gitignore) | Local environment template, shared formatting defaults, and excluded local/generated files. |

### Reference material

[archive/](archive/) preserves the original technical design document, ERD, wireframes, and other
course artifacts. Its archived SQL migrations and seed files are historical reference only: the
running application does not execute them. Current database work belongs in
[moffat_bay/models.py](moffat_bay/models.py) and [migrations/](migrations/); see the
[archived database notes](archive/archived_database_files/README.md) for details.

### Where to go next

- [Development guide](docs/DEVELOPMENT.md): daily workflow, configuration, database setup, and troubleshooting.
- [Contributing guide](docs/CONTRIBUTING.md): branch, review, code-quality, and security expectations.
- [Persistence decision](docs/decisions/0003-sqlalchemy-alembic-persistence.md): rationale for SQLAlchemy, Flask-Migrate, and Alembic.
- [Script reference](scripts/README.md): detailed behavior of the setup and validation scripts.

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
