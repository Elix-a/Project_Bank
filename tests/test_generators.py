import pytest
from src.generators.generators import filter_by_currency, transaction_descriptions, card_number_generator


# --- Тесты для filter_by_currency (используют фикстуру sample_transactions) ---
def test_filter_by_currency_usd(sample_transactions):
    """Тестирует фильтрацию по валюте USD."""
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    # Проверяем, что вернулись только транзакции в USD
    assert len(usd_transactions) == 3
    for trans in usd_transactions:
        assert trans["operationAmount"]["currency"]["code"] == "USD"

def test_filter_by_currency_rub(sample_transactions):
    """Тестирует фильтрацию по валюте RUB."""
    rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
    # Проверяем, что вернулись только транзакции в RUB
    assert len(rub_transactions) == 2
    for trans in rub_transactions:
        assert trans["operationAmount"]["currency"]["code"] == "RUB"

def test_filter_by_currency_empty(sample_transactions):
    """Тестирует фильтрацию по несуществующей валюте."""
    empty_transactions = list(filter_by_currency(sample_transactions, "EUR"))
    # Проверяем, что вернулся пустой список
    assert len(empty_transactions) == 0

def test_filter_by_currency_empty_list():
    """Тестирует фильтрацию с пустым списком."""
    empty_transactions = list(filter_by_currency([], "USD"))
    # Проверяем, что вернулся пустой список
    assert len(empty_transactions) == 0

# Параметризованные тесты для filter_by_currency (можно оставить как есть или адаптировать)
@pytest.mark.parametrize("currency, expected_count", [
    ("USD", 3),
    ("RUB", 2),
    ("EUR", 0),
])
def test_filter_by_currency_parametrized(sample_transactions, currency, expected_count):
    """Параметризованный тест для различных валют."""
    filtered = list(filter_by_currency(sample_transactions, currency))
    assert len(filtered) == expected_count


# --- Тесты для transaction_descriptions (используют фикстуру sample_transactions) ---
def test_transaction_descriptions_all(sample_transactions):
    """Тестирует генерацию всех описаний."""
    descriptions = list(transaction_descriptions(sample_transactions))
    expected_descriptions = [t["description"] for t in sample_transactions]
    assert descriptions == expected_descriptions

def test_transaction_descriptions_empty():
    """Тестирует генерацию описаний с пустым списком."""
    descriptions = list(transaction_descriptions([]))
    assert descriptions == []

def test_transaction_descriptions_single(sample_transactions):
    """Тестирует генерацию описания для одной транзакции."""
    # Берём первую транзакцию из фикстуры
    single_transaction = [sample_transactions[0]]
    descriptions = list(transaction_descriptions(single_transaction))
    assert descriptions == [sample_transactions[0]["description"]]


# --- Тесты для card_number_generator (используют фикстуры card_range_small, single_card_number, specific_card_number) ---
def test_card_number_generator_range(card_range_small):
    """Тестирует генерацию в заданном диапазоне (фикстура)."""
    start, end = card_range_small
    generated_numbers = list(card_number_generator(start, end))
    expected_numbers = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]
    assert generated_numbers == expected_numbers

def test_card_number_generator_single(single_card_number):
    """Тестирует генерацию одного номера (фикстура)."""
    start, end = single_card_number
    generated_numbers = list(card_number_generator(start, end))
    expected_numbers = ["1234 5678 9012 3456"]
    assert generated_numbers == expected_numbers

def test_card_number_generator_formatting(specific_card_number):
    """Тестирует форматирование конкретного номера (фикстура, исправленный тест)."""
    # Тестируем номер 1000000000000001 -> 1000 0000 0000 0001
    start, end = specific_card_number
    generated_numbers = list(card_number_generator(start, end))
    expected_numbers = ["1000 0000 0000 0001"] # <-- Исправлено: реальный результат функции
    assert generated_numbers == expected_numbers

# Параметризованные тесты для card_number_generator (используют фикстуру card_params)
def test_card_number_generator_parametrized(card_params):
    """Параметризованный тест для форматирования номеров (через фикстуру)."""
    input_num, expected_formatted = card_params
    generated_numbers = list(card_number_generator(input_num, input_num))
    assert generated_numbers == [expected_formatted]
