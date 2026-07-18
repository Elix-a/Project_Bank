# tests/conftest.py

import pytest


@pytest.fixture
def sample_card_string() -> str:
    """Возвращает строку с номером карты для тестов."""
    return "Visa Platinum 7000792289606361"


@pytest.fixture
def sample_account_string() -> str:
    """Возвращает строку с номером счёта для тестов."""
    return "Счет 73654108430135874305"


@pytest.fixture
def sample_transaction_rub() -> dict:
    """Возвращает пример транзакции в RUB."""
    return {"amount": 100.0, "currency": "RUB"}


@pytest.fixture
def sample_transaction_usd() -> dict:
    """Возвращает пример транзакции в USD."""
    return {"amount": 1.0, "currency": "USD"}


@pytest.fixture
def sample_transaction_eur() -> dict:
    """Возвращает пример транзакции в EUR."""
    return {"amount": 1.0, "currency": "EUR"}


@pytest.fixture
def sample_transaction_gbp() -> dict:
    """Возвращает пример транзакции в GBP."""
    return {"amount": 1.0, "currency": "GBP"}


@pytest.fixture
def sample_transaction_with_amount_and_currency() -> dict:
    """Возвращает пример транзакции с amount и currency."""
    return {"id": 1, "amount": 100.0, "currency": "USD", "description": "Test Transaction"}


@pytest.fixture
def sample_transactions_list() -> list[dict]:
    """Возвращает список примеров транзакций."""
    return [
        {"id": 1, "amount": 100.0, "currency": "USD", "description": "Transaction 1"},
        {"id": 2, "amount": 200.0, "currency": "EUR", "description": "Transaction 2"},
        {"id": 3, "amount": 300.0, "currency": "RUB", "description": "Transaction 3"},
    ]


@pytest.fixture
def sample_iso_date_string() -> str:
    """Возвращает строку даты в формате ISO 8601."""
    return "2023-03-11T02:26:18.671407"


@pytest.fixture
def sample_iso_date_string_with_z() -> str:
    """Возвращает строку даты в формате ISO 8601 с суффиксом Z."""
    return "2023-03-11T02:26:18.671407Z"


@pytest.fixture
def sample_invalid_iso_date_string() -> str:
    """Возвращает неверную строку даты."""
    return "это_не_дата"


@pytest.fixture
def sample_card_number_string() -> str:
    """Возвращает строку с номером карты."""
    return "7000792289606361"


@pytest.fixture
def sample_account_number_string() -> str:
    """Возвращает строку с номером счёта."""
    return "73654108430135874305"


@pytest.fixture
def sample_card_type_visa() -> str:
    """Возвращает тип карты Visa."""
    return "Visa"


@pytest.fixture
def sample_card_type_mastercard() -> str:
    """Возвращает тип карты Mastercard."""
    return "Mastercard"


@pytest.fixture
def sample_card_type_maestro() -> str:
    """Возвращает тип карты Maestro."""
    return "Maestro"


@pytest.fixture
def sample_card_type_discover() -> str:
    """Возвращает тип карты Discover."""
    return "Discover"


@pytest.fixture
def sample_account_prefix() -> str:
    """Возвращает префикс для счёта."""
    return "Счет "


@pytest.fixture
def sample_card_prefixes() -> list[str]:
    """Возвращает список префиксов для карт."""
    return ["Visa ", "Mastercard ", "Maestro ", "Discover "]


@pytest.fixture
def sample_transaction_executed() -> dict:
    """Возвращает пример транзакции со статусом EXECUTED."""
    return {"id": 1, "state": "EXECUTED", "amount": 100.0, "currency": "USD", "description": "Executed Transaction"}


@pytest.fixture
def sample_transaction_pending() -> dict:
    """Возвращает пример транзакции со статусом PENDING."""
    return {"id": 2, "state": "PENDING", "amount": 200.0, "currency": "EUR", "description": "Pending Transaction"}


@pytest.fixture
def sample_transaction_cancelled() -> dict:
    """Возвращает пример транзакции со статусом CANCELLED."""
    return {"id": 3, "state": "CANCELLED", "amount": 300.0, "currency": "RUB", "description": "Cancelled Transaction"}


@pytest.fixture
def sample_transaction_with_date() -> dict:
    """Возвращает пример транзакции с датой."""
    return {
        "id": 4,
        "date": "2023-01-01T00:00:00.000000",
        "amount": 400.0,
        "currency": "GBP",
        "description": "Transaction with Date",
    }


@pytest.fixture
def sample_transaction_without_date() -> dict:
    """Возвращает пример транзакции без даты."""
    return {"id": 5, "amount": 500.0, "currency": "JPY", "description": "Transaction without Date"}
