# ADR 0001: Flask application factory and feature blueprints

- Status: Superseded by [ADR 0003](0003-sqlalchemy-alembic-persistence.md)
- Date: 2026-08-13
- Decision owner: Group B, led by Alexander Hunt

## Context

The application must provide public lodge pages, customer registration and authentication, authenticated reservation confirmation, MySQL persistence, and reservation lookup. Four students need to work concurrently while keeping the initial structure understandable.

## Decision

Use Python with Flask, an application factory, and feature-oriented packages for public pages, authentication, and reservations. Use MySQL Connector/Python behind one shared request-scoped connection helper. Read local configuration from environment variables.

## Consequences

- Teammates can work in separate feature packages with fewer merge conflicts.
- Tests can create isolated application instances.
- Secrets remain outside source control.
- Database access has one reusable entry point.
- The project gains a small amount of structure before feature implementation.

This decision can be revisited through another numbered architecture decision record if the team agrees that course or deployment constraints require a change.

