# src/widget.py


def mask_account_card(card_or_account: str) -> str:
    """
    Маскирует номер карты или счёта.

    Args:
        card_or_account (str): Номер карты или счёта в виде строки.

    Returns:
        str: Маскированный номер.
    """
    parts = card_or_account.split()
    if not parts:
        return ""

    # Найдём индекс, с которого начинаются цифры
    # Проходим с конца, собираем числа, пока они есть
    numbers_from_end = []
    i = len(parts) - 1
    while i >= 0:
        part = parts[i]
        # Проверяем, состоит ли часть *только* из цифр
        if part.isdigit():
            numbers_from_end.append(part)
        else:
            # Если часть содержит буквы, останавливаемся
            break
        i -= 1

    # numbers_from_end содержит части в обратном порядке (с конца строки)
    numbers_str = "".join(reversed(numbers_from_end))

    # Текстовое описание — это всё, что до чисел
    text_description = " ".join(parts[: i + 1])

    # Извлекаем только цифры из объединённой строки чисел
    numbers_only = "".join(filter(str.isdigit, numbers_str))

    if len(numbers_only) == 16:  # Карта
        masked = f"{numbers_only[:4]} {numbers_only[4:6]}** **** {numbers_only[-4:]}"
        return f"{text_description} {masked}"
    elif len(numbers_only) == 20:  # Счёт
        masked = f"**{numbers_only[-4:]}"
        return f"{text_description} {masked}"
    else:
        # Если длина не подходит, возвращаем как есть (или можно бросить исключение)
        return card_or_account


def get_date(iso_date_string: str) -> str:
    """
    Преобразует строку даты в формате ISO 8601 в формат DD.MM.YYYY.

    Args:
        iso_date_string (str): Строка даты в формате ISO 8601 (например, YYYY-MM-DDTHH:MM:SS.ffffff).

    Returns:
        str: Дата в формате DD.MM.YYYY. Возвращает пустую строку при ошибке.
    """
    # Импортируем datetime внутри функции
    from datetime import datetime

    try:
        # Преобразуем строку в объект datetime, указав формат
        # 'fromisoformat' может не работать с Z в старых версиях, заменим Z на +00:00.
        date_object = datetime.fromisoformat(iso_date_string.replace("Z", "+00:00"))
        # Форматируем дату в нужный формат
        return date_object.strftime("%d.%m.%Y")
    except ValueError:
        # Если строка не соответствует формату, возвращаем пустую строку
        return ""
