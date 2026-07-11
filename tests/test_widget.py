# tests/test_widget.py

import pytest

from src.widget import get_date, mask_account_card


def test_mask_account_card_card_found(sample_card_string: str) -> None:
    """Тестирует маскировку номера карты, когда номер найден в строке."""
    result = mask_account_card(sample_card_string)  # sample_card_string = "Visa Platinum 7000792289606361"
    expected = "Visa Platinum 7000 79** **** 6361"
    assert result == expected


def test_mask_account_card_account_found(sample_account_string: str) -> None:
    """Тестирует маскировку номера счёта, когда номер найден в строке."""
    result = mask_account_card(sample_account_string)  # sample_account_string = "Счет 73654108430135874305"
    expected = "Счет **4305"
    assert result == expected


def test_mask_account_card_invalid_input() -> None:
    """Тестирует поведение при неверном вводе."""
    result = mask_account_card("Invalid Input")
    # Если длина не подходит, возвращаем как есть
    expected = "Invalid Input"
    assert result == expected


def test_mask_account_card_empty_input() -> None:
    """Тестирует поведение при пустом вводе."""
    result = mask_account_card("")
    expected = ""
    assert result == expected


def test_get_date_valid() -> None:
    """Тестирует преобразование корректной строки даты."""
    iso_date = "2023-03-11T02:26:18.671407"
    result = get_date(iso_date)
    expected = "11.03.2023"
    assert result == expected


def test_get_date_with_z_suffix() -> None:
    """Тестирует преобразование строки даты с Z-суффиксом."""
    iso_date = "2023-03-11T02:26:18.671407Z"
    result = get_date(iso_date)
    expected = "11.03.2023"
    assert result == expected


def test_get_date_invalid() -> None:
    """Тестирует поведение при некорректной строке даты."""
    invalid_date = "это_не_дата"
    # Проверяем, что функция возвращает пустую строку при ошибке
    result = get_date(invalid_date)
    expected = ""
    assert result == expected


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 5555555555554444", "MasterCard 5555 55** **** 4444"),
        ("Discover 6011111111111117", "Discover 6011 11** **** 1117"),
    ],
)
def test_mask_account_card_parametrized(input_string: str, expected_output: str) -> None:
    """Параметризованный тест для различных строк с картами и счетами."""
    assert mask_account_card(input_string) == expected_output
