import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv  # <-- Убираем неиспользуемые imports и исправляем импорт

# Загрузите переменные из .env файла (если он существует)
load_dotenv()

# Получаем API-ключ из переменных окружения
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (Dict[str, Any]): Словарь с данными о транзакции.
            Должен содержать ключи 'amount' (float) и 'currency' (str).

    Returns:
        float: Сумма транзакции в рублях.
        Если валюта не USD/EUR, возвращается исходная сумма.
    """
    amount = transaction.get("amount", 0.0)
    currency = transaction.get("currency", "").upper()

    # Если валюта уже RUB, возвращаем сумму как есть
    if currency == "RUB":
        return float(amount)

    # Для USD и EUR делаем запрос к API
    if currency in ("USD", "EUR"):
        url = "https://api.apilayer.com/exchangerates_data/convert"
        params = {"from": currency, "to": "RUB", "amount": amount}
        headers = {"apikey": API_KEY}  # <-- API_KEY может быть загружен из .env

        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
            response.raise_for_status()  # Вызовет исключение при 4xx/5xx
            data = response.json()
            # Извлекаем результат конвертации
            return float(data.get("result", amount))
        except (requests.exceptions.RequestException, KeyError, ValueError, TypeError):
            # При любой ошибке (сеть, API, парсинг) возвращаем исходную сумму
            return float(amount)

    # Для всех остальных валют возвращаем исходную сумму
    return float(amount)
