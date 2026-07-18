# tests/test_utils.py

from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.utils.utils import (
    filter_by_state,
    filter_transactions_by_date,
    get_transaction_by_id,
    greeting_by_time,
    load_transactions_from_xlsx,
    sort_by_date,
)


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


def test_greeting_morning() -> None:
    """Приветствие утром."""
    assert greeting_by_time(datetime(2023, 1, 1, 6, 0, 0)) == "Доброе утро"
    assert greeting_by_time(datetime(2023, 1, 1, 11, 59, 59)) == "Доброе утро"


def test_greeting_day() -> None:
    """Приветствие днём."""
    assert greeting_by_time(datetime(2023, 1, 1, 12, 0, 0)) == "Добрый день"
    assert greeting_by_time(datetime(2023, 1, 1, 17, 59, 59)) == "Добрый день"


def test_greeting_evening() -> None:
    """Приветствие вечером."""
    assert greeting_by_time(datetime(2023, 1, 1, 18, 0, 0)) == "Добрый вечер"
    assert greeting_by_time(datetime(2023, 1, 1, 22, 59, 59)) == "Добрый вечер"


def test_greeting_night() -> None:
    """Приветствие ночью."""
    assert greeting_by_time(datetime(2023, 1, 1, 23, 0, 0)) == "Доброй ночи"
    assert greeting_by_time(datetime(2023, 1, 1, 5, 59, 59)) == "Доброй ночи"


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """DataFrame для тестов фильтрации по дате."""
    return pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2023-03-05", "2023-03-25", "2023-02-28", "2023-03-01", "2023-04-01"]),
            "amount": [100, 200, 300, 400, 500],
        }
    )


def test_filter_in_march(sample_df: pd.DataFrame) -> None:
    """Фильтрация – остаются операции с 1 по 25 марта."""
    filtered = filter_transactions_by_date(sample_df, "2023-03-25 12:00:00")
    assert len(filtered) == 3
    assert all(filtered["Дата операции"] <= pd.Timestamp("2023-03-25 23:59:59.999999"))


def test_filter_start_of_month(sample_df: pd.DataFrame) -> None:
    """Фильтрация – только 1 марта."""
    filtered = filter_transactions_by_date(sample_df, "2023-03-01")
    assert len(filtered) == 1


def test_filter_no_results(sample_df: pd.DataFrame) -> None:
    """Фильтрация – нет операций за январь."""
    filtered = filter_transactions_by_date(sample_df, "2023-01-15")
    assert len(filtered) == 0


@patch("os.path.exists", return_value=True)
@patch("pandas.read_excel")
def test_load_transactions_success(mock_read_excel: MagicMock, mock_exists: MagicMock) -> None:
    """Успешная загрузка Excel-файла."""
    mock_df = pd.DataFrame({"Дата операции": ["01.01.2023"], "Сумма": [100]})
    mock_read_excel.return_value = mock_df
    df = load_transactions_from_xlsx("dummy.xlsx")
    assert not df.empty
    assert "Дата операции" in df.columns


def test_load_transactions_file_not_found() -> None:
    """Ошибка при отсутствии файла."""
    with pytest.raises(FileNotFoundError, match="не найден"):
        load_transactions_from_xlsx("nonexistent_file.xlsx")
