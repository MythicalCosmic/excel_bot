APP_NAME=telegram-bot
SERVICE_NAME=bot


build:
	docker compose build


up:
	docker compose up -d


down:
	docker compose down


restart:
	docker compose restart $(SERVICE_NAME)


logs:
	docker compose logs -f $(SERVICE_NAME)


rebuild:
	docker compose down
	docker compose build
	docker compose up -d


sh:
	docker exec -it $(SERVICE_NAME) sh


prune:
	docker system prune -af --volumes
