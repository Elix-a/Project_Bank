# tests/test_utils.py

from src.utils.utils import filter_by_state, get_transaction_by_id, sort_by_date


def test_get_transaction_by_id_found() -> None:
    """Тестирует поиск транзакции по ID."""
    transactions = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}]
    result = get_transaction_by_id(transactions, 1)
    expected: dict = {"id": 1, "state": "EXECUTED"}
    assert result == expected


def test_get_transaction_by_id_not_found() -> None:
    """Тестирует поведение, если транзакция не найдена."""
    transactions = [{"id": 1, "state": "EXECUTED"}]
    result = get_transaction_by_id(transactions, 999)
    expected: dict = {}
    assert result == expected


def test_filter_by_state_default() -> None:
    """Тестирует фильтрацию по умолчанию (EXECUTED)."""
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "EXECUTED"},
    ]
    result = filter_by_state(transactions)
    expected = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"},
    ]
    assert result == expected


def test_filter_by_state_cancelled() -> None:
    """Тестирует фильтрацию по состоянию CANCELLED."""
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "CANCELLED"},
    ]
    result = filter_by_state(transactions, state="CANCELLED")
    expected = [{"id": 3, "state": "CANCELLED"}]
    assert result == expected


def test_sort_by_date_descending() -> None:
    """Тестирует сортировку по дате (по убыванию)."""
    transactions = [
        {"id": 1, "date": "2023-01-02T00:00:00.000000"},
        {"id": 2, "date": "2023-01-01T00:00:00.000000"},
        {"id": 3, "date": "2023-01-03T00:00:00.000000"},
    ]
    result = sort_by_date(transactions)
    expected = [
        {"id": 3, "date": "2023-01-03T00:00:00.000000"},
        {"id": 1, "date": "2023-01-02T00:00:00.000000"},
        {"id": 2, "date": "2023-01-01T00:00:00.000000"},
    ]
    assert result == expected


def test_sort_by_date_ascending() -> None:
    """Тестирует сортировку по дате по возрастанию."""
    transactions = [
        {"id": 1, "date": "2023-01-02T00:00:00.000000"},
        {"id": 2, "date": "2023-01-01T00:00:00.000000"},
        {"id": 3, "date": "2023-01-03T00:00:00.000000"},
    ]
    result = sort_by_date(transactions, reverse=False)
    expected = [
        {"id": 2, "date": "2023-01-01T00:00:00.000000"},
        {"id": 1, "date": "2023-01-02T00:00:00.000000"},
        {"id": 3, "date": "2023-01-03T00:00:00.000000"},
    ]
    assert result == expected
