import json

from db.database import get_connection

USERS_FILE = "data/users.json"
COURIERS_FILE = "data/couriers.json"
PACKAGES_FILE = "data/packages.json"


def load_json(filename: str):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_users(conn) -> None:
    users = load_json(USERS_FILE)
    conn.executemany(
        "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
        [(u["id"], u["name"], u.get("email", "")) for u in users],
    )


def import_couriers(conn) -> None:
    couriers = load_json(COURIERS_FILE)
    conn.executemany(
        """
        INSERT INTO couriers (
            id, name, phone, vehicle,
            departure_date, expected_delivery_date,
            capacity_kg, is_available
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                c["id"],
                c["name"],
                c["phone"],
                c["vehicle"],
                c["departure_date"],
                c["expected_delivery_date"],
                float(c["capacity_kg"]),
                int(c.get("is_available", True)),
            )
            for c in couriers
        ],
    )


def import_packages(conn) -> None:
    packages = load_json(PACKAGES_FILE)
    conn.executemany(
        """
        INSERT INTO packages (
            id, category, departure_date, arrival_date,
            weight, status, sender_id, recipient_id, courier_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                p["id"],
                p["category"],
                p["departure_date"],
                p["arrival_date"],
                float(p["weight"]),
                p["status"],
                p.get("sender_id"),
                p.get("recipient_id"),
                p.get("courier_id"),
            )
            for p in packages
        ],
    )


def main() -> None:
    conn = get_connection()
    try:
        import_users(conn)
        import_couriers(conn)
        import_packages(conn)
        conn.commit()
        print("Импорт завершён успешно")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()