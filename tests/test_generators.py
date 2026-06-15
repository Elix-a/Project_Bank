import pytest
from src.generators.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Пример данных из задания
transactions_data = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160"
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229"
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {
            "amount": "67314.70",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657"
    }
]


# --- Тесты для filter_by_currency ---
def test_filter_by_currency_usd():
    """Тестирует фильтрацию по валюте USD."""
    usd_transactions = list(filter_by_currency(transactions_data, "USD"))
    # Проверяем, что вернулись только транзакции в USD
    assert len(usd_transactions) == 3
    for trans in usd_transactions:
        assert trans["operationAmount"]["currency"]["code"] == "USD"

def test_filter_by_currency_rub():
    """Тестирует фильтрацию по валюте RUB."""
    rub_transactions = list(filter_by_currency(transactions_data, "RUB"))
    # Проверяем, что вернулись только транзакции в RUB
    assert len(rub_transactions) == 2
    for trans in rub_transactions:
        assert trans["operationAmount"]["currency"]["code"] == "RUB"

def test_filter_by_currency_empty():
    """Тестирует фильтрацию по несуществующей валюте."""
    empty_transactions = list(filter_by_currency(transactions_data, "EUR"))
    # Проверяем, что вернулся пустой список
    assert len(empty_transactions) == 0

def test_filter_by_currency_empty_list():
    """Тестирует фильтрацию с пустым списком."""
    empty_transactions = list(filter_by_currency([], "USD"))
    # Проверяем, что вернулся пустой список
    assert len(empty_transactions) == 0

# Параметризованные тесты для filter_by_currency
@pytest.mark.parametrize("currency, expected_count", [
    ("USD", 3),
    ("RUB", 2),
    ("EUR", 0),
])
def test_filter_by_currency_parametrized(currency, expected_count):
    """Параметризованный тест для различных валют."""
    filtered = list(filter_by_currency(transactions_data, currency))
    assert len(filtered) == expected_count


# --- Тесты для transaction_descriptions ---
def test_transaction_descriptions_all():
    """Тестирует генерацию всех описаний."""
    descriptions = list(transaction_descriptions(transactions_data))
    expected_descriptions = [t["description"] for t in transactions_data]
    assert descriptions == expected_descriptions

def test_transaction_descriptions_empty():
    """Тестирует генерацию описаний с пустым списком."""
    descriptions = list(transaction_descriptions([]))
    assert descriptions == []

def test_transaction_descriptions_single():
    """Тестирует генерацию описания для одной транзакции."""
    single_transaction = [transactions_data[0]]
    descriptions = list(transaction_descriptions(single_transaction))
    assert descriptions == [transactions_data[0]["description"]]


# --- Тесты для card_number_generator ---
def test_card_number_generator_range():
    """Тестирует генерацию в заданном диапазоне."""
    start = 1
    end = 5
    generated_numbers = list(card_number_generator(start, end))
    expected_numbers = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]
    assert generated_numbers == expected_numbers

def test_card_number_generator_single():
    """Тестирует генерацию одного номера."""
    start = 1234567890123456
    end = 1234567890123456
    generated_numbers = list(card_number_generator(start, end))
    expected_numbers = ["1234 5678 9012 3456"]
    assert generated_numbers == expected_numbers

def test_card_number_generator_formatting():
    """Тестирует форматирование конкретного номера."""
    # Тестируем номер 1000000000000001 -> 1000 0000 0000 0001 (ПРАВИЛЬНО)
    start = 1000000000000001
    end = 1000000000000001
    generated_numbers = list(card_number_generator(start, end))
    expected_numbers = ["1000 0000 0000 0001"] # <-- ИСПРАВЛЕНО
    assert generated_numbers == expected_numbers

# Параметризованные тесты для card_number_generator
@pytest.mark.parametrize("input_num, expected_formatted", [
    (1, "0000 0000 0000 0001"),
    (1234, "0000 0000 0000 1234"),
    (1234567890123456, "1234 5678 9012 3456"),
])
def test_card_number_generator_parametrized(input_num, expected_formatted):
    """Параметризованный тест для форматирования номеров."""
    generated_numbers = list(card_number_generator(input_num, input_num))
    assert generated_numbers == [expected_formatted]
