from datetime import date

import pytest

from models import Courier, Package, User
from models.couriers import (
    add_courier,
    assign_package_to_best_courier,
    find_free_couriers,
)


@pytest.fixture
def courier():
    return Courier(
        courier_id=1,
        name="Сергей Иванов",
        phone="+79001234567",
        vehicle="car",
        departure_date=date(2026, 9, 18),
        expected_delivery_date=date(2026, 9, 20),
        capacity_kg=10.0,
    )


@pytest.fixture
def package():
    sender = User(1, "Иван", "i@e.ru")
    recipient = User(2, "Мария", "m@e.ru")
    return Package(
        package_id=1, category="Документы",
        departure_date=date(2026, 9, 15),
        arrival_date=date(2026, 9, 20),
        weight=0.5, status="New",
        sender=sender, recipient=recipient,
    )


def test_validate_phone():
    assert Courier.validate_phone("+7-900-123-45-67")
    assert not Courier.validate_phone("abc")


def test_can_take_package_date_mismatch(courier):
    p = Package(2, "x", date(2026, 9, 15), date(2026, 9, 25),
                1.0, "New")
    assert not courier.can_take_package(p)


def test_can_take_package_overweight(courier):
    p = Package(2, "x", date(2026, 9, 15), date(2026, 9, 20),
                20.0, "New")
    assert not courier.can_take_package(p)


def test_assign_and_release(courier, package):
    courier.assign_package(package)
    assert package in courier.packages
    assert package.courier is courier
    courier.release_package(package)
    assert package not in courier.packages
    assert package.courier is None


def test_assign_best_courier(courier, package):
    courier.is_available = False
    assert assign_package_to_best_courier([courier], package) is None
    courier.is_available = True
    assert assign_package_to_best_courier([courier], package) is courier


def test_find_free_couriers(courier):
    assert find_free_couriers([courier], date(2026, 9, 20)) == [courier]
    assert find_free_couriers([courier], date(2026, 9, 21)) == []


def test_add_duplicate_courier_raises(courier):
    with pytest.raises(ValueError):
        add_courier([courier], Courier(1, "x", "+7999", "foot",
                                       date.today(), date.today()))