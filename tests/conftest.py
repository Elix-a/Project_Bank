import pytest


# =============================================================================
# ФИКСТУРЫ ДЛЯ СТАРЫХ ТЕСТОВ (masks, widget, processing)
# =============================================================================

@pytest.fixture
def sample_transactions():
    """Возвращает список тестовых транзакций для модулей processing и generators."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"}
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
                "currency": {"name": "USD", "code": "USD"}
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
                "currency": {"name": "руб.", "code": "RUB"}
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
                "currency": {"name": "USD", "code": "USD"}
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
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


@pytest.fixture
def card_number():
    """Тестовый номер карты для модуля masks/widget."""
    return "7000792289606361"


@pytest.fixture
def account_number():
    """Тестовый номер счета для модуля masks/widget."""
    return "73654108430135874305"


@pytest.fixture
def iso_date_string():
    """Тестовая строка даты в формате ISO."""
    return "2024-03-11T02:26:18.671407"


# =============================================================================
# ФИКСТУРЫ ДЛЯ НОВЫХ ТЕСТОВ (generators)
# =============================================================================

@pytest.fixture
def card_range_small():
    """Диапазон для генерации небольшого количества номеров карт."""
    return 1, 5


@pytest.fixture
def single_card_number():
    """Одиночный номер карты для теста."""
    return 1234567890123456, 1234567890123456


@pytest.fixture
def specific_card_number():
    """Конкретный номер для проверки форматирования."""
    return 1000000000000001, 1000000000000001


@pytest.fixture(params=[
    (1, "0000 0000 0000 0001"),
    (1234, "0000 0000 0000 1234"),
    (1234567890123456, "1234 5678 9012 3456"),
])
def card_params(request):
    """Параметризованная фикстура для генератора карт."""
    return request.param

# Алиасы для совместимости со старыми тестами из homework_17
@pytest.fixture
def sample_card_number(card_number):
    return card_number

@pytest.fixture
def sample_account_number(account_number):
    return account_number

@pytest.fixture
def sample_iso_date(iso_date_string):
    return iso_date_string

@pytest.fixture
def sample_card_string(card_number):
    return f"Visa Platinum {card_number}"

@pytest.fixture
def sample_account_string(account_number):
    return f"Счет {account_number}"
