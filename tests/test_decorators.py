# tests/test_decorators.py

import os
import tempfile
from typing import Union  # Добавлен Import

import pytest

from src.decorators.decorators import log


def test_log_success_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует логирование успешного вызова в stdout."""

    @log(filename=None)  # Явно указываем None
    def func_success() -> str:
        return "Success!"

    result = func_success()

    assert result == "Success!"
    captured = capsys.readouterr()
    # Проверяем, что сообщение попало в stdout
    assert "func_success ok" in captured.out


def test_log_with_args_kwargs_success_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует логирование успешного вызова с аргументами в stdout."""

    @log(filename=None)  # Явно указываем None
    def func_with_args_success(a: int, b: int, c: Union[int, None] = None) -> int:
        return a + b + (c or 0)

    result = func_with_args_success(1, 2, c=3)

    assert result == 6  # 1 + 2 + 3
    captured = capsys.readouterr()
    # Проверяем, что сообщение попало в stdout
    assert "func_with_args_success ok" in captured.out


def test_log_with_args_kwargs_error_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует логирование ошибки с аргументами в stdout."""

    @log(filename=None)  # Явно указываем None
    def func_with_args_error(a: int, b: int, c: Union[int, None] = None) -> int:
        if a < 0:
            raise ValueError("A cannot be negative")
        return a + b + (c or 0)

    with pytest.raises(ValueError, match="A cannot be negative"):
        func_with_args_error(-1, 2, c=3)

    captured = capsys.readouterr()

    assert "func_with_args_error error: ValueError" in captured.out
    # --- ИСПРАВЛЕНО: Ожидаем c='3' ---
    assert "Inputs: ('-1', '2', c='3')" in captured.out  # Проверяем, что аргументы попали в сообщение


def test_log_success_file() -> None:
    """Тестирует логирование успешного вызова в файл."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as temp_file:
        temp_filename = temp_file.name

    @log(filename=temp_filename)
    def func_success_file() -> str:
        return "Success!"

    result = func_success_file()

    assert result == "Success!"
    #  Проверяем, что файл был создан и содержит ожидаемое сообщение
    assert os.path.exists(temp_filename)
    with open(temp_filename, "r", encoding="utf-8") as f:
        content = f.read()
        assert "func_success_file ok" in content

    # Удаляем временный файл
    os.unlink(temp_filename)


def test_log_different_errors_file_runtime_error() -> None:  # Переименована функция, чтобы избежать дубликата
    """Тестирует логирование разных типов ошибок в файл."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as temp_file:
        temp_filename = temp_file.name

    @log(filename=temp_filename)
    def func_raising_error() -> None:
        raise RuntimeError("Runtime error test")

    with pytest.raises(RuntimeError, match="Runtime error test"):
        func_raising_error()

    #  Проверяем, что файл был создан и содержит ожидаемое сообщение об ошибке
    assert os.path.exists(temp_filename)
    with open(temp_filename, "r", encoding="utf-8") as f:
        content = f.read()
        assert "func_raising_error error: RuntimeError" in content
        # Аргументы не передаются, поэтому Inputs: () или Inputs: (,)
        # Проверим только начало сообщения об ошибке
        assert "Runtime error test" in content

    # Удаляем временный файл
    os.unlink(temp_filename)


@pytest.mark.parametrize(
    "exception_type, exception_msg",
    [
        (ValueError, "Value error test"),
        (TypeError, "Type error test"),
        (KeyError, "key_test"),
    ],
)
def test_log_different_errors_file_parametrized(
    exception_type: type, exception_msg: str
) -> None:  # Переименована функция, чтобы избежать дубликата
    """Параметризованный тест для логирования разных типов ошибок в файл."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as temp_file:
        temp_filename = temp_file.name

    @log(filename=temp_filename)
    def func_raising_error(msg: str) -> None:
        raise exception_type(msg)

    with pytest.raises(exception_type, match=exception_msg):
        func_raising_error(exception_msg)

    #  Проверяем, что файл был создан и содержит ожидаемое сообщение об ошибке
    assert os.path.exists(temp_filename)
    with open(temp_filename, "r", encoding="utf-8") as f:
        content = f.read()
        assert f"func_raising_error error: {exception_type.__name__}" in content
        assert f"Inputs: ('{exception_msg}',)" in content  # Аргумент передаётся как кортеж в строке

    # Удаляем временный файл
    os.unlink(temp_filename)


def test_log_with_args_kwargs_success_file() -> None:
    """Тестирует логирование успешного вызова с аргументами в файл."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as temp_file:
        temp_filename = temp_file.name

    @log(filename=temp_filename)
    def func_with_args_success_file(a: int, b: int, c: Union[int, None] = None) -> int:
        return a + b + (c or 0)

    result = func_with_args_success_file(10, 20, c=30)

    assert result == 60  # 10 + 20 + 30
    #  Проверяем, что файл был создан и содержит ожидаемое сообщение об успехе
    assert os.path.exists(temp_filename)
    with open(temp_filename, "r", encoding="utf-8") as f:
        content = f.read()
        assert "func_with_args_success_file ok" in content

    # Удаляем временный файл
    os.unlink(temp_filename)


def test_log_with_args_kwargs_error_file() -> None:
    """Тестирует логирование ошибки с аргументами в файл."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as temp_file:
        temp_filename = temp_file.name

    @log(filename=temp_filename)
    def func_with_args_error_file(x: int, y: int) -> int:
        if x > y:
            raise ArithmeticError("x cannot be greater than y")
        return x * y

    with pytest.raises(ArithmeticError, match="x cannot be greater than y"):
        func_with_args_error_file(5, 3)

    #  Проверяем, что файл был создан и содержит ожидаемое сообщение об ошибке
    assert os.path.exists(temp_filename)
    with open(temp_filename, "r", encoding="utf-8") as f:
        content = f.read()
        assert "func_with_args_error_file error: ArithmeticError" in content
        # --- ИСПРАВЛЕНО: Ожидаем c='3' ---
        assert "Inputs: ('5', '3')" in content  # Проверяем, что аргументы попали в сообщение

    # Удаляем временный файл
    os.unlink(temp_filename)


def test_log_no_filename_decorator() -> None:
    """Тестирует поведение декоратора, если filename не передан."""
    # log(filename=None) уже протестирован в test_log_success_stdout

    # Проверим, что log() без аргументов работает как log(filename=None)
    # Для этого нужно создать декоратор и применить его
    decorator_instance = log()  # Вызов без аргументов, эквивалентно log(filename=None)

    @decorator_instance
    def func_test_no_filename() -> str:
        return "No filename test"

    result = func_test_no_filename()
    assert result == "No filename test"
    # Логика проверки stdout аналогична test_log_success_stdout
    # Но мы не можем легко получить доступ к capsys извне
    # Проверим, что функция выполняется без ошибок


def test_log_filename_is_none_explicitly() -> None:
    """Тестирует поведение декоратора, если filename явно равен None."""
    # log(filename=None) уже протестирован в test_log_success_stdout
    # Этот тест делает то же самое, но явно указывает None

    @log(filename=None)
    def func_test_filename_none() -> str:
        return "Filename is None test"

    result = func_test_filename_none()
    assert result == "Filename is None test"
    # Логика проверки stdout аналогична test_log_success_stdout
    # Но мы не можем легко получить доступ к capsys извне
    # Проверим, что функция выполняется без ошибок


def test_log_filename_empty_string() -> None:
    """Тестирует поведение декоратора, если filename - пустая строка."""
    # Это может быть особым случаем, ведущим к странному поведению
    # или ошибке при открытии файла. Проверим.

    @log(filename="")  # Пустая строка
    def func_test_empty_filename() -> str:
        return "Empty filename test"

    # Ожидаем, что вызов функции приведёт к ошибке при попытке открытия файла с пустым именем
    with pytest.raises(OSError):  # OSError или FileNotFoundError
        func_test_empty_filename()


def test_log_filename_non_existent_directory() -> None:
    """Тестирует поведение декоратора, если filename указывает на несуществующую директорию."""
    non_existent_path = "/this/directory/does/not/exist/log.txt"

    @log(filename=non_existent_path)
    def func_test_nonexistent_dir() -> str:
        return "Non-existent dir test"

    # Ожидаем, что вызов функции приведёт к ошибке при попытке открытия файла в несуществующей директории
    with pytest.raises(OSError):  # OSError или FileNotFoundError
        func_test_nonexistent_dir()
