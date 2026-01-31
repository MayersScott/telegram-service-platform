# Telegram Service Platform

[![CI](https://github.com/MayersScott/telegram-service-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/MayersScott/telegram-service-platform/actions/workflows/ci.yml)

Платформа “бот + backend” для обработки заявок: бот в Telegram принимает заявки, FastAPI хранит их в базе и отдаёт API, Celery отправляет уведомления о создании заявки и изменении статуса.

## Quick demo (Docker)

```bash
cp .env.example .env
# заполни SECRET_KEY, BOT_TOKEN, ADMIN_EMAIL, ADMIN_PASSWORD
docker compose up --build -d
```

- Swagger: http://localhost:8000/docs
- Flower: http://localhost:5555

Тест руками:
1) В Telegram: `/start` → `/new` → `/my`
2) В Swagger: логин админа → поменяй статус заявки → проверь уведомление

## Возможности

### Telegram-бот
- `/start` — регистрирует пользователя
- `/new` — создание заявки (тема → описание)
- `/my` — список заявок пользователя

### Backend (FastAPI)
- создание и просмотр заявок
- админские endpoints: список заявок, смена статуса, статистика
- JWT-авторизация для админки
- Swagger/OpenAPI (`/docs`)

### Очереди и фоновые задачи
- Redis + Celery
- уведомления при:
  - создании заявки
  - изменении статуса

## Мини-архитектура

```text
User -> Telegram Bot (Aiogram) -> FastAPI -> PostgreSQL
                               -> Redis (broker) -> Celery Worker -> Telegram sendMessage
```

## Примеры API (curl)

### 1) Логин админа (JWT)
```bash
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin12345"}'
```

### 2) Смена статуса заявки
```bash
curl -X PATCH http://localhost:8000/requests/1/status \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress"}'
```

## Demo

![Bot demo](docs/bot-demo.png)
![Swagger](docs/swagger.png)

## Стек

Python 3.12, FastAPI, SQLAlchemy (async), Alembic, PostgreSQL, Redis, Celery, Aiogram, Docker Compose.

## Demo

![Bot demo](docs/bot-demo.png)
![Swagger](docs/swagger.png)

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

Обязательные:
- `SECRET_KEY`
- `BOT_TOKEN`
- `ADMIN_EMAIL`, `ADMIN_PASSWORD` (пароль не длиннее 72 символов — ограничение bcrypt)

Docker-значения по умолчанию подходят:
- `DATABASE_URL=postgresql+asyncpg://tsp:tsp@postgres:5432/tsp`
- `CELERY_BROKER_URL=redis://redis:6379/1`
- `CELERY_RESULT_BACKEND=redis://redis:6379/2`
- `API_BASE_URL=http://backend:8000` (в Docker это не localhost)

## Структура проекта

```text
backend/   FastAPI + DB + Celery
bot/       Aiogram bot (клиент к backend API)
```

## Makefile

```bash
make up
make down
make ps
make logs
```

## Troubleshooting

### Бот не видит backend
В Docker должно быть:
```env
API_BASE_URL=http://backend:8000
```
Локально (без Docker):
```env
API_BASE_URL=http://localhost:8000
```

### Celery пишет “Received unregistered task …”
Проверь регистрацию задач (импорт `notifications` внутри `backend/app/tasks/__init__.py`).

## License
MIT (см. `LICENSE`)
