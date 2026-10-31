.PHONY: help install test lint format run up up-build down build logs logs-api ps shell clean db-upgrade db-migration db-current

POETRY := poetry -C backend
PYTEST := $(POETRY) run pytest
RUFF := $(POETRY) run ruff
UVICORN := $(POETRY) run uvicorn

help:
	@echo "Comandos disponiveis:"
	@echo "  make install"
	@echo "  make test"
	@echo "  make lint"
	@echo "  make format"
	@echo "  make run"
	@echo "  make up"
	@echo "  make up-build"
	@echo "  make down"
	@echo "  make build"
	@echo "  make logs"
	@echo "  make logs-api"
	@echo "  make ps"
	@echo "  make shell"
	@echo "  make clean"
	@echo "  make db-upgrade"
	@echo "  make db-migration msg="create items""
	@echo "  make db-current"

install:
	$(POETRY) install

test:
	$(PYTEST)

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

run:
	$(UVICORN) app.main:app --reload

up:
	docker compose up -d

up-build:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

logs-api:
	docker compose logs -f api

ps:
	docker compose ps

shell:
	docker compose exec api sh

clean:
	docker compose down -v

db-upgrade:
	cd backend && poetry run alembic upgrade head

db-migration:
	cd backend && poetry run alembic revision --autogenerate -m "Send a message to a user.  MSG {username | sessionname | sessionid | @filename | *}     [/SERVER:servername] [/TIME:seconds] [/V] [/W] [message]    username            Identifies the specified username.   sessionname         The name of the session.   sessionid           The ID of the session.   @filename           Identifies a file containing a list of usernames,                       sessionnames, and sessionids to send the message to.   *                   Send message to all sessions on specified server.   /SERVER:servername  server to contact (default is current).   /TIME:seconds       Time delay to wait for receiver to acknowledge msg.   /V                  Display information about actions being performed.   /W                  Wait for response from user, useful with /V.   message             Message to send.  If none specified, prompts for it                       or reads from stdin. "

db-current:
	cd backend && poetry run alembic current


.PHONY: frontend-install frontend-dev frontend-lint frontend-format frontend-check frontend-test frontend-test-e2e frontend-build check-all

frontend-install:
	npm --prefix frontend ci

frontend-dev:
	npm --prefix frontend run dev

frontend-lint:
	npm --prefix frontend run lint

frontend-format:
	npm --prefix frontend run format

frontend-check:
	npm --prefix frontend run check

frontend-test:
	npm --prefix frontend run test

frontend-test-e2e:
	npm --prefix frontend run test:e2e

frontend-build:
	npm --prefix frontend run build

check-all: lint test frontend-check frontend-test frontend-build frontend-test-e2e
