import re # Импортируем модуль для работы с регулярными выражениями

from datetime import datetime
# Импортируем функции маскировки из masks.py
# Убедитесь, что файл src/masks.py существует и содержит эти функции
from src.masks import get_mask_card_number, get_mask_account


def get_mask_card_number(card_number: str) -> str:
    """Возвращает маску номера карты в формате XXXX XX** **** XXXX."""
    # Проверяем длину номера карты
    if len(card_number) != 16:
        # Можно вернуть ошибку или частичную маску, в зависимости от требований
        # Пока оставим как есть, но можно улучшить
        # print(f"Warning: Card number length is not 16: {len(card_number)}. Masking anyway.")
        pass # Или raise ValueError("Номер карты должен содержать 16 цифр")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Возвращает маску номера счёта в формате **XXXX."""
    # Проверяем длину номера счёта
    if len(account_number) != 20:
        # print(f"Warning: Account number length is not 20: {len(account_number)}. Masking anyway.")
        pass # Или raise ValueError("Номер счёта должен содержать 20 цифр")
    return f"**{account_number[-4:]}"


def mask_account_card(input_string: str) -> str:
    """
    Обрабатывает строку с информацией о карте или счете.
    Возвращает строку с замаскированным номером.
    """
    # Регулярное выражение для поиска последовательности из 16 или 20 цифр
    # \b - граница слова (чтобы не захватить часть другого числа)
    # \d - цифра
    # {16}|{20} - 16 или 20 повторений
    # () - захватываем найденную последовательность
    match = re.search(r'\b(\d{16}|\d{20})\b', input_string)

    if not match:
        # Если номер не найден, возвращаем исходную строку
        # Или можно вызвать исключение, в зависимости от требований
        return input_string

    number = match.group(1) # Получаем найденный номер
    prefix_part = input_string[:match.start()].strip() # Получаем часть строки до номера
    suffix_part = input_string[match.end():].strip() # Получаем часть строки после номера (если есть)

    # Определяем, карта это или счёт, по длине номера
    if len(number) == 16:
        masked_number = get_mask_card_number(number)
    elif len(number) == 20:
        masked_number = get_mask_account(number)
    else:
        # Теоретически, этого не должно произойти из-за регулярного выражения
        # Но на всякий случай
        return input_string

    # Собираем итоговую строку
    # Убираем лишние пробелы в prefix_part и suffix_part
    result_parts = [part for part in [prefix_part, masked_number, suffix_part] if part]
    return " ".join(result_parts)

    # Альтернативный способ (если suffix_part не важен или всегда пуст):
    # return f"{prefix_part} {masked_number}".strip()


def get_date(iso_date: str) -> str:
    """
    Преобразует строку с датой в формате ISO 8601
    в строку формата ДД.ММ.ГГГГ.
    """
    try:
        date_obj = datetime.fromisoformat(iso_date.replace("T", " "))
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        # raise ValueError("Некорректный формат даты.") # Опционально вызвать исключение
        # Или возвратить пустую строку или None, в зависимости от требований
        return "" # Возвращаем пустую строку при ошибке
