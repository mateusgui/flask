# Registro de Incidentes (NOC)

Ambiente de desenvolvimento Dockerizado para a API Flask + PostgreSQL. A aplicação (models, rotas, etc.) ainda será escrita; este repositório só contém o esqueleto do projeto e a infraestrutura de desenvolvimento.

## Pré-requisitos

- Docker Desktop (Windows)

## Como subir

```
docker compose up -d --build
```

A API fica disponível em `http://localhost:8000` e recarrega automaticamente ao salvar arquivos em `backend/`.

## Como parar

```
docker compose down
```

## Como ver os logs

```
docker compose logs -f api
```

(troque `api` por `db` ou `adminer` para ver os logs dos outros serviços)

## Como abrir o Adminer

Acesse `http://localhost:8080` e use as credenciais definidas no `.env` (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`), com servidor `db`.

## Como rodar comandos do Flask dentro do container

```
docker compose exec api flask db init
docker compose exec api flask db migrate -m "mensagem"
docker compose exec api flask db upgrade
```

## Como zerar o banco

```
docker compose down -v
```

Isso remove o volume de dados do PostgreSQL, apagando todo o conteúdo do banco.
