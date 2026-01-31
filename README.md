# Telegram Service Platform

Платформа “бот + backend” для обработки заявок: Telegram-бот принимает заявки от пользователей, FastAPI хранит их в базе и отдаёт API, Celery отправляет уведомления о создании заявки и изменении статуса.

## Возможности

### Telegram-бот
- `/start` — регистрация пользователя
- `/new` — создание заявки (тема → описание)
- `/my` — список заявок пользователя

### Backend (FastAPI)
- создание и просмотр заявок
- админские endpoints: список заявок, смена статуса, статистика
- JWT-авторизация для админки
- Swagger/OpenAPI (`/docs`)

### Очереди и фоновые задачи
- Redis + Celery
- уведомления в Telegram при:
  - создании заявки
  - изменении статуса

## Стек

Python 3.12, FastAPI, SQLAlchemy (async), Alembic, PostgreSQL, Redis, Celery, Aiogram, Docker Compose.

## Demo

Добавь скриншоты в папку `docs/`:
- `docs/bot-demo.png` — пример работы бота
- `docs/swagger.png` — Swagger UI

После этого секция будет выглядеть так:

```md
![Bot demo](docs/bot-demo.png)
![Swagger](docs/swagger.png)
```

## Быстрый старт (Docker)

1) Создай `.env`:
```bash
cp .env.example .env
```

2) Заполни обязательные переменные в `.env`:
- `SECRET_KEY` — секрет для подписи JWT
- `BOT_TOKEN` — токен Telegram бота (BotFather)
- `ADMIN_EMAIL`, `ADMIN_PASSWORD` — учётка админа (создаётся при старте)

Важно: `ADMIN_PASSWORD` должен быть не длиннее **72 символов** (ограничение bcrypt).

3) Запуск:
```bash
docker compose up --build -d
```

Ссылки:
- Swagger: `http://localhost:8000/docs`
- Flower: `http://localhost:5555`

## Как проверить работу

1) В Telegram:
- `/start`
- `/new` → создать заявку
- `/my` → убедиться, что заявка отображается

2) В Swagger:
- `POST /auth/login` → получить `access_token`
- нажать `Authorize` → `Bearer <token>`
- `GET /requests/` → увидеть заявки
- `PATCH /requests/{id}/status` → поменять статус

После смены статуса пользователю приходит уведомление в Telegram.

## Статусы заявок

- `new` — Новая
- `in_progress` — В работе
- `done` — Завершена
- `cancelled` — Отменена

## Переменные окружения

Что обычно меняют вручную:
- `SECRET_KEY`
- `BOT_TOKEN`
- `ADMIN_EMAIL`, `ADMIN_PASSWORD`

Docker-значения по умолчанию подходят:
- `DATABASE_URL=postgresql+asyncpg://tsp:tsp@postgres:5432/tsp`
- `CELERY_BROKER_URL=redis://redis:6379/1`
- `CELERY_RESULT_BACKEND=redis://redis:6379/2`
- `API_BASE_URL=http://backend:8000` (важно: внутри Docker это не localhost)

## Структура проекта

```text
backend/   FastAPI + DB + Celery
bot/       Aiogram bot (клиент к backend API)
```

## Makefile (если используешь)

```bash
make up
make down
make ps
make logs
```

## Troubleshooting

### Бот не видит backend
Проверь в `.env`:
```env
API_BASE_URL=http://backend:8000
```

Если запускаешь без Docker, тогда:
```env
API_BASE_URL=http://localhost:8000
```

### Celery пишет “Received unregistered task …”
Проверь регистрацию задач (импорт `notifications` внутри `backend/app/tasks/__init__.py`).

### Ошибка “password cannot be longer than 72 bytes”
Сократи `ADMIN_PASSWORD` (≤72 символов) и перезапусти контейнеры.

## License
MIT (см. `LICENSE`)
