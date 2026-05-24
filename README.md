# Electronics Store

API платформа для управления торговой сетью электроники.

## Технологии

- Python 3.13
- Django 4.2 + Django REST Framework
- PostgreSQL
- Redis + Celery
- Docker + Docker Compose

## Структура проекта

- **Head Office** — головной отдел, единственный в сети
- **Dealers** — дилерские центры, ведут учёт наличия товаров и суточную выручку

## Запуск

**1. Клонировать репозиторий**
```bash
git clone https://github.com/burvelandrei/Electronics_Store.git
cd electronics_store
```

**2. Создать `.env` из примера**
```bash
cp .env.example .env
```

**3. Запустить**
```bash
docker compose up --build
```

**4. Создать суперпользователя для админки**
```bash
docker compose exec app python manage.py createsuperuser
```

**5. Заполнить БД тестовыми данными**
```bash
docker compose exec app python manage.py seed
```

## API

Базовый URL: `http://localhost:8000/api/`

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/stores/` | Все торговые точки |
| GET | `/stores/?city=<city>` | Фильтр по городу |
| GET | `/stores/dealers/above-average/` | Дилеры с выручкой выше средней |
| GET | `/stores/by-product/?product_id=<id>` | Точки где есть продукт |
| POST | `/stores/` | Создать точку |
| GET/PATCH/DELETE | `/stores/<id>/` | Управление точкой |
| GET | `/stores/my/` | Своя точка (по API ключу) |
| GET/POST | `/products/` | Каталог продуктов |
| GET/PATCH/DELETE | `/products/<id>/` | Управление продуктом |

## Доступ

**Админка:** `http://localhost:8000/admin/`

**API** - только для аутентифицированных сотрудников (session auth).

**API по ключу** - передать заголовок `X-API-Key: <uuid>`, возвращает данные только своей точки.

## Celery задачи

- **09:00 ежедневно** - для позиций с нулевым остатком у дилеров увеличивает количество на случайное целое от 5 до 25 единиц
- **каждый час** - выбирает случайные позиции у случайного дилера, уменьшает остаток на случайное целое от 1 до 10 по каждой позиции, добавляет сумму списаний к суточной выручке дилера; если остаток позиции стал 0 - отправляет email сотруднику головного отдела с информацией о дилере и товаре
- **21:15 ежедневно** - обнуляет суточную выручку у всех дилерских центров

---

**Автор:** [burvelandrei](https://github.com/burvelandrei)
