# tests/test_views.py

import json
from unittest.mock import MagicMock, patch

import pandas as pd

from src.views import (
    _fetch_currency_rate,
    _fetch_stock_price,
    _get_cards_info,
    _get_top_transactions,
    _load_user_settings,
    generate_main_view,
)

# ---------- Вспомогательные данные ----------

SAMPLE_DF = pd.DataFrame(
    {
        "Дата операции": pd.to_datetime(["2023-03-15", "2023-03-20", "2023-02-10", "2023-03-05"]),
        "Номер карты": ["1234", "1234", "5678", "1234"],
        "Сумма платежа": [-1500.0, -2500.0, -1000.0, -500.0],
        "Категория": ["Супермаркеты", "Транспорт", "Рестораны", "Супермаркеты"],
        "Описание": ["Пятёрочка", "Метро", "Кафе", "Магнит"],
        "Сумма операции": [-1500.0, -2500.0, -1000.0, -500.0],
        "Валюта операции": ["RUB", "RUB", "RUB", "RUB"],
    }
)


# ---------- Тесты хелперов ----------


class TestLoadUserSettings:
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    def test_load_valid_json(self, mock_open: MagicMock, mock_exists: MagicMock) -> None:
        mock_open.return_value.__enter__.return_value.read.return_value = (
            '{"user_currencies": ["USD"], "user_stocks": ["AAPL"]}'
        )
        result = _load_user_settings()
        assert result == {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}

    @patch("os.path.exists", return_value=False)
    def test_file_not_found(self, mock_exists: MagicMock) -> None:
        result = _load_user_settings()
        assert result == {"user_currencies": [], "user_stocks": []}

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", side_effect=IOError)
    def test_read_error(self, mock_open: MagicMock, mock_exists: MagicMock) -> None:
        result = _load_user_settings()
        assert result == {"user_currencies": [], "user_stocks": []}


class TestFetchCurrencyRate:
    @patch("src.views.requests.get")
    def test_successful_fetch(self, mock_get: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"RUB": 75.5}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        rate = _fetch_currency_rate("USD")
        assert rate == 75.5

    @patch("src.views.requests.get", side_effect=Exception("Network error"))
    def test_fetch_error(self, mock_get: MagicMock) -> None:
        rate = _fetch_currency_rate("USD")
        assert rate == 0.0


class TestFetchStockPrice:
    @patch("src.views.requests.get")
    def test_successful_fetch(self, mock_get: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {"Global Quote": {"05. price": "150.25"}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        price = _fetch_stock_price("AAPL")
        assert price == 150.25

    @patch("src.views.requests.get", side_effect=Exception("Network error"))
    def test_fetch_error(self, mock_get: MagicMock) -> None:
        price = _fetch_stock_price("AAPL")
        assert price == 0.0


class TestGetCardsInfo:
    def test_extracts_correctly(self) -> None:
        cards = _get_cards_info(SAMPLE_DF)
        assert len(cards) == 2  # две уникальные карты
        # карта 1234: 1500 + 2500 + 500 = 4500
        card1 = next(c for c in cards if c["last_digits"] == "1234")
        assert card1["total_spent"] == 4500.00
        assert card1["cashback"] == 45.00

    def test_no_cards_column(self) -> None:
        df = SAMPLE_DF.drop(columns=["Номер карты"])
        assert _get_cards_info(df) == []


class TestGetTopTransactions:
    def test_top_n(self) -> None:
        top = _get_top_transactions(SAMPLE_DF, top_n=2)
        assert len(top) == 2
        # первая по абсолютной сумме: 2500 (Метро)
        assert top[0]["amount"] == -2500.0
        assert top[0]["category"] == "Транспорт"
        assert top[0]["date"] == "20.03.2023"

    def test_empty_df(self) -> None:
        empty = pd.DataFrame()
        assert _get_top_transactions(empty) == []


# ---------- Тест главной функции ----------


class TestGenerateMainView:
    @patch("src.views._load_user_settings")
    @patch("src.views._fetch_currency_rate")
    @patch("src.views._fetch_stock_price")
    @patch("src.views.load_transactions_from_xlsx")
    @patch("os.path.exists", return_value=True)
    def test_full_json(
        self,
        mock_exists: MagicMock,
        mock_load_xlsx: MagicMock,
        mock_stock: MagicMock,
        mock_currency: MagicMock,
        mock_settings: MagicMock,
    ) -> None:
        # Настраиваем моки
        mock_load_xlsx.return_value = SAMPLE_DF.copy()
        mock_settings.return_value = {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "TSLA"],
        }
        mock_currency.return_value = 75.5
        mock_stock.return_value = 150.25

        date_str = "2023-03-25 12:00:00"
        result_json = generate_main_view(date_str)
        result = json.loads(result_json)

        # Проверяем структуру
        assert "greeting" in result
        assert result["greeting"] in [
            "Доброе утро",
            "Добрый день",
            "Добрый вечер",
            "Доброй ночи",
        ]
        assert "cards" in result
        assert isinstance(result["cards"], list)
        assert "top_transactions" in result
        assert len(result["top_transactions"]) <= 5
        assert "currency_rates" in result
        assert len(result["currency_rates"]) == 2
        assert "stock_prices" in result
        assert len(result["stock_prices"]) == 2

    def test_invalid_date_format(self) -> None:
        result = json.loads(generate_main_view("not-a-date"))
        assert "error" in result

    @patch("src.views.load_transactions_from_xlsx", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_load: MagicMock) -> None:
        result = json.loads(generate_main_view("2023-03-25 12:00:00"))
        assert "error" in result
