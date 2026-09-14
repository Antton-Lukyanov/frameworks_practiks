"""Вспомогательные функции безопасного ввода."""

from datetime import date


def input_str(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ввод не может быть пустым. Повторите.")


def input_int(prompt: str) -> int:
    """Запросить целое число с обработкой ошибок."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Некорректный ввод. Введите целое число.")


def input_float(prompt: str) -> float:
    """Запросить число с плавающей точкой с обработкой ошибок."""
    while True:
        try:
            return float(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("Некорректный ввод. Введите число.")


def input_date(prompt: str) -> str:
    """Запросить дату в формате ГГГГ-ММ-ДД с обработкой ошибок."""
    while True:
        raw = input(prompt).strip()
        try:
            return date.fromisoformat(raw).isoformat()
        except ValueError:
            print("Некорректный формат даты. Ожидается ГГГГ-ММ-ДД.")