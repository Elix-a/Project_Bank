from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей с транзакциями по ключу 'state'.

    Args:
        transactions: Список словарей, представляющих транзакции.
                      Каждый словарь должен иметь ключ 'state'.
        state: Значение статуса для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        Новый список, содержащий только те словари, у которых ключ 'state'
        соответствует указанному значению.
    """
    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], ascending: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей с транзакциями по ключу 'date'.

    Args:
        transactions: Список словарей, представляющих транзакции.
                      Каждый словарь должен иметь ключ 'date' в формате ISO
                      (например, 'YYYY-MM-DDTHH:MM:SS.ssssss').
        ascending: Если True, сортирует по возрастанию (сначала старые).
                   Если False (по умолчанию), сортирует по убыванию (сначала новые).

    Returns:
        Новый список, отсортированный по дате.
    """

    def get_datetime(transaction: Dict[str, Any]) -> datetime:
        date_str = transaction.get("date", "")
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            # Возвращаем минимальную дату, если парсинг не удался
            return datetime.min

    # Аргумент 'reverse' для sorted() противоположен флагу 'ascending'
    return sorted(transactions, key=get_datetime, reverse=not ascending)
