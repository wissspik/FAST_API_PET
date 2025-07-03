# Fast API Pet Project

This repository contains a set of small services used for educational purposes. Each service can be started separately using Docker Compose. The main components are:

- **auth_service** – user registration and JWT token issuance. [Documentation](auth_service/readme.md)
- **profile** – user profile management.
- **apigateway** – simple API gateway facade.
- **db_script** – helper compose file for PostgreSQL and Kafka initialization.

## Preparing environment files

1. Copy the existing example from `db_script/.env` and create `.env` files in `auth_service` and `profile` using variables described in their code. Minimum variables:
   - `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`
   - `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`
   - `ALGORITHM`, `SECRET_KEY`

2. Ensure `db_script/.env` contains valid credentials for PostgreSQL and Kafka.

## Running with Docker Compose

Create a shared Docker network once:

```bash
docker network create common_net
```

Start the database and Kafka services:

```bash
docker compose -f db_script/docker-compose_db.yml up -d
```

Then start the microservices:

```bash
docker compose -f auth_service/docker-compose_auth.yml up -d
```

```bash
docker compose -f profile/docker-compose_profile.yml up -d
```

Launch the API gateway locally:

```bash
uvicorn apigateway.gateway:app --reload --port 8000
```

After the containers are running the APIs will be available on ports `8001` and `8002`. The gateway listens on `8000`.
