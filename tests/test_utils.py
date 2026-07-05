import os
import tempfile
import json
from src.utils.utils import load_transactions_from_json


def test_load_transactions_from_json_success():
    """Тест успешной загрузки списка транзакций."""
    # Создаем временный JSON-файл
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_file:
        temp_filename = temp_file.name
        json.dump([{"id": 1, "amount": 100, "currency": "RUB"}], temp_file)
        temp_file.flush()

    result = load_transactions_from_json(temp_filename)
    assert result == [{"id": 1, "amount": 100, "currency": "RUB"}]
    os.unlink(temp_filename)


def test_load_transactions_from_json_empty_file():
    """Тест загрузки пустого файла."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_file:
        temp_filename = temp_file.name
        temp_file.write("")
        temp_file.flush()

    result = load_transactions_from_json(temp_filename)
    assert result == []
    os.unlink(temp_filename)


def test_load_transactions_from_json_not_a_list():
    """Тест загрузки файла, содержащего не список."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_file:
        temp_filename = temp_file.name
        json.dump({"key": "value"}, temp_file)
        temp_file.flush()

    result = load_transactions_from_json(temp_filename)
    assert result == []
    os.unlink(temp_filename)


def test_load_transactions_from_json_file_not_found():
    """Тест загрузки несуществующего файла."""
    result = load_transactions_from_json("nonexistent.json")
    assert result == []
