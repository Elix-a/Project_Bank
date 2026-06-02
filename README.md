# Виджет банковского проекта

Этот проект является частью более крупного банковского приложения-виджета. Он предоставляет функциональность для:

- Маскировки номеров банковских карт (формат: `XXXX XX** **** XXXX`).
- Маскировки номеров банковских счетов (формат: `**XXXX`).
- Парсинга дат из формата ISO 8601 (`YYYY-MM-DDTHH:MM:SS.ffffff`) в формат `DD.MM.YYYY`.
- Фильтрации и сортировки списков банковских транзакций.

## Модули

- `src.masks`: Содержит основные функции маскировки (устаревшие).
- `src.widget`: Основной модуль с функциями `mask_account_card` и `get_date`.
- `src.processing`: Модуль для обработки данных транзакций (`filter_by_state`, `sort_by_date`).

## Примеры использования

### Маскировка данных и работа с датами
```

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


## Обработка транзакций

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

# Сортировка по возрастанию (старые сначала)
sorted_asc_txs = sort_by_date(transactions, ascending=True)
print(sorted_asc_txs)
```
## Установка и запуск
Для работы с проектом требуется Python 3.10+ и менеджер зависимостей Poetry.

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Elix-a/Project_Bank.git
cd Project_Bank
```
2. Установите зависимости:

```bash
poetry install
```

## Лицензия
MIT