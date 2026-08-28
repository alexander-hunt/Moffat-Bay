"""Provision and migrate the local development and test MySQL databases."""

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv, set_key
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPOSITORY_ROOT / ".env"
TEST_DATABASE_NAME = "moffat_bay_test"
LOCAL_MYSQL_ACCOUNT_HOST = "localhost"
DATABASE_IDENTIFIER = re.compile(r"[A-Za-z0-9_]+\Z")
MYSQL_ACCOUNT_NAME = re.compile(r"[A-Za-z0-9_.-]+\Z")


@dataclass(frozen=True)
class DatabaseSettings:
    """Connection settings shared by the local application databases."""

    host: str
    port: int
    database: str
    username: str
    password: str
    root_password: str


def required_environment_value(name: str) -> str:
    """Return a required environment value or explain how to configure it."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} must be configured before running this script.")
    return value


def validate_name(name: str, value: str, pattern: re.Pattern[str]) -> str:
    """Reject configuration that cannot be safely used in MySQL DDL."""
    if not pattern.fullmatch(value):
        raise ValueError(f"{name} contains unsupported characters.")
    return value


def load_settings() -> DatabaseSettings:
    """Load local settings after dotenv has expanded local variable references."""
    host = required_environment_value("MYSQL_HOST")
    database = validate_name(
        "MYSQL_DATABASE", required_environment_value("MYSQL_DATABASE"), DATABASE_IDENTIFIER
    )
    username = validate_name(
        "MYSQL_USER", required_environment_value("MYSQL_USER"), MYSQL_ACCOUNT_NAME
    )
    try:
        port = int(required_environment_value("MYSQL_PORT"))
    except ValueError as error:
        raise ValueError("MYSQL_PORT must be an integer.") from error
    if not 1 <= port <= 65535:
        raise ValueError("MYSQL_PORT must be between 1 and 65535.")

    return DatabaseSettings(
        host=host,
        port=port,
        database=database,
        username=username,
        password=required_environment_value("MYSQL_PASSWORD"),
        root_password=required_environment_value("MYSQL_ROOT_PASSWORD"),
    )


def database_url(settings: DatabaseSettings, database: str, password: str) -> URL:
    """Build a URL without exposing credentials through string interpolation."""
    return URL.create(
        "mysql+pymysql",
        username=settings.username,
        password=password,
        host=settings.host,
        port=settings.port,
        database=database,
    )


def provision_databases(settings: DatabaseSettings) -> None:
    """Create the two local databases and grant the configured account access."""
    root_url = URL.create(
        "mysql+pymysql",
        username="root",
        password=settings.root_password,
        host=settings.host,
        port=settings.port,
    )
    engine = create_engine(root_url)
    database_names = (settings.database, TEST_DATABASE_NAME)
    try:
        with engine.begin() as connection:
            for database_name in database_names:
                connection.execute(
                    text(
                        f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                        "CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci"
                    )
                )

            if settings.username != "root":
                account = f"'{settings.username}'@'{LOCAL_MYSQL_ACCOUNT_HOST}'"
                connection.execute(
                    text(f"CREATE USER IF NOT EXISTS {account} IDENTIFIED BY :password"),
                    {"password": settings.password},
                )
                for database_name in database_names:
                    connection.execute(
                        text(f"GRANT ALL PRIVILEGES ON `{database_name}`.* TO {account}")
                    )
    finally:
        engine.dispose()


def persist_test_database_url(settings: DatabaseSettings) -> None:
    """Make the dedicated test database available to the existing pytest fixtures."""
    test_url = database_url(settings, TEST_DATABASE_NAME, settings.password)
    set_key(ENV_FILE, "TEST_DATABASE_URL", test_url.render_as_string(hide_password=False))


def run_flask(arguments: list[str], environment: dict[str, str]) -> int:
    """Run a Flask database command from the repository root."""
    completed = subprocess.run(
        [sys.executable, "-m", "flask", "--app", "run.py", *arguments],
        cwd=REPOSITORY_ROOT,
        env=environment,
    )
    return completed.returncode


def migrate_databases(settings: DatabaseSettings) -> int:
    """Migrate both databases and seed only the development database."""
    development_environment = os.environ.copy()
    development_environment["MYSQL_DATABASE"] = settings.database
    print("==> Migrating and seeding the development database")
    returncode = run_flask(["init-db"], development_environment)
    if returncode != 0:
        return returncode

    test_environment = os.environ.copy()
    test_environment["MYSQL_DATABASE"] = TEST_DATABASE_NAME
    print("==> Migrating the test database")
    return run_flask(["db", "upgrade"], test_environment)


def main() -> int:
    load_dotenv(ENV_FILE)
    try:
        settings = load_settings()
        print("==> Creating local databases and granting application access")
        provision_databases(settings)
        persist_test_database_url(settings)
        returncode = migrate_databases(settings)
    except (SQLAlchemyError, ValueError) as error:
        print(f"Database setup failed: {error}", file=sys.stderr)
        return 1

    if returncode != 0:
        print("Database migration failed.", file=sys.stderr)
        return returncode
    print("Database setup complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
