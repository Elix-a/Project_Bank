import pytest
from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number_valid(sample_card_number):
    """Тестирует корректную маскировку номера карты."""
    masked = get_mask_card_number(sample_card_number)  # sample_card_number = "7000792289606361"
    assert masked == "7000 79** **** 6361"


def test_get_mask_card_number_invalid_length_short():
    """Тестирует обработку короткого номера карты (15 цифр)."""
    short_number = "123456789012345"  # 15 цифр
    # Проверяем, что функция возвращает строку (не вызывает исключение)
    # и форматирует её в соответствии с логикой (берёт срезы)
    result = get_mask_card_number(short_number)
    # Ожидаемый результат по логике: f"{short_number[:4]} {short_number[4:6]}** **** {short_number[-4:]}"
    # "1234 56** **** 2345"
    expected = "1234 56** **** 2345"
    assert result == expected
    # Также проверим, что результат - строка
    assert isinstance(result, str)


def test_get_mask_card_number_invalid_length_long():
    """Тестирует обработку слишком длинного номера карты (17 цифр)."""
    long_number = "12345678901234567"  # 17 цифр
    # Проверяем, что функция возвращает строку (не вызывает исключение)
    # и форматирует её в соответствии с логикой (берёт срезы)
    result = get_mask_card_number(long_number)
    # Ожидаемый результат по логике: f"{long_number[:4]} {long_number[4:6]}** **** {long_number[-4:]}"
    # "1234 56** **** 4567" (последние 4 цифры: 4567)
    expected = "1234 56** **** 4567"  # <-- Обновлено
    assert result == expected
    assert isinstance(result, str)


def test_get_mask_card_number_non_numeric():
    """Тестирует обработку некорректного ввода (не цифры)."""
    non_numeric = "abcdabcdabcdabcd"
    # Функция просто берет срезы, поэтому проверим результат
    result = get_mask_card_number(non_numeric)
    # Ожидаемый результат по логике: f"{non_numeric[:4]} {non_numeric[4:6]}** **** {non_numeric[-4:]}"
    # "abcd ab** **** abcd" (последние 4 символа: abcd)
    expected = "abcd ab** **** abcd"  # <-- Обновлено
    assert result == expected
    assert isinstance(result, str)


def test_get_mask_account_valid(sample_account_number):
    """Тестирует корректную маскировку номера счета."""
    masked = get_mask_account(sample_account_number)  # sample_account_number = "73654108430135874305"
    assert masked == "**4305"


def test_get_mask_account_invalid_length_short():
    """Тестирует обработку короткого номера счета (например, 19 цифр)."""
    short_number = "7365410843013587430"  # 19 цифр
    # Проверяем, что функция возвращает строку (не вызывает исключение)
    # и форматирует её в соответствии с логикой (берёт последние 4)
    result = get_mask_account(short_number)
    # Ожидаемый результат по логике: f"**{short_number[-4:]}"
    # "**7430"
    expected = "**7430"
    assert result == expected
    assert isinstance(result, str)


def test_get_mask_account_invalid_length_long():
    """Тестирует обработку слишком длинного номера счета (например, 21 цифра)."""
    long_number = "736541084301358743051"  # 21 цифра
    # Проверяем, что функция возвращает строку (не вызывает исключение)
    # и форматирует её в соответствии с логикой (берёт последние 4)
    result = get_mask_account(long_number)
    # Ожидаемый результат по логике: f"**{long_number[-4:]}"
    # "**3051" (последние 4 цифры: 3051)
    expected = "**3051"  # <-- Обновлено
    assert result == expected
    assert isinstance(result, str)


def test_get_mask_account_non_numeric():
    """Тестирует обработку некорректного ввода (не цифры) для счета."""
    non_numeric = "abcdefghijklmnopqrst"
    # Функция просто берет последние 4 символа, поэтому проверим результат
    result = get_mask_account(non_numeric)
    # Ожидаемый результат по логике: f"**{non_numeric[-4:]}"
    # "**qrst" (последние 4 символа: qrst)
    expected = "**qrst"  # <-- Обновлено
    assert result == expected
    assert isinstance(result, str)


# Параметризованные тесты для маскировки карты
@pytest.mark.parametrize(
    "card_input, expected_output",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
        ("4111111111111111", "4111 11** **** 1111"),  # Пример другого номера
    ],
)
def test_get_mask_card_number_parametrized(card_input, expected_output):
    """Параметризованный тест для различных номеров карт."""
    assert get_mask_card_number(card_input) == expected_output


# Параметризованные тесты для маскировки счета
@pytest.mark.parametrize(
    "account_input, expected_output",
    [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("11112222333344445555", "**5555"),
        ("00000000000000000001", "**0001"),  # Граничный случай
    ],
)
def test_get_mask_account_parametrized(account_input, expected_output):
    """Параметризованный тест для различных номеров счетов."""
    assert get_mask_account(account_input) == expected_output
