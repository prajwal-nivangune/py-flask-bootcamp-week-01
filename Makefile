up:
	docker-compose up --build

down:
	docker-compose down

build:
	docker-compose build

restart:
	down up

migrate:
	docker-compose exec flask flask db upgrade
