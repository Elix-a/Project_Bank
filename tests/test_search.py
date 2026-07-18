# tests/test_search.py

from typing import Any, Dict, List

from src.search import count_by_categories, search_by_description


def test_search_by_description_found() -> None:
    transactions: List[Dict[str, Any]] = [
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты"},
        {"description": "Оплата услуг"},
    ]
    result = search_by_description(transactions, "открытие")
    assert len(result) == 1
    assert result[0]["description"] == "Открытие вклада"


def test_search_by_description_not_found() -> None:
    transactions = [{"description": "Тест"}]
    result = search_by_description(transactions, "нет")
    assert result == []


def test_search_by_description_case_insensitive() -> None:
    transactions = [{"description": "ОТКРЫТИЕ ВКЛАДА"}]
    result = search_by_description(transactions, "открытие")
    assert len(result) == 1


def test_count_by_categories() -> None:
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Открытие вклада"},
        {"description": "Перевод со счета на счет"},
    ]
    categories = ["Перевод", "Открытие"]
    counts = count_by_categories(transactions, categories)
    assert counts == {"Перевод": 3, "Открытие": 1}


def test_count_by_categories_case_insensitive() -> None:
    transactions = [{"description": "ПЕРЕВОД НА КАРТУ"}]
    categories = ["перевод"]
    counts = count_by_categories(transactions, categories)
    assert counts == {"перевод": 1}


def test_count_by_categories_no_match() -> None:
    transactions = [{"description": "Оплата услуг"}]
    categories = ["Перевод"]
    counts = count_by_categories(transactions, categories)
    assert counts == {}
