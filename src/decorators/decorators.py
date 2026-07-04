import functools
import os
import sys


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
            # Мы хотим получить строку, как если бы аргументы были переданы в print или f-строку
            # repr от аргумента, join через ', '
            # Если аргумент один, repr даст x, но нам нужен x, (для кортежа с одним элементом)
            args_repr = [repr(arg) for arg in args]
            kwargs_str = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.items())

            # Собираем общую строку аргументов
            all_args_parts = []
            if args_repr:
                # Обрабатываем позиционные аргументы
                args_part = ', '.join(args_repr)
                # Если только один позиционный аргумент, добавляем запятую, чтобы показать, что это кортеж
                if len(args) == 1:
                    args_part += ","
                all_args_parts.append(args_part)
            if kwargs_str:
                all_args_parts.append(kwargs_str)
            all_args_str = ', '.join(all_args_parts)

            try:
                # Вызываем оригинальную функцию
                result = func(*args, **kwargs)
                # Формируем сообщение об успехе
                message = f"{func.__name__} ok\n"

                # Выводим сообщение в файл или stdout
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(message)
                else:
                    print(message, end='') # end='', чтобы не добавлять лишнюю новую строку, так как message уже содержит \n

                # Возвращаем результат оригинальной функции
                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_type = type(e).__name__
                # Используем all_args_str в сообщении об ошибке
                message = f"{func.__name__} error: {error_type}. Inputs: ({all_args_str})\n"

                # Выводим сообщение об ошибке в файл или stdout
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(message)
                else:
                    print(message, end='') # end='', чтобы не добавлять лишнюю новую строку

                # Повторно вызываем исключение, чтобы оно не гасилось
                raise

        return wrapper
    return decorator
