FROM python:3.12-alpine

WORKDIR /app
# пакеты для Aiokafka
RUN apk add --no-cache \
    git \
    build-base \
    python3-dev \
    musl-dev

RUN pip install --upgrade pip setuptools wheel

COPY auth_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY auth_service/alembic.ini ./auth_service/

COPY auth_service ./auth_service

CMD ["uvicorn", "auth_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

