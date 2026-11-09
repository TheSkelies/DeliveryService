import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

SOURCE_DB = BASE_DIR / "data" / "delivery.sqlite"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parcel_service.settings")
django.setup()

from django.db import transaction  # noqa: E402

from couriers.models import Courier  # noqa: E402
from packages.models import Package  # noqa: E402
from users.models import User  # noqa: E402


def main() -> None:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row

        users = connection.execute(
            "SELECT id, name, email FROM users ORDER BY id"
        ).fetchall()
        couriers = connection.execute(
            """
            SELECT id, name, phone, vehicle,
                   departure_date, expected_delivery_date,
                   capacity_kg, is_available
            FROM couriers
            ORDER BY id
            """
        ).fetchall()
        packages = connection.execute(
            """
            SELECT id, category, departure_date, arrival_date,
                   weight, status, sender_id, recipient_id, courier_id
            FROM packages
            ORDER BY id
            """
        ).fetchall()

    with transaction.atomic():
        for row in users:
            User.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "email": row["email"] or "",
                },
            )

        for row in couriers:
            Courier.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "phone": row["phone"],
                    "vehicle": row["vehicle"],
                    "departure_date": date.fromisoformat(row["departure_date"]),
                    "expected_delivery_date": date.fromisoformat(
                        row["expected_delivery_date"]
                    ),
                    "capacity_kg": float(row["capacity_kg"]),
                    "is_available": bool(row["is_available"]),
                },
            )

        for row in packages:
            Package.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "category": row["category"],
                    "departure_date": date.fromisoformat(row["departure_date"]),
                    "arrival_date": date.fromisoformat(row["arrival_date"]),
                    "weight": float(row["weight"]),
                    "status": row["status"],
                    "sender_id": row["sender_id"],
                    "recipient_id": row["recipient_id"],
                    "courier_id": row["courier_id"],
                },
            )

    print("Перенос завершён.")
    print(f"Пользователей: {User.objects.count()}")
    print(f"Доставщиков: {Courier.objects.count()}")
    print(f"Посылок: {Package.objects.count()}")


if __name__ == "__main__":
    main()