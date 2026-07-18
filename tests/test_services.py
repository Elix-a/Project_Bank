# tests/test_services.py

from src.services import investment_bank


def test_investment_bank_basic() -> None:
    """Простой расчёт за месяц."""
    transactions = [
        {"Дата операции": "2023-03-05", "Сумма операции": 1712},
        {"Дата операции": "2023-03-12", "Сумма операции": 230},
        {"Дата операции": "2023-03-20", "Сумма операции": 987},
    ]
    # Округление до 50:
    # 1712 -> 1750 (38), 230 -> 250 (20), 987 -> 1000 (13) = 71
    result = investment_bank("2023-03", transactions, 50)
    assert result == 71.0


def test_investment_bank_limit_10() -> None:
    """Округление до 10."""
    transactions = [
        {"Дата операции": "2023-04-01", "Сумма операции": 123},
        {"Дата операции": "2023-04-02", "Сумма операции": 77},
    ]
    # 123 -> 130 (7), 77 -> 80 (3) = 10
    result = investment_bank("2023-04", transactions, 10)
    assert result == 10.0


def test_investment_bank_different_months() -> None:
    """Учитываются только операции нужного месяца."""
    transactions = [
        {"Дата операции": "2023-05-10", "Сумма операции": 200},
        {"Дата операции": "2023-06-10", "Сумма операции": 200},
    ]
    result = investment_bank("2023-05", transactions, 100)
    # 200 -> 200 (0)
    assert result == 0.0


def test_investment_bank_empty() -> None:
    """Пустой список транзакций."""
    result = investment_bank("2023-07", [], 50)
    assert result == 0.0


def test_investment_bank_negative_amount() -> None:
    """Отрицательные суммы игнорируются."""
    transactions = [
        {"Дата операции": "2023-08-01", "Сумма операции": -500},
        {"Дата операции": "2023-08-02", "Сумма операции": 50},
    ]
    # -500 игнорируется, 50 округляется до 100 → отложено 50
    result = investment_bank("2023-08", transactions, 100)
    assert result == 50.0
