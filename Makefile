up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

restart:
	docker compose restart

rebuild:
	docker compose build --no-cache
	docker compose up -d --force-recreate

backend-logs:
	docker compose logs -f --tail=200 backend

worker-logs:
	docker compose logs -f --tail=200 worker

bot-logs:
	docker compose logs -f --tail=200 bot
