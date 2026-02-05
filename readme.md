# Wibe

## Запуск проекта

### Вариант 1. Через Docker Compose (рекомендуется)

1. Соберите и запустите сервисы:

```bash
docker compose up --build
```

2. Приложение будет доступно по адресу:

- Auth API: `http://localhost:8001`
- Articles API: `http://localhost:8002`
- Profile API: `http://localhost:8003`
- Interactions API: `http://localhost:8004`

3. Инициализируйте базу данных (создаст таблицы):

```bash
curl -X POST http://localhost:8001/init-db
```

### Вариант 2. Локально без Docker

1. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r backend/entrance/requirements.txt
```

2. Убедитесь, что PostgreSQL и Redis запущены, и параметры подключения корректны.
   По умолчанию используются:
   - PostgreSQL: `postgresql+asyncpg://appuser:strongpass@postgres:5432/full_db`
   - Redis: `redis://redis:6379/0`

3. Запустите сервисы (в разных терминалах):

```bash
uvicorn backend.entrance.main:app --host 0.0.0.0 --port 8001 --reload
uvicorn backend.articles_service.main:app --host 0.0.0.0 --port 8002 --reload
uvicorn backend.profile_service.main:app --host 0.0.0.0 --port 8003 --reload
uvicorn backend.interactions_service.main:app --host 0.0.0.0 --port 8004 --reload
```

4. Инициализируйте базу данных:

```bash
curl -X POST http://localhost:8001/init-db
```

## Основные эндпоинты

Auth (8001):
- `POST /registration` — регистрация
- `POST /entrance` — вход (получение access/refresh токенов)
- `POST /refresh` — обновление access токена

Profile (8003):
- `GET /profile` — получить профиль (email/phone)
- `GET /profile/{login}` -- view profile by login
- `PATCH /profile` — обновить/очистить email или phone

Articles (8002):
- `POST /articles` — создать статью
- `GET /articles` — список своих статей
- `GET /articles/{id}` — получить свою статью
- `PATCH /articles/{id}` — редактировать статью
- `DELETE /articles/{id}` — удалить статью

Interactions (8004):
- `POST /comments` -- create comment
- `GET /comments/article/{article_id}` -- list comments for article
- `DELETE /comments/{comment_id}` -- delete own comment
- `POST /likes/{article_id}` -- like article
- `DELETE /likes/{article_id}` -- unlike article
- `GET /likes/{article_id}` -- likes count
- `POST /views/{article_id}` -- register view
- `GET /views/{article_id}` -- views count

Все защищённые запросы требуют заголовок:

```
Authorization: Bearer <access_token>
```

## Тесты

Запуск тестов из корня репозитория:

```bash
pytest
```




