# src/generators/generators.py

from typing import Any, Dict, Iterator, List


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.

    Args:
        start (int): Начальный номер (включительно).
        end (int): Конечный номер (включительно).

    Yields:
        str: Следующий номер карты в формате XXXX XXXX XXXX XXXX.
    """
    for number in range(start, end + 1):
        # Форматирование: 16-значное число с ведущими нулями, разбитое на 4 группы по 4 цифры
        formatted_number = f"{number:016d}"  # Форматируем как 16-значное число с ведущими нулями
        yield f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:16]}"


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданному коду валюты.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.
        currency_code (str): Код валюты для фильтрации (например, 'USD', 'EUR').

    Yields:
        Dict[str, Any]: Транзакция, у которой 'currency_code' совпадает с заданным.
    """
    for transaction in transactions:
        # Предполагаем, что в транзакции есть ключ 'operationAmount' или 'currency_code'
        # Сначала пробуем 'operationAmount'
        op_amount = transaction.get("operationAmount", {})
        if op_amount.get("currency", {}).get("code") == currency_code:
            yield transaction
        # Если не нашли в operationAmount, пробуем напрямую в транзакции
        elif transaction.get("currency_code") == currency_code:
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
        yield transaction.get("description", "")  # Возвращаем описание или пустую строку, если ключ отсутствует
