# tests/test_processing.py

import json
from pathlib import Path
from typing import Any, Dict, List, cast

import pandas as pd

from src.generators.generators import card_number_generator, filter_by_currency, transaction_descriptions
from src.processing import load_transactions_from_json

# Пример данных для мока
MOCK_DF = pd.DataFrame(
    [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T00:00:00.000000",
            "amount": 100.0,
            "currency_name": "RUB",
            "currency_code": "RUB",
            "description": "Payment",
            "from": "",
            "to": "Account 12345",
        },
        {
            "id": 2,
            "state": "CANCELLED",
            "date": "2023-01-02T00:00:00.000000",
            "amount": 200.0,
            "currency_name": "USD",
            "currency_code": "USD",
            "description": "Transfer",
            "from": "Card 6789",
            "to": "Account 67890",
        },
    ]
)

MOCK_TRANSACTIONS: List[Dict[str, Any]] = cast(List[Dict[str, Any]], MOCK_DF.to_dict(orient="records"))
MOCK_EXCEL_DATA = MOCK_DF


def test_filter_by_currency_usd() -> None:
    """Тестирует фильтрацию транзакций по валюте USD."""
    result = list(filter_by_currency(MOCK_TRANSACTIONS, "USD"))
    expected_filtered = [
        {
            "id": 2,
            "state": "CANCELLED",
            "date": "2023-01-02T00:00:00.000000",
            "amount": 200.0,
            "currency_name": "USD",
            "currency_code": "USD",
            "description": "Transfer",
            "from": "Card 6789",
            "to": "Account 67890",
        }
    ]
    assert result == expected_filtered


def test_filter_by_currency_rub() -> None:
    """Тестирует фильтрацию транзакций по валюте RUB."""
    result = list(filter_by_currency(MOCK_TRANSACTIONS, "RUB"))
    expected_filtered = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T00:00:00.000000",
            "amount": 100.0,
            "currency_name": "RUB",
            "currency_code": "RUB",
            "description": "Payment",
            "from": "",
            "to": "Account 12345",
        }
    ]
    assert result == expected_filtered


def test_transaction_descriptions() -> None:
    """Тестирует извлечение описаний транзакций."""
    result = list(transaction_descriptions(MOCK_TRANSACTIONS))
    expected = ["Payment", "Transfer"]
    assert result == expected


def test_card_number_generator() -> None:
    """Тестирует генерацию номеров карт."""
    result = list(card_number_generator(1, 3))
    expected = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
    assert result == expected


def test_filter_by_currency_no_match() -> None:
    """Тестирует фильтрацию, если валюта не найдена."""
    result = list(filter_by_currency(MOCK_TRANSACTIONS, "GBP"))
    expected: list = []
    assert result == expected


def test_transaction_descriptions_with_missing_key() -> None:
    """Тестирует извлечение описаний, если ключ отсутствует."""
    transactions_with_missing = MOCK_TRANSACTIONS + [{"id": 3}]
    result = list(transaction_descriptions(transactions_with_missing))
    expected = ["Payment", "Transfer", ""]
    assert result == expected


def test_card_number_generator_large_range() -> None:
    """Тестирует генерацию номеров карт в большом диапазоне."""
    result = list(card_number_generator(9999999999999997, 9999999999999999))
    expected = [
        "9999 9999 9999 9997",
        "9999 9999 9999 9998",
        "9999 9999 9999 9999",
    ]
    assert result == expected


def test_card_number_generator_single_number() -> None:
    """Тестирует генерацию одного номера карты."""
    result = list(card_number_generator(1234567890123456, 1234567890123456))
    expected = ["1234 5678 9012 3456"]
    assert result == expected


# Тесты для load_transactions_from_json


def test_load_transactions_from_json_success(tmp_path: Path) -> None:
    """Тест успешной загрузки корректного JSON."""
    data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    file_path = tmp_path / "test.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    result = load_transactions_from_json(str(file_path))
    assert result == data


def test_load_transactions_from_json_file_not_found(tmp_path: Path) -> None:
    """Тест, если файл не существует."""
    file_path = tmp_path / "nonexistent.json"
    result = load_transactions_from_json(str(file_path))
    assert result == []


def test_load_transactions_from_json_invalid_json(tmp_path: Path) -> None:
    """Тест, если в файле не JSON."""
    file_path = tmp_path / "invalid.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("not a json")
    result = load_transactions_from_json(str(file_path))
    assert result == []


def test_load_transactions_from_json_not_a_list(tmp_path: Path) -> None:
    """Тест, если JSON содержит не список (например, словарь)."""
    data = {"key": "value"}
    file_path = tmp_path / "dict.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    result = load_transactions_from_json(str(file_path))
    assert result == []
