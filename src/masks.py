import logging
import os

# --- Настройка логирования для модуля masks ---
# Создаём папку logs, если её нет
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаём обработчик для файла
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаём форматтер
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем обработчик к логеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: int) -> str:
    """
    Маскирует номер банковской карты по формату XXXX XX** **** XXXX.

    Args:
        card_number: Номер карты в виде целого числа.

    Returns:
        str: Маскированный номер карты.
    """
    card_number_str = str(card_number)
    if len(card_number_str) != 16:
        logger.error(f"Неверная длина номера карты: {len(card_number_str)}. Ожидается 16.")
        # Возвращаем пустую строку при ошибке
        return ""

    # Маскировка: первые 6 и последние 4 цифры видны, остальные заменяются на *
    masked = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
    logger.info(f"Номер карты {card_number} успешно замаскирован как {masked}")
    return masked


def get_mask_account(account_number: int) -> str:
    """
    Маскирует номер банковского счёта по формату **XXXX.

    Args:
        account_number: Номер счёта в виде целого числа.

    Returns:
        str: Маскированный номер счёта.
    """
    account_number_str = str(account_number)
    if len(account_number_str) != 20:
        logger.error(f"Неверная длина номера счёта: {len(account_number_str)}. Ожидается 20.")
        # Возвращаем пустую строку при ошибке
        return ""

    # Маскировка: последние 4 цифры видны, остальные заменяются на **
    masked = f"**{account_number_str[-4:]}"
    logger.info(f"Номер счёта {account_number} успешно замаскирован как {masked}")
    return masked
