.PHONY: help docker-build docker-up docker-down docker-ps docker-logs

help:
	@echo Comandos disponiveis:
	@echo   make docker-build - constroi as imagens
	@echo   make docker-up    - inicia os servicos
	@echo   make docker-down  - encerra os servicos
	@echo   make docker-ps    - lista os servicos
	@echo   make docker-logs  - exibe os logs da API

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-ps:
	docker compose ps

docker-logs:
	docker compose logs api
