from datetime import date
from typing import List, Optional, TYPE_CHECKING

from .users import User

if TYPE_CHECKING:
    from .couriers import Courier

DEFAULT_STATUS = "Package at the drop-off point"


class Package:
    """Посылка, отправляемая пользователем другому пользователю."""

    def __init__(
        self,
        package_id: int,
        category: str,
        departure_date: date,
        arrival_date: date,
        weight: float,
        status: str,
        sender: Optional[User] = None,
        recipient: Optional[User] = None,
        courier: Optional["Courier"] = None,
    ) -> None:
        """Создать объект посылки.

        Args:
            package_id: уникальный идентификатор посылки.
            category: категория посылки.
            departure_date: дата отправления.
            arrival_date: ожидаемая дата прибытия.
            weight: вес посылки в кг.
            status: текущий статус.
            sender: объект User-отправитель (ссылка, а не id).
            recipient: объект User-получатель (ссылка, а не id).
        """
        self.id: int = package_id
        self.category: str = category
        self.departure_date: date = departure_date
        self.arrival_date: date = arrival_date
        self.weight: float = weight
        self.status: str = status
        self.sender: Optional[User] = sender
        self.recipient: Optional[User] = recipient
        self.courier = courier

    def __str__(self) -> str:
        sender = self.sender.name if self.sender else "—"
        recipient = self.recipient.name if self.recipient else "—"
        courier = self.courier.name if self.courier else "не назначен"
        return (
            f"Посылка #{self.id} [{self.category}] {sender} -> {recipient}, "
            f"вес: {self.weight} кг, доставка: {self.arrival_date}, "
            f"курьер: {courier}, статус: {self.status}"
        )

    def change_status(self, new_status: str) -> None:
        """Изменить статус посылки."""
        if not new_status.strip():
            raise ValueError("Статус не может быть пустым")
        self.status = new_status

    def is_delivered(self) -> bool:
        """Проверить, доставлена ли посылка."""
        return "delivered" in self.status.lower()

    @staticmethod
    def validate_weight(weight: float) -> bool:
        """Проверить корректность веса посылки."""
        return weight > 0

    @classmethod
    def from_data(
        cls,
        data: dict,
        sender: Optional[User],
        recipient: Optional[User],
        courier: Optional["Courier"] = None,
    ) -> "Package":
        return cls(
            package_id=int(data["id"]),
            category=data["category"],
            departure_date=date.fromisoformat(data["departure_date"]),
            arrival_date=date.fromisoformat(data["arrival_date"]),
            weight=float(data["weight"]),
            status=data["status"],
            sender=sender,
            recipient=recipient,
            courier=courier,
        )


# ---------- Функции работы с коллекцией посылок ----------

def add_package(packages: List[Package], package: Package) -> None:
    """Добавить посылку в коллекцию."""
    if find_package_by_id(packages, package.id) is not None:
        raise ValueError(f"Посылка с id={package.id} уже существует")
    packages.append(package)


def find_package_by_id(packages: List[Package],
                       package_id: int) -> Optional[Package]:
    """Найти посылку по идентификатору."""
    for package in packages:
        if package.id == package_id:
            return package
    return None


def get_all_packages(packages: List[Package]) -> List[Package]:
    """Вернуть список всех посылок."""
    return list(packages)


def get_package_status(packages: List[Package],
                       package_id: int) -> Optional[str]:
    """Вернуть статус посылки по её идентификатору."""
    package = find_package_by_id(packages, package_id)
    if package is None:
        return None
    return package.status


def change_package_status(packages: List[Package], package_id: int,
                          new_status: str) -> bool:
    """Изменить статус посылки. Вернуть True при успехе."""
    package = find_package_by_id(packages, package_id)
    if package is None:
        return False
    package.change_status(new_status)
    return True


def filter_packages_by_category(packages: List[Package],
                                category: str) -> List[Package]:
    """Отобрать посылки по категории."""
    category_lower = category.lower()
    return [p for p in packages if p.category.lower() == category_lower]


def sort_packages_by_weight(packages: List[Package]) -> List[Package]:
    """Отсортировать посылки по весу (по возрастанию)."""
    return sorted(packages, key=lambda p: p.weight)


def show_packages(packages: List[Package]) -> None:
    """Вывести список посылок."""
    if not packages:
        print("Посылки не найдены")
        return
    for package in packages:
        print(package)