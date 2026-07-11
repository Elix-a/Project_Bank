# src/external_api/external_api.py

import requests

# API Key for exchangerate.host (заменён API Apilayer)
API_KEY = "pin23uLFWYL1FY9S10330AuVlHq89ip9"


def convert_to_rub(transaction: dict) -> float:
    """
    Конвертирует сумму транзакции в рубли по курсу ЦБ РФ через exchangerate.host.

    Args:
        transaction (dict): Словарь с информацией о транзакции.
                            Ожидается ключ 'amount' (сумма) и 'currency' (код валюты).

    Returns:
        float: Сумма в рублях. Если валюта RUB, возвращает исходную сумму.
               Если конвертация не удалась, возвращает исходную сумму.
    """
    amount = transaction.get("amount", 0.0)
    currency = transaction.get("currency", "")

    if currency == "RUB":
        return float(amount)

    # Ссылка на API exchangerate.host
    url = "https://api.exchangerate.host/convert"
    params = {"from": currency, "to": "RUB", "amount": amount}
    headers = {"apikey": API_KEY}

    try:
        # Разбиваем длинный вызов на несколько строк
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()  # Проверяем статус ответа

        response_data = response.json()
        converted_amount = response_data.get("result")

        if converted_amount is not None:
            return float(converted_amount)
        else:
            # Если в ответе нет 'result', возвращаем исходную сумму
            return float(amount)

    except (requests.RequestException, ConnectionError):
        # Ловим все исключения, связанные с запросами (сетевые, таймаут и т.д.) и ConnectionError
        # и возвращаем исходную сумму
        return float(amount)
    except (ValueError, KeyError):
        # Ловим ошибки при парсинге JSON или отсутствии ключей
        # и возвращаем исходную сумму
        return float(amount)
