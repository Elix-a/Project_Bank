# src/services.py

import logging
from typing import Any, Dict, List

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму, которую можно отложить в «Инвесткопилку» за указанный месяц.

    Args:
        month: Месяц в формате 'YYYY-MM'.
        transactions: Список транзакций с полями 'Дата операции' и 'Сумма операции'.
        limit: Предел округления (10, 50 или 100).

    Returns:
        Сумма, отложенная в «Инвесткопилку» (float).
    """
    total_saved = 0.0

    for tr in transactions:
        # Проверяем, что транзакция принадлежит нужному месяцу
        date_str = tr.get("Дата операции", "")
        if isinstance(date_str, str):
            # ожидается формат 'YYYY-MM-DD ...', берем первые 7 символов
            tr_month = date_str[:7]
        else:
            continue

        if tr_month != month:
            continue

        # Сумма операции (всегда положительная для округления)
        amount = tr.get("Сумма операции", 0)
        if amount <= 0:
            continue

        # Округление вверх до ближайшего кратного limit
        rounded = ((amount + limit - 1) // limit) * limit
        saved = rounded - amount
        total_saved += saved

    logger.info(f"Месяц {month}: отложено {total_saved:.2f} ₽ при лимите {limit} ₽")
    return round(total_saved, 2)
