# src/reports.py

import functools
from datetime import datetime
from typing import Any, Callable, Optional

import pandas as pd

# Маппинг английских названий дней недели на русские
_WEEKDAY_MAP = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье",
}


def report_to_file(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для записи результата функции-отчёта в файл.

    Если filename не указан, генерирует имя вида report_YYYYMMDD_HHMMSS.txt.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            fname = filename
            if fname is None:
                fname = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            if isinstance(result, pd.DataFrame):
                content = result.to_string(index=False)
            else:
                content = str(result)
            with open(fname, "w", encoding="utf-8") as f:
                f.write(content)
            return result

        return wrapper

    return decorator


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Рассчитывает средние траты по дням недели за последние три месяца от указанной даты.

    Args:
        transactions: DataFrame с транзакциями. Ожидается наличие столбцов:
            - 'Дата операции' (datetime)
            - 'Сумма платежа' (float, отрицательные значения — расходы)
        date: опциональная дата в формате 'YYYY-MM-DD'. Если не указана, используется текущая дата.

    Returns:
        DataFrame со столбцами 'День недели' и 'Средние траты'.
    """
    if date is None:
        end_date = pd.Timestamp.now()
    else:
        end_date = pd.to_datetime(date)

    start_date = end_date - pd.DateOffset(months=3)

    # Приводим дату операции к datetime
    transactions = transactions.copy()
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")

    # Фильтруем транзакции за последние три месяца
    mask = (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
    df_filtered = transactions.loc[mask].copy()

    # Оставляем только расходы
    expenses = df_filtered[df_filtered["Сумма платежа"] < 0].copy()
    if expenses.empty:
        return pd.DataFrame(columns=["День недели", "Средние траты"])

    expenses["abs_amount"] = expenses["Сумма платежа"].abs()

    # Получаем название дня недели на английском, заменяем на русский
    expenses["День недели"] = expenses["Дата операции"].dt.day_name().map(_WEEKDAY_MAP)

    grouped = expenses.groupby("День недели")["abs_amount"].mean().reset_index()
    grouped.columns = ["День недели", "Средние траты"]
    grouped["Средние траты"] = grouped["Средние траты"].round(2)

    return grouped
