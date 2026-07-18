# tests/test_reports.py

import os

import pandas as pd

from src.reports import report_to_file, spending_by_weekday

# ---------- Тесты декоратора ----------


@report_to_file()
def decorated_default() -> str:
    return "Default file name"


@report_to_file("custom_report.txt")
def decorated_custom() -> str:
    return "Custom file name"


def test_decorator_writes_to_file() -> None:
    """Декоратор записывает результат функции в файл."""
    for filename in os.listdir():
        if filename.startswith("report_") and filename.endswith(".txt"):
            os.remove(filename)

    result = decorated_default()
    assert result == "Default file name"

    report_files = [f for f in os.listdir() if f.startswith("report_") and f.endswith(".txt")]
    assert len(report_files) == 1
    with open(report_files[0], "r", encoding="utf-8") as file:
        content = file.read()
    assert content == "Default file name"
    os.remove(report_files[0])


def test_decorator_with_custom_filename() -> None:
    """Декоратор с явным именем файла."""
    result = decorated_custom()
    assert result == "Custom file name"

    assert os.path.exists("custom_report.txt")
    with open("custom_report.txt", "r", encoding="utf-8") as file:
        content = file.read()
    assert content == "Custom file name"
    os.remove("custom_report.txt")


def test_decorator_with_dataframe() -> None:
    """Декоратор корректно обрабатывает DataFrame."""

    @report_to_file("df_report.txt")
    def df_func() -> pd.DataFrame:
        return pd.DataFrame({"A": [1, 2], "B": [3, 4]})

    result = df_func()
    assert isinstance(result, pd.DataFrame)

    assert os.path.exists("df_report.txt")
    with open("df_report.txt", "r", encoding="utf-8") as file:
        content = file.read()
    assert content.replace(" ", "") == "A  B\n1  3\n2  4".replace(" ", "")
    os.remove("df_report.txt")


# ---------- Тесты spending_by_weekday ----------


def create_test_df() -> pd.DataFrame:
    """Создаёт тестовый DataFrame с транзакциями за несколько месяцев."""
    data = {
        "Дата операции": pd.to_datetime(
            [
                "2023-09-04",  # Понедельник
                "2023-09-04",  # Понедельник
                "2023-09-05",  # Вторник
                "2023-08-07",  # Понедельник (август)
                "2023-06-01",  # Четверг (вне диапазона, так как начало — 2023-06-15)
            ]
        ),
        "Сумма платежа": [-1000.0, -2000.0, -500.0, -1500.0, -300.0],
    }
    return pd.DataFrame(data)


def test_spending_by_weekday() -> None:
    """Корректный подсчёт средних трат по дням недели."""
    df = create_test_df()
    result = spending_by_weekday(df, date="2023-09-15")

    # Ожидаем 2 строки: Понедельник и Вторник
    assert len(result) == 2

    # Понедельник: (1000 + 2000 + 1500) / 3 = 1500.00
    monday = result[result["День недели"] == "Понедельник"]
    assert not monday.empty
    assert float(monday["Средние траты"].iloc[0]) == 1500.00

    # Вторник: 500 / 1 = 500.00
    tuesday = result[result["День недели"] == "Вторник"]
    assert not tuesday.empty
    assert float(tuesday["Средние траты"].iloc[0]) == 500.00


def test_spending_by_weekday_default_date() -> None:
    """Если дата не указана, используется текущая."""
    df = create_test_df()
    result = spending_by_weekday(df)
    assert isinstance(result, pd.DataFrame)
    assert set(result.columns) == {"День недели", "Средние траты"}


def test_spending_by_weekday_empty() -> None:
    """Пустой DataFrame возвращает пустой результат."""
    empty_df = pd.DataFrame(columns=["Дата операции", "Сумма платежа"])
    result = spending_by_weekday(empty_df, date="2023-09-15")
    assert len(result) == 0
    assert set(result.columns) == {"День недели", "Средние траты"}
