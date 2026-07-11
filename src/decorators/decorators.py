# src/decorators/decorators.py

import functools
from typing import Any, Callable


def log(func: Callable | None = None, *, filename: str | None = None) -> Any:
    """
    Декоратор, который логирует результат выполнения функции.
    При успешном завершении выводит "<имя_функции> ok".
    При ошибке выводит "<имя_функции> error: <тип_ошибки>. Inputs: <аргументы>."
    В сообщение об ошибке также включается её текст (str(e)).

    Если filename передан, лог записывается в файл в режиме добавления.
    Если filename равен None, лог выводится в stdout.
    Если filename = "" или указывает на несуществующую директорию – OSError.
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = f(*args, **kwargs)
                msg = f"{f.__name__} ok"
                _write_log(msg, filename)
                return result
            except Exception as e:
                # Формируем представление аргументов
                arg_reprs = [f"'{a}'" for a in args]  # все позиционные – в кавычках
                kwarg_reprs = [f"{k}='{v}'" for k, v in kwargs.items()]
                all_parts = arg_reprs + kwarg_reprs

                # Кортеж: для одного элемента добавляем запятую
                if len(all_parts) == 0:
                    inputs_str = "()"
                elif len(all_parts) == 1:
                    inputs_str = f"({all_parts[0]},)"
                else:
                    inputs_str = "(" + ", ".join(all_parts) + ")"

                error_type = type(e).__name__
                error_text = str(e)  # текст ошибки
                msg = (
                    f"{f.__name__} error: {error_type}. "
                    f"Inputs: {inputs_str}."
                    f" Message: {error_text}"  # добавляем сообщение ошибки
                )
                _write_log(msg, filename)
                raise

        return wrapper

    # Поддержка @log, @log() и @log(filename=...)
    if func is None:
        return decorator
    else:
        return decorator(func)


def _write_log(message: str, filename: str | None) -> None:
    """Запись сообщения в файл или stdout."""
    if filename is not None:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
