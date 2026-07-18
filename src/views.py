# src/views.py

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests

from src.utils.utils import filter_transactions_by_date, greeting_by_time, load_transactions_from_xlsx

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def _load_user_settings() -> Dict[str, Any]:
    """
    Загружает пользовательские настройки из user_settings.json.
    Возвращает словарь с ключами 'user_currencies' и 'user_stocks'.
    В случае ошибки возвращает словарь с пустыми списками.
    """
    settings_path = os.path.join(os.path.dirname(__file__), "..", "user_settings.json")
    if not os.path.exists(settings_path):
        logger.warning("Файл user_settings.json не найден. Используются пустые списки.")
        return {"user_currencies": [], "user_stocks": []}
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        logger.warning("Файл user_settings.json имеет некорректный формат. Используются пустые списки.")
        return {"user_currencies": [], "user_stocks": []}
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Ошибка чтения user_settings.json: {e}")
        return {"user_currencies": [], "user_stocks": []}


def _fetch_currency_rate(currency: str) -> float:
    """
    Получает курс рубля за 1 единицу указанной валюты через API.
    Возвращает курс (float) или 0.0 при ошибке.
    """
    try:
        url = f"https://api.exchangerate.host/latest?base={currency}&symbols=RUB"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        rate = data["rates"].get("RUB", 0.0)
        if rate:
            logger.info(f"Курс {currency}/RUB: {rate}")
        return float(rate)
    except Exception as e:
        logger.error(f"Не удалось получить курс для {currency}: {e}")
        return 0.0


def _fetch_stock_price(symbol: str) -> float:
    """
    Получает цену акции через Alpha Vantage (демо-ключ).
    Возвращает цену (float) или 0.0 при ошибке.
    """
    try:
        # Демо-ключ Alpha Vantage, для реальной работы замените на свой
        api_key = "demo"
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        price = data.get("Global Quote", {}).get("05. price", 0.0)
        price = float(price)
        if price:
            logger.info(f"Цена акции {symbol}: {price}")
        return price
    except Exception as e:
        logger.error(f"Не удалось получить цену для {symbol}: {e}")
        return 0.0


def _get_cards_info(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Группирует транзакции по последним 4 цифрам карты и считает общую сумму расходов и кешбэк.
    Если столбец 'Номер карты' отсутствует, возвращает пустой список.
    """
    if "Номер карты" not in df.columns:
        return []

    # Убираем строки без номера карты
    cards_df = df.dropna(subset=["Номер карты"]).copy()
    if cards_df.empty:
        return []

    # Оставляем только расходные операции (сумма платежа отрицательная)
    expenses = cards_df[cards_df["Сумма платежа"] < 0].copy()
    expenses.loc[:, "abs_amount"] = expenses["Сумма платежа"].abs()

    # Группируем по номеру карты (последние 4 цифры – строка)
    grouped = expenses.groupby("Номер карты")["abs_amount"].sum().reset_index()
    grouped.columns = ["last_digits", "total_spent"]

    result = []
    for _, row in grouped.iterrows():
        total = round(row["total_spent"], 2)
        cashback = round(total * 0.01, 2)  # 1%
        result.append(
            {
                "last_digits": str(row["last_digits"]),
                "total_spent": total,
                "cashback": cashback,
            }
        )
    return result


def _get_top_transactions(df: pd.DataFrame, top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Возвращает топ-N транзакций по абсолютной сумме платежа.
    """
    if df.empty:
        return []

    temp_df = df.copy()
    temp_df["abs_payment"] = temp_df["Сумма платежа"].abs()
    top = temp_df.nlargest(top_n, "abs_payment")

    result = []
    for _, row in top.iterrows():
        # Форматируем дату как dd.mm.yyyy
        date_obj = row.get("Дата операции")
        if pd.notna(date_obj):
            formatted_date = date_obj.strftime("%d.%m.%Y")
        else:
            formatted_date = ""

        result.append(
            {
                "date": formatted_date,
                "amount": row.get("Сумма платежа", 0.0),
                "category": row.get("Категория", ""),
                "description": row.get("Описание", ""),
            }
        )
    return result


def generate_main_view(date_str: str) -> str:
    """
    Генерирует JSON-ответ для главной страницы.

    Args:
        date_str: строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        JSON-строка с данными для главной страницы.
    """
    try:
        target_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.error(f"Некорректный формат даты: {date_str}")
        return json.dumps({"error": "Invalid date format"}, ensure_ascii=False)

    # Загрузка данных из Excel
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    file_path = os.path.join(data_dir, "operations.xlsx")
    try:
        df = load_transactions_from_xlsx(file_path)
    except FileNotFoundError as e:
        logger.error(e)
        return json.dumps({"error": "Transaction file not found"}, ensure_ascii=False)

    # Фильтрация до указанной даты (с начала месяца)
    df_filtered = filter_transactions_by_date(df, date_str)

    # Приветствие
    greeting = greeting_by_time(target_dt)

    # Информация по картам
    cards_info = _get_cards_info(df_filtered)

    # Топ-5 транзакций
    top_transactions = _get_top_transactions(df_filtered, top_n=5)

    # Пользовательские настройки (валюты и акции)
    settings = _load_user_settings()
    currencies = settings.get("user_currencies", [])
    stocks = settings.get("user_stocks", [])

    # Курсы валют
    currency_rates = []
    for cur in currencies:
        rate = _fetch_currency_rate(cur)
        if rate > 0:
            currency_rates.append({"currency": cur, "rate": rate})

    # Цены акций
    stock_prices = []
    for stock in stocks:
        price = _fetch_stock_price(stock)
        if price > 0:
            stock_prices.append({"stock": stock, "price": price})

    # Собираем ответ
    response_data = {
        "greeting": greeting,
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(response_data, ensure_ascii=False, indent=2)
