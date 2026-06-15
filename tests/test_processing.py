import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def unsorted_transactions():
    """Возвращает список транзакций в неотсортированном порядке для тестов сортировки."""
    return [
        {"id": 1, "date": "2024-03-01T10:00:00"},
        {"id": 2, "date": "2024-01-01T10:00:00"},
        {"id": 3, "date": "2024-02-01T10:00:00"},
    ]


def test_filter_by_state_default_executed(sample_transactions):
    """Тестирует фильтрацию по умолчанию ('EXECUTED')."""
    filtered = filter_by_state(sample_transactions)
    executed_count = sum(1 for t in sample_transactions if t["state"] == "EXECUTED")
    assert len(filtered) == executed_count
    for transaction in filtered:
        assert transaction["state"] == "EXECUTED"


def test_filter_by_state_canceled(sample_transactions):
    """Тестирует фильтрацию по статусу 'CANCELED'."""
    filtered = filter_by_state(sample_transactions, "CANCELED")
    canceled_count = sum(1 for t in sample_transactions if t["state"] == "CANCELED")
    assert len(filtered) == canceled_count
    for transaction in filtered:
        assert transaction["state"] == "CANCELED"


def test_filter_by_state_empty_result(sample_transactions):
    """Тестирует фильтрацию, когда нет совпадений."""
    filtered = filter_by_state(sample_transactions, "UNKNOWN_STATE")
    assert len(filtered) == 0


@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 4),
    ("CANCELED", 1),
    ("PENDING", 0),
    ("UNKNOWN", 0),
])
def test_filter_by_state_parametrized(state, expected_count, sample_transactions):
    """Параметризованный тест для различных значений state."""
    filtered = filter_by_state(sample_transactions, state)
    assert len(filtered) == expected_count


def test_sort_by_date_descending(sample_transactions):
    """Тестирует сортировку по дате по убыванию (по умолчанию)."""
    sorted_transactions = sort_by_date(sample_transactions)
    valid_dates = [t for t in sorted_transactions if isinstance(t.get("date"), str) and "invalid" not in t["date"]]
    for i in range(len(valid_dates) - 1):
        assert valid_dates[i]["date"] >= valid_dates[i + 1]["date"]


def test_sort_by_date_ascending(sample_transactions):
    """Тестирует сортировку по дате по возрастанию."""
    sorted_transactions = sort_by_date(sample_transactions, ascending=True)
    valid_dates = [t for t in sorted_transactions if isinstance(t.get("date"), str) and "invalid" not in t["date"]]
    for i in range(len(valid_dates) - 1):
        assert valid_dates[i]["date"] <= valid_dates[i + 1]["date"]


@pytest.mark.parametrize("ascending, expected_order", [
    (False, [{"id": 1}, {"id": 3}, {"id": 2}]),
    (True, [{"id": 2}, {"id": 3}, {"id": 1}]),
])
def test_sort_by_date_parametrized(unsorted_transactions, ascending, expected_order):
    """Параметризованный тест для сортировки по возрастанию/убыванию."""
    sorted_transactions = sort_by_date(unsorted_transactions, ascending=ascending)
    sorted_ids = [t["id"] for t in sorted_transactions]
    expected_ids = [t["id"] for t in expected_order]
    assert sorted_ids == expected_ids
