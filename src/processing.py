# src/processing.py

from typing import Any, Dict, Iterator, List  # Union удалён


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданному коду валюты, используя поле currency_code на верхнем уровне.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.
        currency_code (str): Код валюты для фильтрации (например, 'USD', 'EUR').

    Yields:
        Dict[str, Any]: Транзакция, у которой 'currency_code' совпадает с заданным.
    """
    for transaction in transactions:
        # Ищем currency_code на верхнем уровне, как в MOCK_TRANSACTIONS
        if transaction.get("currency_code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Извлекает описания транзакций.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.

    Yields:
        str: Описание транзакции.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.
    Числа обрезаются до 16 знаков для форматирования.

    Args:
        start (int): Начальный номер (включительно).
        end (int): Конечный номер (включительно).

    Yields:
        str: Следующий номер карты в формате XXXX XXXX XXXX XXXX.
    """
    for number in range(start, end + 1):
        # Обрезаем число до 16 знаков, чтобы избежать чисел > 16 символов
        # 10**16 = 10000000000000000, 10**16 - 1 = 9999999999999999
        # number % (10**16) даст остаток от деления, гарантируя <= 9999999999999999
        truncated_number = number % (10**16)
        # Форматирование: 16-значное число с ведущими нулями, разбитое на 4 группы по 4 цифры
        formatted_number = f"{truncated_number:016d}"  # Форматируем как 16-значное число с ведущими нулями
        yield f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:16]}"
