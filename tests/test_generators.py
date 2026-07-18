# tests/test_generators.py

import pytest

from src.generators.generators import (  # Импортируем из правильного места
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


def test_card_number_generator_basic() -> None:
    """Тестирует базовую генерацию номеров карт."""
    gen = card_number_generator(1, 2)
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"
    with pytest.raises(StopIteration):
        next(gen)


def test_filter_by_currency_basic() -> None:
    """Тестирует базовую фильтрацию по валюте."""
    transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
    ]
    gen = filter_by_currency(transactions, "USD")
    assert next(gen) == {"id": 1, "operationAmount": {"currency": {"code": "USD"}}}
    with pytest.raises(StopIteration):
        next(gen)


def test_transaction_descriptions_basic() -> None:
    """Тестирует базовое извлечение описаний."""
    transactions = [
        {"id": 1, "description": "Payment"},
        {"id": 2, "description": "Transfer"},
    ]
    gen = transaction_descriptions(transactions)
    assert next(gen) == "Payment"
    assert next(gen) == "Transfer"
    with pytest.raises(StopIteration):
        next(gen)


def test_card_number_generator_edge_case() -> None:
    """Тестирует генерацию с граничным значением."""
    gen = card_number_generator(9999999999999999, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9999"
    with pytest.raises(StopIteration):
        next(gen)


def test_filter_by_currency_no_matches() -> None:
    """Тестирует фильтрацию, когда совпадений нет."""
    transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
    ]
    gen = filter_by_currency(transactions, "EUR")
    with pytest.raises(StopIteration):
        next(gen)


def test_transaction_descriptions_empty_description() -> None:
    """Тестирует извлечение описания, если оно пустое."""
    transactions = [
        {"id": 1, "description": ""},
    ]
    gen = transaction_descriptions(transactions)
    assert next(gen) == ""
    with pytest.raises(StopIteration):
        next(gen)


def test_card_number_generator_range_zero() -> None:
    """Тестирует генерацию в диапазоне, начинающемся с нуля."""
    gen = card_number_generator(0, 0)
    assert next(gen) == "0000 0000 0000 0000"
    with pytest.raises(StopIteration):
        next(gen)


def test_filter_by_currency_multiple_matches() -> None:
    """Тестирует фильтрацию с несколькими совпадениями."""
    transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 4, "operationAmount": {"currency": {"code": "USD"}}},
    ]
    gen = filter_by_currency(transactions, "USD")
    assert next(gen) == {"id": 1, "operationAmount": {"currency": {"code": "USD"}}}
    assert next(gen) == {"id": 3, "operationAmount": {"currency": {"code": "USD"}}}
    assert next(gen) == {"id": 4, "operationAmount": {"currency": {"code": "USD"}}}
    with pytest.raises(StopIteration):
        next(gen)


def test_transaction_descriptions_mixed() -> None:
    """Тестирует извлечение описаний с различными значениями."""
    transactions = [
        {"id": 1, "description": "Payment"},
        {"id": 2, "description": ""},  # Пустое описание
        {"id": 3, "description": "Refund"},
        {"id": 4, "description": "Transfer"},
    ]
    gen = transaction_descriptions(transactions)
    assert next(gen) == "Payment"
    assert next(gen) == ""  # Пустое описание
    assert next(gen) == "Refund"
    assert next(gen) == "Transfer"
    with pytest.raises(StopIteration):
        next(gen)


def test_card_number_generator_large_numbers() -> None:
    """Тестирует генерацию с большими номерами."""
    gen = card_number_generator(1000000000000000, 1000000000000002)
    assert next(gen) == "1000 0000 0000 0000"
    assert next(gen) == "1000 0000 0000 0001"
    assert next(gen) == "1000 0000 0000 0002"
    with pytest.raises(StopIteration):
        next(gen)
