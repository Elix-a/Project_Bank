# src/readers.py

from typing import Any, Dict, List, cast

import pandas as pd


def read_transactions_from_csv(csv_file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла и возвращает список словарей.

    Args:
        csv_file_path (str): Путь к CSV-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей, представляющих транзакции.
                              Каждый словарь соответствует одной строке в CSV-файле.
                              Возвращается пустой список, если файл не найден, пуст или содержит ошибки формата.
    """
    try:
        df = pd.read_csv(csv_file_path)
        transactions_list_raw = df.to_dict(orient="records")
        transactions_list: List[Dict[str, Any]] = cast(List[Dict[str, Any]], transactions_list_raw)
        return transactions_list
    except FileNotFoundError:
        return []
    except pd.errors.EmptyDataError:
        return []
    except (OSError, pd.errors.ParserError, UnicodeDecodeError, ValueError, RuntimeError):
        return []


def read_transactions_from_excel(excel_file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла и возвращает список словарей.

    Args:
        excel_file_path (str): Путь к Excel-файлу (.xlsx).

    Returns:
        List[Dict[str, Any]]: Список словарей, представляющих транзакции.
                              Каждый словарь соответствует одной строке в Excel-файле.
                              Возвращается пустой список, если файл не найден, пуст или содержит ошибки формата.
    """
    try:
        df = pd.read_excel(excel_file_path)
        transactions_list_raw = df.to_dict(orient="records")
        transactions_list: List[Dict[str, Any]] = cast(List[Dict[str, Any]], transactions_list_raw)
        return transactions_list
    except FileNotFoundError:
        return []
    except pd.errors.EmptyDataError:
        return []
    except (OSError, pd.errors.ParserError, UnicodeDecodeError, ValueError, RuntimeError):
        return []
