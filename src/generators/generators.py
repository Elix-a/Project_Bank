def filter_by_currency(transactions: list[dict], currency_code: str):
    """
    Фильтрует транзакции по заданному коду валюты.

    Args:
        transactions: Список словарей транзакций.
        currency_code: Код валюты для фильтрации (например, "USD").

    Yields:
        Словарь транзакции, если валюта совпадает.
    """
    for transaction in transactions:
        # Проверяем, существует ли ключ 'operationAmount' и 'currency'
        if "operationAmount" in transaction and "currency" in transaction["operationAmount"]:
            if transaction["operationAmount"]["currency"]["code"] == currency_code:
                yield transaction

def transaction_descriptions(transactions: list[dict]):
    """
    Генерирует описания транзакций по очереди.

    Args:
        transactions: Список словарей транзакций.

    Yields:
        Строка с описанием транзакции.
    """
    for transaction in transactions:
        # Проверяем, существует ли ключ 'description'
        if "description" in transaction:
            yield transaction["description"]

def card_number_generator(start: int = 1, stop: int = 9999999999999999):
    """
    Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start: Начальное число для генерации (по умолчанию 1).
        stop: Конечное число для генерации (по умолчанию 9999999999999999).

    Yields:
        Строка с номером карты в формате XXXX XXXX XXXX XXXX.
    """
    for num in range(start, stop + 1):
        # Преобразуем число в строку, дополняем нулями до 16 символов
        padded_num = str(num).zfill(16)
        # Форматируем строку с пробелами
        formatted_num = f"{padded_num[0:4]} {padded_num[4:8]} {padded_num[8:12]} {padded_num[12:16]}"
        yield formatted_num
