# src/utils/utils.py

from datetime import datetime
from typing import Any, Dict, List, Union


def get_transaction_by_id(transactions: List[Dict[str, Any]], transaction_id: Union[int, str]) -> Dict[str, Any]:
    """
    Находит транзакцию по её ID.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.
        transaction_id (Union[int, str]): ID транзакции для поиска.

    Returns:
        Dict[str, Any]: Найденная транзакция или пустой словарь, если не найдена.
    """
    for transaction in transactions:
        if transaction.get("id") == transaction_id:
            return transaction
    return {}  # Возвращаем пустой словарь, если транзакция не найдена


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по состоянию (state).

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.
        state (str, optional): Состояние для фильтрации. По умолчанию "EXECUTED".

    Returns:
        List[Dict[str, Any]]: Отфильтрованный список транзакций.
    """
    filtered_transactions = []
    for transaction in transactions:
        if transaction.get("state") == state:
            filtered_transactions.append(transaction)
    return filtered_transactions


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.
        reverse (bool, optional): Если True, сортировка по убыванию
            (новые первыми). Если False - по возрастанию.
            По умолчанию True.

    Returns:
        List[Dict[str, Any]]: Отсортированный список транзакций.
    """

    def get_date_key(transaction: Dict[str, Any]) -> datetime:
        date_str = transaction.get("date", "")
        if date_str:
            # Пытаемся преобразовать строку даты в объект datetime
            # Формат ISO 8601 с микросекундами и Z
            # Заменяем Z на +00:00 для совместимости
            normalized_date_str = date_str.replace("Z", "+00:00")
            try:
                return datetime.fromisoformat(normalized_date_str)
            except ValueError:
                # Если формат не подходит, возвращаем минимальную дату
                return datetime.min
        else:
            # Если дата отсутствует, возвращаем минимальную дату
            return datetime.min

    sorted_transactions = sorted(transactions, key=get_date_key, reverse=reverse)
    return sorted_transactions
