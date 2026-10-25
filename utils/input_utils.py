from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить целое число с повторением при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число")


def input_float(prompt: str) -> float:
    """Запросить число с плавающей точкой."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число")


def input_date(prompt: str) -> date:
    """Запросить дату в формате YYYY-MM-DD."""
    while True:
        try:
            return datetime.strptime(input(prompt), "%Y-%m-%d").date()
        except ValueError:
            print("Ошибка: дата должна быть в формате YYYY-MM-DD")