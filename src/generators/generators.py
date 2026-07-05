# src/generators/generators.py

import random


def filter_by_currency(transactions, currency_code):
    """Фильтрует список транзакций по заданному коду валюты."""
    for transaction in transactions:
        # Проверяем, существует ли 'operationAmount' и 'currency', и совпадает ли код
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions):
    """Генерирует описания транзакций."""
    for transaction in transactions:
        # Получаем описание, возвращаем 'No Description', если ключ отсутствует
        description = transaction.get("description", "No Description")
        yield description


def card_number_generator(start, stop):
    """Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX."""
    # Используем random.randint для генерации случайного числа в диапазоне
    for _ in range(start, stop + 1):  # Включаем stop в диапазон
        # Генерируем 16-значное число
        number = random.randint(0, 9999999999999999)
        # Форматируем число, добавляя ведущие нули до 16 цифр
        formatted_number = f"{number:016d}"
        # Разбиваем на группы по 4 цифры
        chunked_number = " ".join([formatted_number[i : i + 4] for i in range(0, len(formatted_number), 4)])
        yield chunked_number
