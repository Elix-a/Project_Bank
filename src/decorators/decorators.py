# src/decorators/decorators.py

import functools


def log(filename=None):
    """
    Декоратор для логирования вызовов функций.

    Args:
        filename (str, optional): Имя файла для логирования. Если None, логируется в stdout.

    Returns:
        callable: Декоратор, оборачивающий функцию.
    """
    def decorator(func):
        # Сохраняем метаданные оригинальной функции
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Формируем строку с аргументами
            # Для кортежа с одним элементом repr даст (x,) - с запятой
            # Мы хотим получить строку, как если бы это был кортеж
            args_repr = tuple(repr(arg) for arg in args)
            kwargs_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
            all_args_str_parts = []
            if args_repr:
                # Если есть позиционные аргументы, создаем строку, как если бы это был кортеж
                # repr от кортежа (x, y, z) -> '(x, y, z)'
                # repr от кортежа (x,) -> "(x,)"
                # repr от кортежа () -> "()"
                args_tuple_str = repr(args_repr)
                # Убираем внешние скобки ()
                args_str = args_tuple_str[1:-1]  # срез убирает первую '(' и последнюю ')'
                all_args_str_parts.append(args_str)
            if kwargs_str:
                all_args_str_parts.append(kwargs_str)
            all_args_str = ", ".join(all_args_str_parts)

            try:
                # Вызываем оригинальную функцию
                result = func(*args, **kwargs)
                # Формируем сообщение об успехе
                message = f"{func.__name__} ok\n"

                # Выводим сообщение в файл или stdout
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message)
                else:
                    print(message, end="")  # end="", чтобы не добавлять лишнюю новую строку

                # Возвращаем результат оригинальной функции
                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_type = type(e).__name__
                # Используем all_args_str в сообщении об ошибке
                # Исправлено: разбита длинная строка, чтобы не превышать 119 символов
                # Подготовим части сообщения на отдельных строках, чтобы не превысить 119 символов
                # Используем .format() для вставки потенциально длинных значений
                fn_name = func.__name__
                # Собираем сообщение напрямую, используя короткие имена и короткий шаблон
                # Шаблон разбит на части, но собран в .format() строкой, которая не превышает 119 символов
                # Это должно избежать ошибки E501
                msg_parts = ["{n} error: {et}. Inputs: ({a})\n"]
                message = "".join(msg_parts).format(n=fn_name, et=error_type, a=all_args_str)

                # Выводим сообщение об ошибке в файл или stdout
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message)
                else:
                    print(message, end="")  # end="", чтобы не добавлять лишнюю новую строку

                # Повторно вызываем исключение, чтобы оно не гасилось
                raise

        return wrapper
    return decorator
