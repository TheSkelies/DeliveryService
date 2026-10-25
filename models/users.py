from typing import List, Optional


class User:
    """Пользователь сервиса: отправитель или получатель посылки."""

    def __init__(self, user_id: int, name: str, email: str = "") -> None:
        """Создать объект пользователя.

        Args:
            user_id: уникальный идентификатор пользователя.
            name: имя пользователя.
            email: адрес электронной почты.
        """
        self.id: int = user_id
        self.name: str = name
        self.email: str = email

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        if self.email:
            return f"Пользователь #{self.id}: {self.name} ({self.email})"
        return f"Пользователь #{self.id}: {self.name}"

    @staticmethod
    def validate_name(name: str) -> bool:
        """Проверить корректность имени пользователя."""
        return bool(name and name.strip())

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из набора данных (например, из JSON)."""
        return cls(
            user_id=int(data["id"]),
            name=data["name"],
            email=data.get("email", ""),
        )


# ---------- Функции работы с коллекцией пользователей ----------

def add_user(users: List[User], user: User) -> None:
    """Добавить пользователя в коллекцию (если id не занят)."""
    if find_user_by_id(users, user.id) is not None:
        raise ValueError(f"Пользователь с id={user.id} уже существует")
    users.append(user)


def find_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user(users: List[User], query: str) -> List[User]:
    """Найти пользователей по подстроке имени или email."""
    query_lower = query.lower()
    return [
        user for user in users
        if query_lower in user.name.lower()
        or query_lower in user.email.lower()
    ]


def show_users(users: List[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Пользователи не найдены")
        return
    for user in users:
        print(user)