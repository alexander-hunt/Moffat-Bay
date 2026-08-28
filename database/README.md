# Moffat Bay Lodge SQL integration

These files are kept as reference documentation for the approved `CUSTOMER`,
`ROOM_TYPE`, and `RESERVATION` ERD. The running application no longer executes
them: schema is managed by Flask-Migrate/Alembic revisions generated from
`moffat_bay/models.py`, and development data is loaded by the `flask init-db`
CLI command (see `moffat_bay/seeds.py`). See `docs/DEVELOPMENT.md` for the
current setup steps, including `scripts/setup_databases.py` for local database
provisioning.

They still use the repository's lowercase `snake_case` convention and its
configured `moffat_bay` database, and remain useful for understanding the
original schema design and constraints.

