import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "delivery.sqlite"


def main() -> None:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        for (table_name,) in tables:
            print(f"\nТаблица: {table_name}")
            columns = connection.execute(
                f'PRAGMA table_info("{table_name}")'
            ).fetchall()
            for column in columns:
                print(
                    f"  имя={column['name']}, тип={column['type']}, "
                    f"NOT NULL={column['notnull']}, PK={column['pk']}"
                )
            count = connection.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            ).fetchone()[0]
            print(f"  Записей: {count}")


if __name__ == "__main__":
    main()