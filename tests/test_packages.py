from datetime import date

import pytest

from models import Package, User
from models.packages import (
    DEFAULT_STATUS,
    add_package,
    change_package_status,
    filter_packages_by_category,
    find_package_by_id,
    get_package_status,
    sort_packages_by_weight,
)


def test_package_creation(sample_package):
    assert sample_package.id == 1
    assert sample_package.sender.name == "Иван Петров"
    assert sample_package.recipient.name == "Мария Сидорова"


def test_package_str_contains_sender_and_recipient(sample_package):
    text = str(sample_package)
    assert "Иван Петров" in text
    assert "Мария Сидорова" in text
    assert "Документы" in text


def test_package_change_status(sample_package):
    sample_package.change_status("Delivered")
    assert sample_package.status == "Delivered"
    assert sample_package.is_delivered()


def test_package_change_status_empty_raises(sample_package):
    with pytest.raises(ValueError):
        sample_package.change_status("")


def test_package_validate_weight():
    assert Package.validate_weight(1.5)
    assert not Package.validate_weight(0)


def test_add_package_and_find(sample_users, sample_package):
    packages = []
    add_package(packages, sample_package)
    assert find_package_by_id(packages, 1) is sample_package


def test_get_package_status(sample_users, sample_package):
    packages = [sample_package]
    assert get_package_status(packages, 1) == DEFAULT_STATUS
    assert get_package_status(packages, 999) is None


def test_change_package_status(sample_package):
    packages = [sample_package]
    assert change_package_status(packages, 1, "In transit")
    assert sample_package.status == "In transit"
    assert not change_package_status(packages, 999, "x")


def test_filter_by_category(sample_package):
    other = Package(
        package_id=2,
        category="Одежда",
        departure_date=date(2026, 10, 1),
        arrival_date=date(2026, 10, 5),
        weight=2.0,
        status=DEFAULT_STATUS,
        sender=None,
        recipient=None,
    )
    result = filter_packages_by_category(
        [sample_package, other], "документы"
    )
    assert result == [sample_package]


def test_sort_by_weight(sample_package):
    heavy = Package(
        package_id=3,
        category="Книги",
        departure_date=date(2026, 10, 1),
        arrival_date=date(2026, 10, 5),
        weight=5.0,
        status=DEFAULT_STATUS,
        sender=None,
        recipient=None,
    )
    assert sort_packages_by_weight([heavy, sample_package]) == [
        sample_package, heavy
    ]