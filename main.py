# main.py

import os
from datetime import datetime
from typing import Any, Dict, List

from src.processing import load_transactions_from_json
from src.readers import read_transactions_from_csv, read_transactions_from_excel
from src.search import search_by_description
from src.utils import filter_by_state, sort_by_date
from src.widget import mask_account_card


def get_file_choice() -> str:
    """Запрашивает у пользователя формат файла и возвращает путь к выбранному файлу."""
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    choice = input("Ваш выбор: ").strip()

    base_path = os.path.dirname(__file__)
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        return os.path.join(base_path, "data", "operations.json")
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        return os.path.join(base_path, "data", "transactions.csv")
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        return os.path.join(base_path, "data", "transactions_excel.xlsx")
    else:
        print("Некорректный выбор. Попробуйте снова.")
        return get_file_choice()


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции в зависимости от расширения файла."""
    _, ext = os.path.splitext(file_path)
    if ext == ".json":
        return load_transactions_from_json(file_path)
    elif ext == ".csv":
        return read_transactions_from_csv(file_path)
    elif ext == ".xlsx":
        return read_transactions_from_excel(file_path)
    else:
        print("Неподдерживаемый формат файла.")
        return []


def get_status() -> str:
    """Запрашивает статус операции до тех пор, пока не будет введён корректный."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = (
            input(
                "Введите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            )
            .strip()
            .upper()
        )
        if status in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        else:
            print(f'Статус операции "{status}" недоступен.')


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует одну транзакцию для вывода."""
    date_str = transaction.get("date", "")
    try:
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        formatted_date = date_obj.strftime("%d.%m.%Y")
    except (ValueError, AttributeError):
        formatted_date = date_str

    description = transaction.get("description", "")
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")
    amount = transaction.get("amount", "")
    currency_code = transaction.get("currency_code", "")

    if from_account and to_account:
        accounts = f"{mask_account_card(from_account)} -> {mask_account_card(to_account)}"
    elif to_account:
        accounts = mask_account_card(to_account)
    else:
        accounts = ""

    if currency_code == "RUB":
        currency_display = "руб."
    else:
        currency_display = currency_code

    lines = [f"{formatted_date} {description}"]
    if accounts:
        lines.append(accounts)
    lines.append(f"Сумма: {amount} {currency_display}")
    return "\n".join(lines)


def main() -> None:
    """Главная функция, реализующая пользовательский интерфейс."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    file_path = get_file_choice()
    transactions = load_transactions(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции. Программа завершена.")
        return

    status = get_status()
    filtered = filter_by_state(transactions, status)

    sort_choice = input("Отсортировать операции по дате? Да/Нет ").strip().lower()
    if sort_choice in ("да", "yes", "y"):
        direction = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if direction in ("по возрастанию", "возрастанию", "asc"):
            reverse = False
        else:
            reverse = True
        filtered = sort_by_date(filtered, reverse=reverse)

    rub_only = input("Выводить только рублевые транзакции? Да/Нет ").strip().lower()
    if rub_only in ("да", "yes", "y"):
        filtered = [t for t in filtered if t.get("currency_code") == "RUB"]

    filter_desc = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет ").strip().lower()
    if filter_desc in ("да", "yes", "y"):
        word = input("Введите слово для поиска в описании: ")
        filtered = search_by_description(filtered, word)

    print("Распечатываю итоговый список транзакций...")
    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered)}\n")
        for t in filtered:
            print(format_transaction(t))
            print()


if __name__ == "__main__":
    main()
