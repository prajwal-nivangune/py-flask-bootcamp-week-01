# Makefile for Flask + Docker Compose

# Default target
up:
	docker-compose up --build

# Stop and remove containers
down:
	docker-compose down

# Build only
build:
	docker-compose build

# Restart services
restart: down up

# Run Flask shell (optional)
shell:
	docker-compose exec flask flask shell

# Run Flask migrations (if using Flask-Migrate)
migrate:
	docker-compose exec flask flask db upgrade

# Clean up unused images/containers
clean:
	docker system prune -f
