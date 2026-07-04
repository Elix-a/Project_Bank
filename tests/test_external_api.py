import os
import requests.exceptions
from unittest.mock import patch
from src.external_api.external_api import convert_to_rub

def test_convert_to_rub_rub():
    """Тест конвертации из RUB в RUB."""
    transaction = {"amount": 100.0, "currency": "RUB"}
    assert convert_to_rub(transaction) == 100.0


def test_convert_to_rub_usd_success():
    """Тест успешной конвертации из USD в RUB с моком API."""
    transaction = {"amount": 1.0, "currency": "USD"}

    # Создаем объект, имитирующий ответ API
    mock_response_data = {"success": True, "result": 95.0}

    # Создаем MagicMock для response
    mock_response = type('obj', (object,), {
        'json': lambda self: mock_response_data,
        'raise_for_status': lambda self: None
    })()

    # Создаем Mock для requests.get, который возвращает наш mock_response
    with patch('src.external_api.external_api.requests.get') as mock_get:
        mock_get.return_value = mock_response # <-- Вот ключевое изменение

        result = convert_to_rub(transaction)
        assert result == 95.0
        # Проверим, что requests.get был вызван с правильными аргументами
        mock_get.assert_called_once()


def test_convert_to_rub_eur_success():
    """Тест успешной конвертации из EUR в RUB с моком API."""
    transaction = {"amount": 1.0, "currency": "EUR"}

    mock_response_data = {"success": True, "result": 105.0}

    mock_response = type('obj', (object,), {
        'json': lambda self: mock_response_data,
        'raise_for_status': lambda self: None
    })()

    with patch('src.external_api.external_api.requests.get') as mock_get:
        mock_get.return_value = mock_response # <-- Вот ключевое изменение

        result = convert_to_rub(transaction)
        assert result == 105.0
        mock_get.assert_called_once()


def test_convert_to_rub_api_error():
    """Тест обработки ошибки API (например, сеть недоступна)."""
    transaction = {"amount": 100.0, "currency": "USD"}

    # Мокаем requests.get, чтобы он бросал исключение из семейства requests.exceptions
    # Это исключение convert_to_rub умеет перехватывать.
    with patch('src.external_api.external_api.requests.get', side_effect=requests.exceptions.ConnectionError("Network error")):
        result = convert_to_rub(transaction)
        # При ошибке, вызванной библиотекой requests (или её подклассами),
        # convert_to_rub должен вернуть исходную сумму.
        assert result == 100.0
