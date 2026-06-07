import pytest
from src.processing import filter_by_state, sort_by_date


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


def test_sort_by_date_descending(sample_transactions):
    """Тестирует сортировку по дате по убыванию (по умолчанию)."""
    sorted_transactions = sort_by_date(sample_transactions)
    dates = [t["date"] for t in sorted_transactions if t["date"] != "invalid_date_format"] # Исключаем некорректные даты из проверки
    parsed_dates = [t for t in sorted_transactions if t["date"] != "invalid_date_format"]
    # Проверяем, что даты отсортированы в порядке убывания
    for i in range(len(parsed_dates) - 1):
        assert parsed_dates[i]["date"] >= parsed_dates[i+1]["date"]


def test_sort_by_date_ascending(sample_transactions):
    """Тестирует сортировку по дате по возрастанию."""
    sorted_transactions = sort_by_date(sample_transactions, ascending=True)
    dates = [t["date"] for t in sorted_transactions if t["date"] != "invalid_date_format"]
    parsed_dates = [t for t in sorted_transactions if t["date"] != "invalid_date_format"]
    # Проверяем, что даты отсортированы в порядке возрастания
    for i in range(len(parsed_dates) - 1):
        assert parsed_dates[i]["date"] <= parsed_dates[i+1]["date"]


def test_sort_by_date_invalid_handling(sample_transactions):
    """Тестирует, как функция сортирует при наличии некорректных дат."""
    # Проверьте, как ваша функция обрабатывает некорректные даты.
    # Скорее всего, она возвращает datetime.min для таких случаев.
    sorted_transactions = sort_by_date(sample_transactions)
    # Найдём транзакцию с некорректной датой
    invalid_transaction = next((t for t in sorted_transactions if t["date"] == "invalid_date_format"), None)
    if invalid_transaction:
        # Если обработка некорректных дат включает datetime.min,
        # они должны быть в начале списка при сортировке по возрастанию.
        # Или в конце при сортировке по убыванию.
        # Адаптируйте проверку под вашу реализацию.
        # Например, если datetime.min -> начало при ascending=True:
        # assert sorted_transactions.index(invalid_transaction) == 0 # Если ascending=True
        # или
        # assert sorted_transactions.index(invalid_transaction) == len(sorted_transactions) - 1 # Если ascending=False
        pass # Замените pass на актуальный тест


# Параметризованные тесты для filter_by_state
@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 3),
    ("CANCELED", 2),
    ("PENDING", 1),
    ("UNKNOWN", 0),
])
def test_filter_by_state_parametrized(state, expected_count, sample_transactions):
    """Параметризованный тест для различных значений state."""
    filtered = filter_by_state(sample_transactions, state)
    assert len(filtered) == expected_count


# Параметризованные тесты для sort_by_date (с фикстурой данных)
# Мы можем создать фикстуру с разными наборами данных для сортировки
@pytest.fixture
def unsorted_transactions():
    """Возвращает список транзакций в неотсортированном порядке."""
    return [
        {"id": 1, "date": "2024-03-01T10:00:00"},
        {"id": 2, "date": "2024-01-01T10:00:00"},
        {"id": 3, "date": "2024-02-01T10:00:00"},
    ]

@pytest.mark.parametrize("ascending, expected_order", [
    (False, [{"id": 1}, {"id": 3}, {"id": 2}]), # Ожидаемый порядок по id при убывании
    (True, [{"id": 2}, {"id": 3}, {"id": 1}]),  # Ожидаемый порядок по id при возрастании
])
def test_sort_by_date_parametrized(unsorted_transactions, ascending, expected_order):
    """Параметризованный тест для сортировки по возрастанию/убыванию."""
    sorted_transactions = sort_by_date(unsorted_transactions, ascending=ascending)
    sorted_ids = [t["id"] for t in sorted_transactions]
    expected_ids = [t["id"] for t in expected_order]
    assert sorted_ids == expected_ids
