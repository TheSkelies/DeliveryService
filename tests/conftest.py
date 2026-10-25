import pytest

from models import Package, User


@pytest.fixture
def sample_users():
    """Два пользователя для тестов."""
    return [
        User(1, "Иван Петров", "ivan@example.com"),
        User(2, "Мария Сидорова", "maria@example.com"),
    ]


@pytest.fixture
def sample_package(sample_users):
    """Готовая посылка с привязанными объектами User."""
    from datetime import date
    return Package(
        package_id=1,
        category="Документы",
        departure_date=date(2026, 9, 15),
        arrival_date=date(2026, 9, 20),
        weight=0.5,
        status="Package at the drop-off point",
        sender=sample_users[0],
        recipient=sample_users[1],
    )