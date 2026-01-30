## Запуск проекта

### Вариант 1. Через Docker Compose (рекомендуется)

1. Соберите и запустите сервисы:

```bash
docker compose up --build
```

2. Приложение будет доступно по адресу:

- API: `http://localhost:8001`

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

3. Запустите приложение:

```bash
uvicorn backend.entrance.main:app --host 0.0.0.0 --port 8001 --reload
```

4. Инициализируйте базу данных:

```bash
curl -X POST http://localhost:8001/init-db
```

## Основные эндпоинты

- `POST /registration` — регистрация
- `POST /entrance` — вход (получение access/refresh токенов)
- `POST /refresh` — обновление access токена
- `GET /profile` — получить профиль (email/phone)
- `PATCH /profile` — обновить/очистить email или phone
- `POST /articles` — создать статью
- `GET /articles` — список своих статей
- `GET /articles/{id}` — получить свою статью
- `PATCH /articles/{id}` — редактировать статью
- `DELETE /articles/{id}` — удалить статью

Все защищённые запросы требуют заголовок:

```
Authorization: Bearer <access_token>
```

## Тесты

Запуск тестов из корня репозитория:

```bash
pytest
```
