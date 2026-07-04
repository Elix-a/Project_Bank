from src.masks import get_mask_card_number, get_mask_account  # Исправлен импорт из текущего пакета


def mask_account_card(input_string):
    """Функция для маскировки номера карты или счета."""
    # Разделяем строку на части (название и номер)
    parts = input_string.split()
    if not parts:
        return ""  # Если строка пуста, возвращаем пустую строку

    # Извлекаем номер (предполагается, что он последний)
    number = parts[-1]

    # Определяем, является ли это номером карты (16 цифр) или счета (20 цифр)
    if len(number) == 16 and number.isdigit():
        # Это карта
        masked_number = get_mask_card_number(int(number))
        # Возвращаем строку с заменённым номером
        return " ".join(parts[:-1]) + " " + masked_number
    elif len(number) == 20 and number.isdigit():
        # Это счёт
        masked_number = get_mask_account(int(number))
        # Возвращаем строку с заменённым номером
        return " ".join(parts[:-1]) + " " + masked_number
    else:
        # Если номер не подходит ни под одно условие, возвращаем как есть
        return input_string


def get_date(date_string):
    """Функция для преобразования строки даты в формат DD.MM.YYYY."""
    # Импортируем datetime внутри функции
    from datetime import datetime

    # Преобразуем строку в объект datetime, указав формат
    date_object = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    # Форматируем объект datetime в строку нужного формата
    return date_object.strftime("%d.%m.%Y")
