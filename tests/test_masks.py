from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_valid() -> None:
    """Тестирует маскировку корректного номера карты."""
    number = 1234567890123456
    expected = "1234 56** **** 3456"
    assert get_mask_card_number(number) == expected


def test_get_mask_card_number_invalid_length_short() -> None:
    """Тестирует обработку короткого номера карты (15 цифр)."""
    short_number = 123456789012345  # 15 цифр
    # Функция теперь возвращает "" при неправильной длине
    result = get_mask_card_number(short_number)
    expected = ""
    assert result == expected


def test_get_mask_card_number_invalid_length_long() -> None:
    """Тестирует обработку слишком длинного номера карты (17 цифр)."""
    long_number = 12345678901234567  # 17 цифр
    # Функция теперь возвращает "" при неправильной длине
    result = get_mask_card_number(long_number)
    expected = ""
    assert result == expected


def test_get_mask_account_valid() -> None:
    """Тестирует маскировку корректного номера счёта."""
    number = 73654108430135874305
    expected = "**4305"
    assert get_mask_account(number) == expected


def test_get_mask_account_invalid_length_short() -> None:
    """Тестирует обработку короткого номера счёта (например, 19 цифр)."""
    short_number = 7365410843013587430  # 19 цифр
    # Функция теперь возвращает "" при неправильной длине
    result = get_mask_account(short_number)
    expected = ""
    assert result == expected


def test_get_mask_account_invalid_length_long() -> None:
    """Тестирует обработку слишком длинного номера счёта (например, 21 цифра)."""
    long_number = 736541084301358743051  # 21 цифра
    # Функция теперь возвращает "" при неправильной длине
    result = get_mask_account(long_number)
    expected = ""
    assert result == expected
