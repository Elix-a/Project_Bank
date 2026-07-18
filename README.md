# Виджет банковского проекта

Этот проект является частью более крупного банковского приложения-виджета. Он предоставляет функциональность для:

- Маскировки номеров банковских карт (формат: `XXXX XX** **** XXXX`).
- Маскировки номеров банковских счетов (формат: `**XXXX`).
- Парсинга дат из формата ISO 8601 (`YYYY-MM-DDTHH:MM:SS.ffffff`) в формат `DD.MM.YYYY`.
- Фильтрации и сортировки списков банковских транзакций.
- Генерации и фильтрации данных транзакций.
- Логирования вызовов функций.
- Анализа транзакций, формирования JSON-ответов для веб-страниц, расчёта инвестиционной копилки и генерации отчётов (курсовая работа).

## Модули

- `src.masks`: Содержит основные функции маскировки (устаревшие).
- `src.widget`: Основной модуль с функциями `mask_account_card` и `get_date`.
- `src.processing`: Модуль для обработки данных транзакций (`filter_by_state`, `sort_by_date`).
- `src.generators`: Модуль для генерации и фильтрации данных транзакций (`filter_by_currency`, `transaction_descriptions`, `card_number_generator`).
- `src.decorators`: Модуль для декораторов (`log`).
- `src.utils`: Модуль для вспомогательных функций, включая загрузку транзакций из Excel, приветствие по времени и фильтрацию по дате.
- `src.external_api`: Модуль для взаимодействия с внешними API, например, для конвертации валюты (`convert_to_rub`).
- `src.readers`: Модуль для чтения транзакций из CSV и Excel-файлов.
- `src.search`: Модуль для поиска транзакций по описанию и подсчёта по категориям.
- `src.views`: Модуль для генерации JSON-ответов для веб-страниц (главная страница).
- `src.services`: Модуль сервисов, включая расчёт отложенной суммы в «Инвесткопилку».
- `src.reports`: Модуль для отчётов с декоратором записи в файл, содержит отчёт «Траты по дням недели».

## Зависимости

Проект использует следующие дополнительные библиотеки:
- `requests`: Для отправки HTTP-запросов к внешним API.
- `python-dotenv`: Для загрузки переменных окружения из файла `.env`.
- `pandas`: Для работы с табличными данными (чтение Excel, анализ транзакций).
- `openpyxl`: Для чтения Excel-файлов.

## Примеры использования

### Маскировка данных и работа с датами

```python
from src.widget import mask_account_card, get_date

# Маскировка карты
print(mask_account_card("Visa Platinum 7000792289606361"))
# Вывод: Visa Platinum 7000 79** **** 6361

# Маскировка счета
print(mask_account_card("Счет 73654108430135874305"))
# Вывод: Счет **4305

# Преобразование даты
print(get_date("2024-03-11T02:26:18.671407"))
# Вывод: 11.03.2024
```
### Обработка транзакций
```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]

# Фильтрация по статусу (по умолчанию EXECUTED)
executed_txs = filter_by_state(transactions)
print(executed_txs)

# Сортировка по дате (по убыванию - новые сначала)
sorted_txs = sort_by_date(transactions)
print(sorted_txs)
```
###  Генерация и фильтрация данных транзакций

```python
from src.generators.generators import filter_by_currency, transaction_descriptions, card_number_generator

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    # ... другие транзакции ...
]

# Фильтрация по валюте
usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))

# Генерация описаний
descriptions = transaction_descriptions(transactions)
for _ in range(2):
    print(next(descriptions))

# Генерация номеров карт
for card_number in card_number_generator(1, 3):
    print(card_number)
```

## Логирование вызовов функций
```python
from src.decorators.decorators import log

@log(filename="function_calls.log")
def calculate_sum(a, b):
    return a + b

@log()
def divide_numbers(x, y):
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return x / y

result1 = calculate_sum(5, 3)
print(f"Sum result: {result1}")

try:
    result2 = divide_numbers(10, 0)
except ZeroDivisionError as e:
    print(f"Caught error: {e}")

result3 = divide_numbers(10, 2)
print(f"Division result: {result3}")
```

## Логирование

Проект использует библиотеку `logging` для отслеживания работы приложения.
Логи записываются в файлы в папке `logs/`:
- `logs/utils.log` - логи модуля `utils` (например, загрузка транзакций).
- `logs/masks.log` - логи модуля `masks` (например, маскировка номеров).

Формат логов: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`.

## Чтение транзакций из файлов

Проект поддерживает чтение транзакций из CSV и Excel (XLSX).
```python
from src.readers import read_transactions_from_csv, read_transactions_from_excel

csv_data = read_transactions_from_csv("data/transactions.csv")
excel_data = read_transactions_from_excel("data/transactions_excel.xlsx")
```

## Новая функциональность (Урок по `re`, `collections`, `random`)

- **Поиск по описанию:** Возможность фильтровать транзакции по ключевым словам в поле `description` с использованием регулярных выражений (`re`).
- **Подсчёт по категориям:** Функция для подсчёта количества транзакций, соответствующих определённым категориям, с использованием `Counter` из `collections`.
- **Интерактивный интерфейс:** Консольное приложение (`main.py`), позволяющее пользователю загружать данные из JSON/CSV/XLSX, фильтровать по статусу, сортировать по дате, выбирать только рублёвые транзакции и фильтровать по описанию.

## Курсовая работа: Анализ транзакций
#### В рамках курсовой работы реализованы новые модули, расширяющие возможности проекта.

## Настройки (user_settings.json)
#### Перед использованием модулей views, services и reports необходимо настроить список отслеживаемых валют и акций в файле user_settings.json в корне проекта.
Пример содержимого:
```python
{
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
```
## Веб-страницы (src/views.py)
#### Генерирует JSON-ответ для главной страницы. Включает приветствие, информацию по картам, топ-5 транзакций, курсы валют и стоимость акций.
```python
from src.views import generate_main_view

json_response = generate_main_view("2023-09-15 12:30:00")
print(json_response)
```
Пример JSON-ответа:
```bash
{
  "greeting": "Добрый день",
  "cards": [
    {
      "last_digits": "1234",
      "total_spent": 4500.00,
      "cashback": 45.00
    }
  ],
  "top_transactions": [
    {
      "date": "20.09.2023",
      "amount": 2500.00,
      "category": "Транспорт",
      "description": "Метро"
    }
  ],
  "currency_rates": [
    {"currency": "USD", "rate": 75.5},
    {"currency": "EUR", "rate": 87.2}
  ],
  "stock_prices": [
    {"stock": "AAPL", "price": 150.25},
    {"stock": "TSLA", "price": 750.10}
  ]
}
```
## Сервисы (src/services.py)
####  Сервис «Инвесткопилка» рассчитывает сумму, которую можно отложить за месяц, округляя траты до заданного лимита.
```python
from src.services import investment_bank

transactions = [
    {"Дата операции": "2023-03-05", "Сумма операции": 1712},
    {"Дата операции": "2023-03-12", "Сумма операции": 230},
    {"Дата операции": "2023-03-20", "Сумма операции": 987}
]

saved = investment_bank("2023-03", transactions, limit=50)
print(f"Отложено в копилку: {saved} руб.")
# Вывод: Отложено в копилку: 71.0 руб.
```
## Отчёты (src/reports.py)
#### Модуль содержит декоратор report_to_file, который сохраняет результат отчёта в файл, и функцию spending_by_weekday для расчёта средних трат по дням недели за последние три месяца.
```python
from src.reports import report_to_file, spending_by_weekday
import pandas as pd

# Пример DataFrame с транзакциями
df = pd.read_excel("data/operations.xlsx")

# Расчёт средних трат по дням недели с сохранением в файл
@report_to_file("my_report.txt")
def weekday_report():
    return spending_by_weekday(df, date="2023-09-15")

weekday_report()
```

## Тестирование
### Проект использует фреймворк pytest для написания и запуска тестов.
#### Для запуска всех тестов выполните:

```bash
poetry run pytest
```

####  Для запуска тестов с отчётом о покрытии в формате HTML:

```bash
poetry run pytest --cov=src --cov-report=html
```

#### Отчёт будет доступен в файле htmlcov/index.html.

### Текущее покрытие кода тестами: 97% (114 тестов).
## Установка и запуск

### Для работы с проектом требуется Python 3.10+ и менеджер зависимостей Poetry.

#### 1. Клонируйте репозиторий:

```bash
git clone https://github.com/Elix-a/Project_Bank.git
cd Project_Bank
```

#### 2. Установите зависимости:

```bash
poetry install
```
### Скопируйте файл .env.example в .env и заполните необходимыми ключами (API-ключ для валют и акций).

### Разместите файл operations.xlsx в папке data/.

## Лицензия

MIT