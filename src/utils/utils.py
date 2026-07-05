import json
import logging
import os
from typing import Any, Dict, List

# --- Настройка логирования для модуля utils ---
# Создаём папку logs, если её нет
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаём обработчик для файла
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаём форматтер
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем обработчик к логеру
logger.addHandler(file_handler)


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
        Если файл не найден, пустой или содержит не список, возвращается пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Проверяем, что данные — это список
            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
                return data
            else:
                logger.warning(f"Файл {file_path} содержит не список, возвращаем пустой список.")
                return []
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден.", exc_info=True)
        return []
    except json.JSONDecodeError:
        logger.error(f"Файл {file_path} содержит некорректный JSON.", exc_info=True)
        return []
    except OSError as e:
        logger.error(f"Ошибка доступа к файлу {file_path}: {e}", exc_info=True)
        return []
