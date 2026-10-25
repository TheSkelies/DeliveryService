import pytest

from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_user_str():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert "Иван Петров" in str(user)
    assert "ivan@example.com" in str(user)


def test_user_from_data():
    user = User.from_data(
        {"id": 5, "name": "Пётр", "email": "p@example.com"}
    )
    assert isinstance(user, User)
    assert user.id == 5
    assert user.name == "Пётр"


def test_add_and_find_user(sample_users):
    new_user = User(3, "Алексей", "alex@example.com")
    add_user(sample_users, new_user)
    assert find_user_by_id(sample_users, 3) is new_user
    assert find_user(sample_users, "алексей") == [new_user]


def test_add_duplicate_user_raises(sample_users):
    with pytest.raises(ValueError):
        add_user(sample_users, User(1, "Двойник", ""))