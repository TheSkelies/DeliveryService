from datetime import date
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .packages import Package


class Courier:
    """Доставщик посылок."""

    def __init__(
        self,
        courier_id: int,
        name: str,
        phone: str,
        vehicle: str,
        departure_date: date,
        expected_delivery_date: date,
        capacity_kg: float = 50.0,
        is_available: bool = True,
    ) -> None:
        """Создать объект доставщика.

        Args:
            courier_id: идентификатор доставщика.
            name: имя.
            phone: телефон.
            vehicle: транспорт (car/bike/foot).
            departure_date: дата выезда.
            expected_delivery_date: примерная дата доставки.
            capacity_kg: максимальный вес за рейс, кг.
            is_available: доступен ли доставщик.
        """
        self.id: int = courier_id
        self.name: str = name
        self.phone: str = phone
        self.vehicle: str = vehicle
        self.departure_date: date = departure_date
        self.expected_delivery_date: date = expected_delivery_date
        self.capacity_kg: float = capacity_kg
        self.is_available: bool = is_available
        self.packages: List["Package"] = []

    def __str__(self) -> str:
        return (
            f"Доставщик #{self.id}: {self.name}, тел. {self.phone}, "
            f"транспорт: {self.vehicle}, "
            f"выезд: {self.departure_date}, "
            f"примерная доставка: {self.expected_delivery_date}, "
            f"загрузка: {self.total_weight()}/{self.capacity_kg} кг, "
            f"посылок: {len(self.packages)}, "
            f"{'свободен' if self.is_available else 'занят'}"
        )

    # ---------- поведение ----------

    def total_weight(self) -> float:
        """Суммарный вес назначенных посылок."""
        return sum(p.weight for p in self.packages)

    def can_take_package(self, package: "Package") -> bool:
        """Может ли доставщик взять посылку."""
        if not self.is_available:
            return False
        if package.arrival_date != self.expected_delivery_date:
            return False
        if self.total_weight() + package.weight > self.capacity_kg:
            return False
        return True

    def assign_package(self, package: "Package") -> None:
        """Назначить посылку доставщику (двусторонняя связь)."""
        if not self.can_take_package(package):
            raise ValueError(
                f"Доставщик #{self.id} не может взять посылку #{package.id}"
            )
        self.packages.append(package)
        package.courier = self

    def release_package(self, package: "Package") -> None:
        """Снять посылку с доставщика."""
        if package in self.packages:
            self.packages.remove(package)
        if package.courier is self:
            package.courier = None

    # ---------- static / class методы ----------

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Простая проверка телефона: только цифры и +, не короче 5 символов."""
        cleaned = phone.replace("+", "").replace(" ", "").replace("-", "")
        return cleaned.isdigit() and len(cleaned) >= 5

    @classmethod
    def from_data(cls, data: dict) -> "Courier":
        """Создать доставщика из данных JSON."""
        return cls(
            courier_id=int(data["id"]),
            name=data["name"],
            phone=data["phone"],
            vehicle=data["vehicle"],
            departure_date=date.fromisoformat(data["departure_date"]),
            expected_delivery_date=date.fromisoformat(
                data["expected_delivery_date"]
            ),
            capacity_kg=float(data.get("capacity_kg", 50.0)),
            is_available=bool(data.get("is_available", True)),
        )


# ---------- функции работы с коллекцией доставщиков ----------

def add_courier(couriers: List[Courier], courier: Courier) -> None:
    """Добавить доставщика в коллекцию."""
    if find_courier_by_id(couriers, courier.id) is not None:
        raise ValueError(f"Доставщик с id={courier.id} уже существует")
    couriers.append(courier)


def find_courier_by_id(couriers: List[Courier],
                       courier_id: int) -> Optional[Courier]:
    """Найти доставщика по id."""
    for c in couriers:
        if c.id == courier_id:
            return c
    return None


def find_free_couriers(couriers: List[Courier],
                       delivery_date: date) -> List[Courier]:
    """Найти свободных доставщиков на дату доставки."""
    return [
        c for c in couriers
        if c.is_available and c.expected_delivery_date == delivery_date
    ]


def assign_package_to_best_courier(
    couriers: List[Courier], package: "Package"
) -> Optional[Courier]:
    """Выбрать первого доставщика, который может взять посылку."""
    for courier in couriers:
        if courier.can_take_package(package):
            courier.assign_package(package)
            return courier
    return None


def show_couriers(couriers: List[Courier]) -> None:
    """Вывести список доставщиков."""
    if not couriers:
        print("Доставщики не найдены")
        return
    for courier in couriers:
        print(courier)