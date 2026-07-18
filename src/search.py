# src/search.py

import re
from collections import Counter
from typing import Any, Dict, List


def search_by_description(transactions: List[Dict[str, Any]], search_str: str) -> List[Dict[str, Any]]:
    """
    Возвращает список транзакций, в описании которых содержится search_str.
    Поиск регистронезависимый, используется регулярное выражение (экранирование).
    """
    pattern = re.compile(re.escape(search_str), re.IGNORECASE)
    return [t for t in transactions if pattern.search(t.get("description", ""))]


def count_by_categories(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.
    Категория засчитывается, если её название (без учёта регистра) найдено в описании транзакции.
    """
    matched_categories = []
    for t in transactions:
        desc = t.get("description", "")
        for cat in categories:
            if re.search(re.escape(cat), desc, re.IGNORECASE):
                matched_categories.append(cat)
    return dict(Counter(matched_categories))
