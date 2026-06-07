import pytest

# Фикстура для тестовых данных транзакций (для модуля processing)
@pytest.fixture
def sample_transactions():
    """Возвращает список тестовых транзакций."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T12:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2024-02-01T13:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-01T14:00:00"},
        {"id": 4, "state": "PENDING", "date": "2024-04-01T15:00:00"}, # Добавим PENDING
        {"id": 5, "state": "EXECUTED", "date": "2023-12-31T11:00:00"}, # Добавим старую дату
        {"id": 6, "state": "CANCELED", "date": "invalid_date_format"} # Добавим некорректную дату
    ]

# Фикстура для тестовых номеров карт и счетов (для модулей masks и widget)
@pytest.fixture
def sample_card_number():
    """Возвращает тестовый номер карты."""
    return "7000792289606361"

@pytest.fixture
def sample_account_number():
    """Возвращает тестовый номер счета."""
    return "73654108430135874305"

@pytest.fixture
def sample_iso_date():
    """Возвращает тестовую строку даты в формате ISO."""
    return "2024-03-11T02:26:18.671407"

# Фикстура для строки с типом и номером (для mask_account_card)
@pytest.fixture
def sample_card_string():
    """Возвращает строку с типом карты и номером."""
    return "Visa Platinum 7000792289606361"

@pytest.fixture
def sample_account_string():
    """Возвращает строку с типом счета и номером."""
    return "Счет 73654108430135874305"

@pytest.fixture
def sample_mixed_string():
    """Возвращает строку с типом карты и счета (для проверки ошибок)."""
    return "Visa Platinum 7000792289606361 и Счет 73654108430135874305"
