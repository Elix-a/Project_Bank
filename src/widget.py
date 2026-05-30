from datetime import datetime


def get_mask_card_number(card_number: str) -> str:
    """Возвращает маску номера карты в формате XXXX XX** **** XXXX."""
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Возвращает маску номера счёта в формате **XXXX."""
    return f"**{account_number[-4:]}"


def mask_account_card(input_string: str) -> str:
    """
    Обрабатывает строку с информацией о карте или счете.
    Возвращает замаскированный номер.
    """
    parts = input_string.split()
    if len(parts) != 2:
        raise ValueError("Некорректный ввод: строка должна содержать ровно два элемента — тип и номер.")

    type_, number = parts

    if "Счет" in type_:
        return f"{type_} {get_mask_account(number)}"
    else:
        return f"{type_} {get_mask_card_number(number)}"


def get_date(iso_date: str) -> str:
    """
    Преобразует строку с датой в формате ISO 8601
    в строку формата ДД.ММ.ГГГГ.
    """
    try:
        date_obj = datetime.fromisoformat(iso_date.replace("T", " "))
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Некорректный формат даты.")
