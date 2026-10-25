# Сервис учёта посылок

## Назначение
Консольное приложение для учёта посылок: создание, поиск, фильтрация,
изменение статуса и сортировка.

## Целевая аудитория
- Сотрудники склада и аналитики почтовых сервисов
- Пользователи, отправляющие и получающие посылки

## Предметная область
Учёт отправлений: отправитель, получатель, категория, даты, вес, статус.

## Основные сущности (классы)

### `User` — пользователь (`models/users.py`)
**Атрибуты:** `id`, `name`, `email`.
**Методы:** `__init__`, `__str__`, `validate_name()` (`@staticmethod`),
`from_data()` (`@classmethod`).
**Функции модуля:** `add_user`, `find_user`, `find_user_by_id`, `show_users`.

### `Package` — посылка (`models/packages.py`)
**Атрибуты:** `id`, `category`, `departure_date`, `arrival_date`,
`weight`, `status`, `sender: User`, `recipient: User`.
**Методы:** `__init__`, `__str__`, `change_status()`, `is_delivered()`,
`validate_weight()` (`@staticmethod`), `from_data()` (`@classmethod`).
**Функции модуля:** `add_package`, `find_package_by_id`, `get_all_packages`,
`get_package_status`, `change_package_status`, `filter_packages_by_category`,
`sort_packages_by_weight`, `show_packages`.

### `Courier` — доставщик (`models/couriers.py`)
**Атрибуты:** `id`, `name`, `phone`, `vehicle`, `departure_date`,
`expected_delivery_date`, `capacity_kg`, `is_available`,
`packages: List[Package]`.
**Методы:** `__init__`, `__str__`, `total_weight()`, `can_take_package()`,
`assign_package()`, `release_package()`, `validate_phone()` (`@staticmethod`),
`from_data()` (`@classmethod`).
**Функции модуля:** `add_courier`, `find_courier_by_id`, `find_free_couriers`,
`assign_package_to_best_courier`, `show_couriers`.

**Взаимодействие:** `Courier.packages ↔ Package.courier` — двусторонняя
связь. `Courier.expected_delivery_date` должен совпадать с `Package.arrival_date`,
иначе `can_take_package()` вернёт `False`. В JSON хранятся `courier_id`
в посылке и `package_ids` в доставщике; при загрузке связь восстанавливается
в `storage.load_packages()`.

## Взаимодействие объектов
`Package` хранит **объекты** `User` (а не только их id), поэтому доступны
`package.sender.name`, `package.recipient.email` и т.п.
В JSON сохраняются только `sender_id` и `recipient_id`; при загрузке
`storage.load_packages()` находит объекты `User` в коллекции и передаёт их
в `Package.from_data()`.

## Структура проекта
packages_service/  
├── main.py  
├── storage.py  
├── utils/  
│ ├── init.py  
│ └── input_utils.py  
├── models/  
│ ├── init.py  
│ ├── couriers.py  
│ ├── users.py  
│ └── packages.py  
├── data/  
│ ├── couriers.json  
│ ├── users.json  
│ └── packages.json
└── tests/  
├── conftest.py  
├── test_couriers.py  
├── test_users.py  
└── test_packages.py  


## Хранение данных
JSON-файлы `data/users.json` и `data/packages.json`.
Загрузка: JSON → `dict` → `User` / `Package` → объекты.
Сохранение: объекты → `dict` с `sender_id` / `recipient_id` → JSON.

## Запуск
```bash
pip install -r requirements.txt
python main.py
```

## Тесты
```bash
pytest
```

## Проверка качества кода
```bash
flake8 .
```


## Используемые технологии
- Python 3
- Django 5.2 — веб-фреймворк
- HTML, CSS, Bootstrap 5.3 (CDN)
- JSON-файлы — источник данных (ПР3)
- pytest, flake8

## Веб-страницы (ПР5)
| URL | Назначение | View |
|---|---|---|
| `/` | главная, навигация | `homepage.views.index` |
| `/packages/` | список посылок | `packages.views.packages` |
| `/packages/<int:package_id>/` | карточка посылки (404, если нет) | `packages.views.package_detail` |
| `/couriers/` | список доставщиков | `couriers.views.couriers` |
| `/couriers/<int:courier_id>/` | карточка доставщика (404, если нет) | `couriers.views.courier_detail` |

Общая 404-страница: `homepage.views.page_not_found` через `handler404`.

## Запуск веб-версии
```bash
python manage.py migrate
python manage.py runserver
# http://127.0.0.1:8000/