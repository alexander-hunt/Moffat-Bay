"""Print the contents of every table in the configured database."""

import sys
from pathlib import Path

from sqlalchemy import MetaData, Table, inspect, select
from sqlalchemy.exc import SQLAlchemyError

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT))

from moffat_bay import create_app  # noqa: E402
from moffat_bay.db import db  # noqa: E402


def format_table(table_name: str, column_names: list[str], rows: list[tuple]) -> str:
    """Format one table as readable, pipe-separated text."""
    values = [[str(value) if value is not None else "NULL" for value in row] for row in rows]
    widths = [len(name) for name in column_names]
    for row in values:
        widths = [max(width, len(value)) for width, value in zip(widths, row, strict=True)]

    lines = [f"Table: {table_name}"]
    lines.append(
        " | ".join(name.ljust(width) for name, width in zip(column_names, widths, strict=True))
    )
    lines.append("-+-".join("-" * width for width in widths))
    if values:
        lines.extend(
            " | ".join(value.ljust(width) for value, width in zip(row, widths, strict=True))
            for row in values
        )
    else:
        lines.append("(empty)")
    return "\n".join(lines)


def print_tables() -> None:
    """Print all tables from the configured database."""
    with db.engine.connect() as connection:
        inspector = inspect(connection)
        metadata = MetaData()
        table_names = sorted(inspector.get_table_names())

        for index, table_name in enumerate(table_names):
            table = Table(table_name, metadata, autoload_with=connection)
            result = connection.execute(select(table))
            rows = [tuple(row) for row in result]
            print(format_table(table_name, list(table.columns.keys()), rows))
            if index < len(table_names) - 1:
                print()


def main() -> int:
    """Run the table printer and return a process status code."""
    application = create_app()
    try:
        with application.app_context():
            print_tables()
    except SQLAlchemyError as error:
        print(f"Unable to read database tables: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
