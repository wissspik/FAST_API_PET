# auth_service

Сервис аутентификации (`auth_service`)

---

## Описание
Микросервис регистрации пользователей и выдачи JWT токенов.

---

## Архитектура и стек
- Язык: Python 3.11
- Тесты: Pytest
- Фреймворк: FastAPI
- База данных: PostgreSQL
- Кэш: Redis
- Docker + Docker Compose
- CI: GitHub Actions

---

## Предусловия
Для запуска проекта необходимы:
- Docker
- Docker Compose
- Доступ к репозиторию с секретными переменными

## Переменные окружения
- `DB_USER` – имя пользователя БД
- `DB_PASSWORD` – пароль пользователя БД
- `DB_HOST` – адрес сервера PostgreSQL
- `DB_PORT` – порт PostgreSQL
- `DB_NAME` – имя базы данных
- `REDIS_HOST` – адрес сервера Redis
- `REDIS_PORT` – порт Redis
- `REDIS_DB` – номер базы Redis
- `ALGORITHM` – алгоритм шифрования JWT
- `SECRET_KEY` – секретный ключ для подписи JWT
- `ACCESS_TOKEN_EXPIRE_MINUTES` – срок действия access-токена в минутах
- `REFRESH_TOKEN_EXPIRE_DAYS` – срок действия refresh-токена в днях
- `ENVIRONMENT` – тип окружения (`development` или `production`), влияет на работу флага `COOKIE_SECURE`
- `COOKIE_SECURE` – устанавливает атрибут `secure` у cookie. По умолчанию `False` в режиме `development`
- `TEST_DATABASE_URL` – строка подключения к БД для тестов

## Миграции БД (Alembic)
1. Создать новую миграцию:
   ```bash
   alembic revision -m "Комментарий"
   ```
2. Применить миграции:
   ```bash
   alembic upgrade head
   ```

## Установка и локальный запуск
1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/wissspik/FAST_API_PET.git
   cd FAST_API_PET
   ```
2. Создать файл `.env` в директории `auth_service` и заполнить его переменными окружения из списка выше.
3. Собрать и запустить контейнеры:
   ```bash
   docker-compose up --build
   ```
4. Для запуска фронтенда в отдельном терминале:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
5. Запуск тестов (при наличии переменной `TEST_DATABASE_URL`):
   ```bash
   pytest -q