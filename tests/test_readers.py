# tests/test_readers.py

import os
from unittest.mock import patch

import pandas as pd

from src.readers import read_transactions_from_csv, read_transactions_from_excel

# Пример данных для мока
MOCK_CSV_DATA = """id,state,date,amount,currency_name,currency_code,description,from,to
1,EXECUTED,2023-01-01T00:00:00.000000,100.0,RUB,RUB,Payment,,Account 12345
2,CANCELLED,2023-01-02T00:00:00.000000,200.0,USD,USD,Transfer,Card 6789,Account 67890
"""

MOCK_DF = pd.DataFrame(
    [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T00:00:00.000000",
            "amount": 100.0,
            "currency_name": "RUB",
            "currency_code": "RUB",
            "description": "Payment",
            "from": "",
            "to": "Account 12345",
        },
        {
            "id": 2,
            "state": "CANCELLED",
            "date": "2023-01-02T00:00:00.000000",
            "amount": 200.0,
            "currency_name": "USD",
            "currency_code": "USD",
            "description": "Transfer",
            "from": "Card 6789",
            "to": "Account 67890",
        },
    ]
)

MOCK_EXCEL_DATA = MOCK_DF  # Для простоты используем тот же DataFrame для Excel


def test_read_transactions_from_csv_success() -> None:  # <-- Добавлен возвращаемый тип
    """Тестирует успешное чтение CSV."""
    with patch("pandas.read_csv") as mock_read_csv:
        mock_read_csv.return_value = MOCK_DF.copy()

        result = read_transactions_from_csv("dummy_path.csv")

        assert result == MOCK_DF.to_dict(orient="records")
        mock_read_csv.assert_called_once_with("dummy_path.csv")


def test_read_transactions_from_csv_file_not_found() -> None:  # <-- Добавлен возвращаемый тип
    """Тестирует поведение при отсутствии файла CSV."""
    with patch("pandas.read_csv", side_effect=FileNotFoundError):
        result = read_transactions_from_csv("nonexistent.csv")

        assert result == []


def test_read_transactions_from_csv_empty_file() -> None:  # <-- Добавлен возвращаемый тип
    """Тестирует поведение при пустом CSV-файле."""
    with patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError("")):
        result = read_transactions_from_csv("empty.csv")

        assert result == []


def test_read_transactions_from_csv_other_error() -> None:  # <-- Добавлен возвращаемый тип
    """Тестирует поведение при других ошибках при чтении CSV."""
    with patch("pandas.read_csv", side_effect=RuntimeError("Some error")):
        result = read_transactions_from_csv("error.csv")

        assert result == []


def test_read_transactions_from_excel_success() -> None:  # <-- Добавлен возвращаемый тип
    """Тестирует успешное чтение Excel."""
    with patch("pandas.read_excel") as mock_read_excel:  # <-- Теперь мокаем напрямую pd.read_excel
        mock_read_excel.return_value = MOCK_EXCEL_DATA.copy()  # <-- Мок возвращает DataFrame

        result = read_transactions_from_excel("dummy_path.xlsx")

        assert result == MOCK_EXCEL_DATA.to_dict(orient="records")
        mock_read_excel.assert_called_once_with("dummy_path.xlsx")  # <-- Проверяем вызов


def test_read_transactions_from_excel_file_not_found() -> None:  # <-- Добавлен возвращаемый тип
    """Тестирует поведение при отсутствии файла Excel."""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = read_transactions_from_excel("nonexistent.xlsx")

        assert result == []


def test_read_transactions_from_excel_empty_file() -> None:  # <-- Добавлен возвращаемый тип
    """Тестирует поведение при пустом Excel-файле."""
    with patch("pandas.read_excel", side_effect=pd.errors.EmptyDataError("")):
        result = read_transactions_from_excel("empty.xlsx")

        assert result == []


def test_read_transactions_from_excel_other_error() -> None:  # <-- Добавлен возвращаемый тип
    """Тестирует поведение при других ошибках при чтении Excel."""
    with patch("pandas.read_excel", side_effect=RuntimeError("Some error")):
        result = read_transactions_from_excel("error.xlsx")

        assert result == []


# --- Интеграционные тесты ---
# Имя файла, которое мы положили в корень
CSV_FILENAME = "transactions.csv"
EXCEL_FILENAME = "transactions_excel.xlsx"


def test_integration_read_csv_real_file() -> None:
    """Интеграционный тест: читаем реальный CSV файл."""
    # Проверяем, что файл существует
    assert os.path.exists(CSV_FILENAME), f"Файл {CSV_FILENAME} не найден в корне проекта."

    # Вызываем функцию с реальным путём
    transactions = read_transactions_from_csv(CSV_FILENAME)

    # Проверяем, что функция вернула список
    assert isinstance(transactions, list)

    # Проверяем, что список не пустой (если файл не пуст)
    assert len(transactions) > 0, f"Файл {CSV_FILENAME} пустой или не содержит данных в ожидаемом формате."

    # Проверяем, что первый элемент списка - словарь
    assert isinstance(transactions[0], dict), f"Первая строка данных в {CSV_FILENAME} не представлена как словарь."

    # (Опционально) Проверяем, что ожидаемые ключи присутствуют в первой транзакции
    # Замените 'id', 'amount' на ключи, которые есть в вашем файле
    # expected_keys = {'id', 'state', 'date', 'amount', 'currency_name', 'currency_code', 'description', 'from', 'to'}
    # assert expected_keys.issubset(set(transactions[0].keys())), \
    #     f"Не все ожидаемые ключи найдены в первой транзакции файла {CSV_FILENAME}."


def test_integration_read_excel_real_file() -> None:
    """Интеграционный тест: читаем реальный Excel файл."""
    # Проверяем, что файл существует
    assert os.path.exists(EXCEL_FILENAME), f"Файл {EXCEL_FILENAME} не найден в корне проекта."

    # Вызываем функцию с реальным путём
    transactions = read_transactions_from_excel(EXCEL_FILENAME)

    # Проверяем, что функция вернула список
    assert isinstance(transactions, list)

    # Проверяем, что список не пустой (если файл не пуст)
    assert len(transactions) > 0, f"Файл {EXCEL_FILENAME} пустой или не содержит данных в ожидаемом формате."

    # Проверяем, что первый элемент списка - словарь
    assert isinstance(transactions[0], dict), f"Первая строка данных в {EXCEL_FILENAME} не представлена как словарь."

    # (Опционально) Проверяем, что ожидаемые ключи присутствуют в первой транзакции
    # expected_keys = {'id', 'state', 'date', 'amount', 'currency_name', 'currency_code', 'description', 'from', 'to'}
    # assert expected_keys.issubset(set(transactions[0].keys())), \
    #     f"Не все ожидаемые ключи найдены в первой транзакции файла {EXCEL_FILENAME}."
