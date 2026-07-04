import json
import os
from typing import Any, Dict, List


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
        Если файл не найден, пустой или содержит не список, возвращается пустой список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Проверяем, что данные — это список
            if isinstance(data, list):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        # Если файл не найден, поврежден или не может быть прочитан, возвращаем пустой список
        return []
