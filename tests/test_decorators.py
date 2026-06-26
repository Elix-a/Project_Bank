import pytest
import tempfile
import os
from unittest.mock import patch, mock_open
from src.decorators.decorators import log

# --- Тесты для декоратора log ---

def test_log_success_stdout(capsys):
    """Тестирует логирование успешного вызова в stdout."""
    @log(filename=None) # Явно указываем None
    def successful_func():
        return "success"

    result = successful_func()
    captured = capsys.readouterr()

    assert result == "success"
    assert "successful_func ok" in captured.out


def test_log_success_file():
    """Тестирует логирование успешного вызова в файл."""
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8') as temp_file:
        temp_filename = temp_file.name

    @log(filename=temp_filename)
    def successful_func():
        return "success"

    result = successful_func()

    # Проверяем, что файл был создан и содержит ожидаемое сообщение
    assert os.path.exists(temp_filename)
    with open(temp_filename, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "successful_func ok" in content

    # Удаляем временный файл
    os.unlink(temp_filename)

    assert result == "success"


def test_log_error_stdout(capsys):
    """Тестирует логирование ошибки в stdout."""
    @log(filename=None) # Явно указываем None
    def failing_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError, match="Test error"):
        failing_func()

    captured = capsys.readouterr()

    assert "failing_func error: ValueError" in captured.out
    assert "Inputs:" in captured.out


def test_log_error_file():
    """Тестирует логирование ошибки в файл."""
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8') as temp_file:
        temp_filename = temp_file.name

    @log(filename=temp_filename)
    def failing_func():
        raise TypeError("Type Error Test")

    with pytest.raises(TypeError, match="Type Error Test"):
        failing_func()

    # Проверяем, что файл был создан и содержит ожидаемое сообщение об ошибке
    assert os.path.exists(temp_filename)
    with open(temp_filename, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "failing_func error: TypeError" in content
        assert "Inputs:" in content

    # Удаляем временный файл
    os.unlink(temp_filename)


def test_log_with_args_kwargs_stdout(capsys):
    """Тестирует логирование вызова с аргументами в stdout."""
    @log(filename=None) # Явно указываем None
    def func_with_args(a, b, c=None):
        return a + b + (c or 0)

    result = func_with_args(1, 2, c=3)
    captured = capsys.readouterr()

    assert result == 6
    assert "func_with_args ok" in captured.out
    # Проверим, что аргументы были переданы (хотя бы косвенно через вызов)
    # Точная проверка формата аргументов в сообщении об успехе может быть сложнее,
    # но логика внутри декоратора их формирует. Основной фокус на логике и выводе.


def test_log_with_args_kwargs_error_stdout(capsys):
    """Тестирует логирование ошибки с аргументами в stdout."""
    @log(filename=None) # Явно указываем None
    def func_with_args_error(a, b, c=None):
        if a < 0:
            raise ValueError("A cannot be negative")
        return a + b + (c or 0)

    with pytest.raises(ValueError, match="A cannot be negative"):
        func_with_args_error(-1, 2, c=3)

    captured = capsys.readouterr()

    assert "func_with_args_error error: ValueError" in captured.out
    assert "Inputs: (-1, 2, c=3)" in captured.out # Проверяем, что аргументы попали в сообщение


# Параметризованный тест для проверки логирования разных типов ошибок в файл
@pytest.mark.parametrize("exception_type, exception_msg", [
    (ValueError, "Value error test"),
    (TypeError, "Type error test"),
    (KeyError, "key_test"),
])
def test_log_different_errors_file(exception_type, exception_msg):
    """Параметризованный тест для логирования разных типов ошибок в файл."""
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8') as temp_file:
        temp_filename = temp_file.name

    @log(filename=temp_filename)
    def func_raising_error(msg):
        raise exception_type(msg)

    with pytest.raises(exception_type, match=exception_msg):
        func_raising_error(exception_msg)

    # Проверяем, что файл был создан и содержит ожидаемое сообщение об ошибке
    assert os.path.exists(temp_filename)
    with open(temp_filename, 'r', encoding='utf-8') as f:
        content = f.read()
        assert f"func_raising_error error: {exception_type.__name__}" in content
        assert f"Inputs: ('{exception_msg}',)" in content # Аргумент передаётся как кортеж в строке

    # Удаляем временный файл
    os.unlink(temp_filename)

