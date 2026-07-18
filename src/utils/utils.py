# src/utils/utils.py

import os
from datetime import datetime
from typing import Any, Dict, List, Union

import pandas as pd


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
            normalized_date_str = date_str.replace("Z", "+00:00")
            try:
                return datetime.fromisoformat(normalized_date_str)
            except ValueError:
                return datetime.min
        else:
            return datetime.min

    sorted_transactions = sorted(transactions, key=get_date_key, reverse=reverse)
    return sorted_transactions


def load_transactions_from_xlsx(file_path: str) -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла.
    Возвращает DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    df = pd.read_excel(file_path)
    # Приводим дату операции к datetime
    if "Дата операции" in df.columns:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True, errors="coerce")
    return df


def greeting_by_time(dt: datetime) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.
    dt: datetime-объект.
    """
    hour = dt.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def filter_transactions_by_date(df: pd.DataFrame, target_date_str: str) -> pd.DataFrame:
    """
    Оставляет транзакции с начала месяца, на который выпадает target_date_str, по саму дату включительно.
    target_date_str: строка в формате 'YYYY-MM-DD HH:MM:SS' (можно и просто 'YYYY-MM-DD').
    """
    target_date = pd.to_datetime(target_date_str)
    start_of_month = target_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_day = target_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    mask = (df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= end_of_day)
    return df.loc[mask].copy()
