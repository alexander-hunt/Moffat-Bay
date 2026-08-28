"""Tests for the local database provisioning helper."""

from subprocess import CompletedProcess

from scripts import setup_databases


class Connection:
    def __init__(self):
        self.calls = []

    def execute(self, statement, parameters=None):
        self.calls.append((statement.text, parameters))


class BeginContext:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        return False


class Engine:
    def __init__(self, connection):
        self.connection = connection
        self.disposed = False

    def begin(self):
        return BeginContext(self.connection)

    def dispose(self):
        self.disposed = True


def configure_environment(monkeypatch, **changes):
    values = {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_DATABASE": "moffat_bay",
        "MYSQL_USER": "moffat_app",
        "MYSQL_PASSWORD": "application-password",
        "MYSQL_ROOT_PASSWORD": "root-password",
    }
    values.update(changes)
    for name, value in values.items():
        monkeypatch.setenv(name, value)


def test_main_provisions_databases_persists_test_url_and_runs_migrations(monkeypatch):
    configure_environment(monkeypatch)
    connection = Connection()
    engine = Engine(connection)
    persisted = []
    commands = []
    monkeypatch.setattr(setup_databases, "load_dotenv", lambda path: True)
    monkeypatch.setattr(setup_databases, "create_engine", lambda url: engine)
    monkeypatch.setattr(
        setup_databases,
        "set_key",
        lambda path, key, value: persisted.append((path, key, value)),
    )

    def run(arguments, **kwargs):
        commands.append((arguments, kwargs))
        return CompletedProcess(arguments, 0)

    monkeypatch.setattr(setup_databases.subprocess, "run", run)

    assert setup_databases.main() == 0

    assert [statement for statement, _ in connection.calls] == [
        "CREATE DATABASE IF NOT EXISTS `moffat_bay` CHARACTER SET utf8mb4 "
        "COLLATE utf8mb4_0900_ai_ci",
        "CREATE DATABASE IF NOT EXISTS `moffat_bay_test` CHARACTER SET utf8mb4 "
        "COLLATE utf8mb4_0900_ai_ci",
        "CREATE USER IF NOT EXISTS 'moffat_app'@'localhost' IDENTIFIED BY :password",
        "GRANT ALL PRIVILEGES ON `moffat_bay`.* TO 'moffat_app'@'localhost'",
        "GRANT ALL PRIVILEGES ON `moffat_bay_test`.* TO 'moffat_app'@'localhost'",
    ]
    assert connection.calls[2][1] == {"password": "application-password"}
    assert engine.disposed
    assert persisted == [
        (
            setup_databases.ENV_FILE,
            "TEST_DATABASE_URL",
            "mysql+pymysql://moffat_app:application-password@localhost:3306/moffat_bay_test",
        )
    ]
    assert [command for command, _ in commands] == [
        [setup_databases.sys.executable, "-m", "flask", "--app", "run.py", "init-db"],
        [setup_databases.sys.executable, "-m", "flask", "--app", "run.py", "db", "upgrade"],
    ]
    assert commands[0][1]["env"]["MYSQL_DATABASE"] == "moffat_bay"
    assert commands[1][1]["env"]["MYSQL_DATABASE"] == "moffat_bay_test"


def test_main_does_not_manage_the_root_account(monkeypatch):
    configure_environment(monkeypatch, MYSQL_USER="root", MYSQL_PASSWORD="root-password")
    connection = Connection()
    monkeypatch.setattr(setup_databases, "load_dotenv", lambda path: True)
    monkeypatch.setattr(setup_databases, "create_engine", lambda url: Engine(connection))
    monkeypatch.setattr(setup_databases, "set_key", lambda *arguments: None)
    monkeypatch.setattr(
        setup_databases.subprocess,
        "run",
        lambda arguments, **kwargs: CompletedProcess(arguments, 0),
    )

    assert setup_databases.main() == 0

    assert len(connection.calls) == 2


def test_main_requires_the_root_password(monkeypatch, capsys):
    configure_environment(monkeypatch)
    monkeypatch.delenv("MYSQL_ROOT_PASSWORD")
    monkeypatch.setattr(setup_databases, "load_dotenv", lambda path: True)

    assert setup_databases.main() == 1

    assert "MYSQL_ROOT_PASSWORD must be configured" in capsys.readouterr().err


def test_main_stops_after_a_failed_development_migration(monkeypatch, capsys):
    configure_environment(monkeypatch)
    connection = Connection()
    commands = []
    monkeypatch.setattr(setup_databases, "load_dotenv", lambda path: True)
    monkeypatch.setattr(setup_databases, "create_engine", lambda url: Engine(connection))
    monkeypatch.setattr(setup_databases, "set_key", lambda *arguments: None)

    def run(arguments, **kwargs):
        commands.append(arguments)
        return CompletedProcess(arguments, 7)

    monkeypatch.setattr(setup_databases.subprocess, "run", run)

    assert setup_databases.main() == 7

    assert len(commands) == 1
    assert "Database migration failed." in capsys.readouterr().err


def test_load_settings_rejects_invalid_database_name(monkeypatch):
    configure_environment(monkeypatch, MYSQL_DATABASE="moffat-bay")

    try:
        setup_databases.load_settings()
    except ValueError as error:
        assert str(error) == "MYSQL_DATABASE contains unsupported characters."
    else:
        raise AssertionError("Expected invalid MYSQL_DATABASE to be rejected.")
