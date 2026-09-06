# C216-L1

Repositório das práticas da disciplina C216 L1 - Sistemas Distribuídos.

## Ambiente Docker

A aplicação utiliza:

- FastAPI
- Docker
- Docker Compose
- PostgreSQL

## Subir o ambiente

```bash
docker compose up -d
```

## Verificar os serviços

```bash
docker compose ps
```

## Visualizar os logs da API

```bash
docker compose logs api
```

## Encerrar o ambiente

```bash
docker compose down
```

## Makefile

```bash
make docker-build
make docker-up
make docker-down
make docker-ps
make docker-logs
```
