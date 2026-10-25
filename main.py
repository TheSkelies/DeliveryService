import os
from datetime import date
from typing import List, Optional

from models import Package, User, Courier
from models.packages import (
    DEFAULT_STATUS,
    add_package,
    change_package_status,
    filter_packages_by_category,
    find_package_by_id,
    get_all_packages,
    get_package_status,
    show_packages,
    sort_packages_by_weight,
)
from models.couriers import (
    add_courier,
    assign_package_to_best_courier,
    find_courier_by_id,
    show_couriers,
)
from storage import (
    load_couriers,
    load_packages,
    load_users,
    save_couriers,
    save_packages,
    save_users,
)
from models.users import add_user, find_user, find_user_by_id, show_users
from storage import load_packages, load_users, save_packages, save_users
from utils.input_utils import input_date, input_float, input_int

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PACKAGES_FILE = os.path.join(DATA_DIR, "packages.json")
COURIERS_FILE = os.path.join(DATA_DIR, "couriers.json")


def create_new_package(packages: List[Package], users: List[User]) -> None:
    """Сценарий создания посылки с участием объектов User и Package."""
    if not users:
        print("Сначала добавьте хотя бы одного пользователя")
        return

    show_users(users)

    sender_id = input_int("ID отправителя: ")
    sender = find_user_by_id(users, sender_id)
    if sender is None:
        print("Отправитель не найден")
        return

    recipient_id = input_int("ID получателя: ")
    recipient = find_user_by_id(users, recipient_id)
    if recipient is None:
        print("Получатель не найден")
        return

    category = input("Категория: ")
    arrival_date = input_date("Дата прибытия (YYYY-MM-DD): ")
    weight = input_float("Вес (кг): ")

    if not Package.validate_weight(weight):
        print("Вес должен быть положительным")
        return

    package_id = max((p.id for p in packages), default=0) + 1
    package = Package(
        package_id=package_id,
        category=category,
        departure_date=date.today(),
        arrival_date=arrival_date,
        weight=weight,
        status=DEFAULT_STATUS,
        sender=sender,
        recipient=recipient,
    )
    add_package(packages, package)
    print(f"Посылка создана:\n{package}")


def find_packages_menu(packages: List[Package]) -> None:
    print("1 - по id\n2 - по категории")
    choice = input("Выбор: ")
    if choice == "1":
        package_id = input_int("ID посылки: ")
        package = find_package_by_id(packages, package_id)
        print(package if package else "Посылка не найдена")
    elif choice == "2":
        category = input("Категория: ")
        show_packages(filter_packages_by_category(packages, category))
    else:
        print("Неверный выбор")


# ---------- сценарий назначения курьера ----------

def assign_courier_to_package(packages: list[Package],
                              couriers: list[Courier]) -> None:
    """Назначить курьера на ещё не назначенную посылку."""
    package_id = input_int("ID посылки: ")
    package = find_package_by_id(packages, package_id)
    if package is None:
        print("Посылка не найдена")
        return
    if package.courier is not None:
        print(f"Посылка уже закреплена за {package.courier.name}")
        return
    courier = assign_package_to_best_courier(couriers, package)
    if courier is None:
        print("Нет подходящего свободного доставщика на эту дату")
    else:
        print(f"Посылка #{package.id} назначена: {courier.name}")


def main() -> None:
    users = load_users(USERS_FILE)
    couriers = load_couriers(COURIERS_FILE)
    packages = load_packages(PACKAGES_FILE, users, couriers)

    while True:
        print(
            "\n0 - выход"
            "\n1 - добавить пользователя"
            "\n2 - показать пользователей"
            "\n3 - добавить доставщика"
            "\n4 - показать доставщиков"
            "\n5 - создать посылку"
            "\n6 - найти посылку"
            "\n7 - все посылки"
            "\n8 - посылки по весу"
            "\n9 - статус посылки"
            "\n10 - изменить статус"
            "\n11 - назначить доставщика"
        )
        choice = input("Выбор: ")

        if choice == "0":
            break
        elif choice == "1":
            user_id = max((u.id for u in users), default=0) + 1
            name = input("Имя: ")
            email = input("Email (необязательно): ")
            if not User.validate_name(name):
                print("Некорректное имя")
                continue
            add_user(users, User(user_id, name, email))
        elif choice == "2":
            show_users(users)
        elif choice == "3":
            courier_id = max((c.id for c in couriers), default=0) + 1
            name = input("Имя доставщика: ")
            phone = input("Телефон: ")
            if not Courier.validate_phone(phone):
                print("Некорректный телефон")
                continue
            vehicle = input("Транспорт (car/bike/foot): ") or "foot"
            departure = input_date("Дата выезда (YYYY-MM-DD): ")
            delivery = input_date("Примерная дата доставки: ")
            capacity = input_float("Грузоподъёмность, кг: ")
            add_courier(
                couriers,
                Courier(courier_id, name, phone, vehicle,
                        departure, delivery, capacity),
            )
            print("Доставщик добавлен")
        elif choice == "4":
            show_couriers(couriers)
        elif choice == "5":
            create_new_package(packages, users)
        elif choice == "6":
            find_packages_menu(packages)
        elif choice == "7":
            show_packages(get_all_packages(packages))
        elif choice == "8":
            show_packages(sort_packages_by_weight(packages))
        elif choice == "9":
            package_id = input_int("ID посылки: ")
            status: Optional[str] = get_package_status(packages, package_id)
            print(status if status else "Посылка не найдена")
        elif choice == "10":
            package_id = input_int("ID посылки: ")
            new_status = input("Новый статус: ")
            if change_package_status(packages, package_id, new_status):
                print("Статус изменён")
            else:
                print("Посылка не найдена")
        elif choice == "11":
            assign_courier_to_package(packages, couriers)
        else:
            print("Неверный выбор")

    save_users(USERS_FILE, users)
    save_couriers(COURIERS_FILE, couriers)
    save_packages(PACKAGES_FILE, packages)


if __name__ == "__main__":
    main()