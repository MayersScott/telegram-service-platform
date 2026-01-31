# Telegram Service Platform

[![CI](https://github.com/MayersScott/telegram-service-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/MayersScott/telegram-service-platform/actions/workflows/ci.yml)

Платформа “бот + backend” для заявок: Telegram-бот принимает заявки, FastAPI хранит их в PostgreSQL и отдаёт API, Celery отправляет уведомления о создании и изменении статуса.

## Quick demo (Docker)

```bash
cp .env.example .env
# заполни SECRET_KEY, BOT_TOKEN, ADMIN_EMAIL, ADMIN_PASSWORD
docker compose up --build -d
```

- Swagger: http://localhost:8000/docs  
- Flower: http://localhost:5555  

Проверка:
1) В Telegram: `/start` → `/new` → `/my`
2) В Swagger: логин админа → поменяй статус → проверь уведомление

## Возможности

**Telegram-бот**
- `/start` — регистрация пользователя
- `/new` — создание заявки (тема → описание)
- `/my` — список заявок пользователя

**Backend (FastAPI)**
- создание и просмотр заявок
- админские endpoints: список, смена статуса, статистика
- JWT-авторизация для админки
- Swagger/OpenAPI (`/docs`)

**Очереди и фоновые задачи**
- Redis + Celery
- уведомления в Telegram при:
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

> Положи скриншоты в `docs/`:
> - `docs/bot-demo.png`
> - `docs/swagger.png`

![Bot demo](docs/bot-demo.png)
![Swagger](docs/swagger.png)

## Статусы заявок

- `new` — Новая  
- `in_progress` — В работе  
- `done` — Завершена  
- `cancelled` — Отменена  

## Переменные окружения

Обязательные:
- `SECRET_KEY`
- `BOT_TOKEN` (BotFather)
- `ADMIN_EMAIL`, `ADMIN_PASSWORD` (**пароль <= 72 символов**, ограничение bcrypt)

Docker-значения по умолчанию уже подходят:
- `DATABASE_URL=postgresql+asyncpg://tsp:tsp@postgres:5432/tsp`
- `CELERY_BROKER_URL=redis://redis:6379/1`
- `CELERY_RESULT_BACKEND=redis://redis:6379/2`
- `API_BASE_URL=http://backend:8000` (в Docker это не localhost)

## Структура проекта

```text
backend/   FastAPI + DB + Celery
bot/       Aiogram bot (клиент к backend API)
docs/      скриншоты для README
```

## Makefile

```bash
make up
make down
make ps
make logs
```

## Troubleshooting

**Бот не видит backend**  
В Docker должно быть:
```env
API_BASE_URL=http://backend:8000
```
Локально (без Docker):
```env
API_BASE_URL=http://localhost:8000
```

**Celery пишет “Received unregistered task …”**  
Проверь регистрацию задач (импорт `notifications` внутри `backend/app/tasks/__init__.py`).

## License

MIT (см. `LICENSE`)
