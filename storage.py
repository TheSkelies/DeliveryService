import json
import os
from datetime import date
from typing import Any, Dict, List
from models.couriers import find_courier_by_id

from models import Package, User, Courier
from models.users import find_user_by_id
from models.packages import find_package_by_id



def _load_json(filename: str) -> Any:
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён. Создан новый.")
        return []


def _save_json(filename: str, data: Any) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:  # noqa: BLE001
        print(f"Ошибка при сохранении {filename}: {e}")


# ---------- Пользователи ----------

def load_users(filename: str) -> List[User]:
    """Загрузить пользователей из JSON в виде объектов User."""
    raw = _load_json(filename)
    return [User.from_data(item) for item in raw]


def save_users(filename: str, users: List[User]) -> None:
    """Сохранить пользователей в JSON."""
    data = [
        {"id": u.id, "name": u.name, "email": u.email}
        for u in users
    ]
    _save_json(filename, data)


# ---------- Посылки ----------

def load_packages(
    filename: str,
    users: list[User],
    couriers: list[Courier],
) -> list[Package]:
    raw = _load_json(filename)
    packages: list[Package] = []
    for item in raw:
        sender = (find_user_by_id(users, int(item["sender_id"]))
                  if item.get("sender_id") is not None else None)
        recipient = (find_user_by_id(users, int(item["recipient_id"]))
                     if item.get("recipient_id") is not None else None)
        courier = (find_courier_by_id(couriers, int(item["courier_id"]))
                   if item.get("courier_id") is not None else None)
        package = Package.from_data(item, sender, recipient, courier)
        packages.append(package)
        if courier is not None:
            courier.packages.append(package)
    return packages


def save_packages(filename: str, packages: list[Package]) -> None:
    data = [
        {
            "id": p.id,
            "category": p.category,
            "departure_date": p.departure_date.isoformat(),
            "arrival_date": p.arrival_date.isoformat(),
            "weight": p.weight,
            "status": p.status,
            "sender_id": p.sender.id if p.sender else None,
            "recipient_id": p.recipient.id if p.recipient else None,
            "courier_id": p.courier.id if p.courier else None,
        }
        for p in packages
    ]
    _save_json(filename, data)


# ---------- Доставщик ----------

def load_couriers(filename: str) -> list[Courier]:
    raw = _load_json(filename)
    return [Courier.from_data(item) for item in raw]


def save_couriers(filename: str, couriers: list[Courier]) -> None:
    data = [
        {
            "id": c.id,
            "name": c.name,
            "phone": c.phone,
            "vehicle": c.vehicle,
            "departure_date": c.departure_date.isoformat(),
            "expected_delivery_date": c.expected_delivery_date.isoformat(),
            "capacity_kg": c.capacity_kg,
            "is_available": c.is_available,
            "package_ids": [p.id for p in c.packages],
        }
        for c in couriers
    ]
    _save_json(filename, data)
