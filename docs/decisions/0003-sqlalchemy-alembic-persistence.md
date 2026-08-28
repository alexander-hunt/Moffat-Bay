# ADR 0003: SQLAlchemy and Alembic persistence

- Status: Accepted
- Date: 2026-08-28
- Decision owner: Group B, led by Alexander Hunt
- Supersedes: [ADR 0001](0001-project-structure.md)

## Context

The application needs one persistence layer that supports MySQL, model-driven schema changes,
repeatable local setup, and isolated database integration tests. ADR 0001 originally selected
MySQL Connector/Python with a request-scoped connection helper, but the implemented application
uses SQLAlchemy models and Flask database extensions instead.

## Decision

Use Flask-SQLAlchemy for the shared application `db` extension and PyMySQL as the MySQL driver.
Define the application schema in `moffat_bay/models.py` and manage schema revisions with
Flask-Migrate and Alembic.

`flask init-db` applies pending migrations and loads the fictional development data.
`scripts/setup_databases.py` creates the configured development database and the disposable
`moffat_bay_test` database, creates and grants a non-root configured application account when
needed, initializes the development database, and upgrades the test database. The legacy SQL
files under `database/` remain reference material for the original ERD and are not executed by
the running application.

## Consequences

- Model changes require an Alembic migration created with `flask db migrate -m "message"`.
- Application code uses the shared SQLAlchemy session instead of direct connector calls.
- `TEST_DATABASE_URL` must target the disposable `moffat_bay_test` database for integration
  tests; test fixtures clear its data after every test.
- Development seeds are idempotent and are loaded only into the development database during
  local provisioning.
- Contributors need Flask-SQLAlchemy, Flask-Migrate, SQLAlchemy, and PyMySQL in the project
  dependencies.