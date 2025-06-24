# Название сервиса

Сервис аутендификации ('auth_service')


---


## Описание
>Микросервис регистрации пользователей,выдачи JWT токенов.


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

Чтобы запустить проект,на машине нужно иметь:
- Docker
- Docker-compose
- Доступ к репозиторию с секретными переменными 


## Установка и локальный запуск
0. Запуск тестов(опционально)
   ```bash
   pytest -q
1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/wissspik/FAST_API_PET.git
   cd auth-service
2. Запустить backend and frontend:
   ```bash
   docker-compose -f docker-compose.auth-service.yml up --build
   cd ..
   cd frontend
   npm run dev
   ```
   