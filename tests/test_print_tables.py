from sqlalchemy import text

from moffat_bay import create_app
from moffat_bay.config import Config
from moffat_bay.db import db
from scripts.print_tables import format_table, print_tables


class SQLiteConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


def test_format_table_shows_empty_marker():
    output = format_table("room_type", ["room_type_id", "room_name"], [])

    assert "Table: room_type" in output
    assert "room_type_id | room_name" in output
    assert "(empty)" in output


def test_print_tables_discovers_and_prints_all_tables(capsys):
    application = create_app(SQLiteConfig)
    with application.app_context():
        db.session.execute(text("CREATE TABLE zeta (id INTEGER PRIMARY KEY, label TEXT)"))
        db.session.execute(text("CREATE TABLE alpha (id INTEGER PRIMARY KEY, label TEXT)"))
        db.session.execute(text("INSERT INTO zeta (label) VALUES ('last')"))
        db.session.commit()

        print_tables()

        db.session.rollback()
        db.session.execute(text("DROP TABLE zeta"))
        db.session.execute(text("DROP TABLE alpha"))
        db.session.commit()

    output = capsys.readouterr().out
    assert output.index("Table: alpha") < output.index("Table: zeta")
    assert "id | label" in output
    assert "last" in output
    assert "(empty)" in output
