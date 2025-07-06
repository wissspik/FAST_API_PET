FROM python:3.12-slim

WORKDIR /app
# пакеты для Aiokafka
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libffi-dev \
      libssl-dev \
      git \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel \
    && pip install Cython

COPY auth_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY auth_service/alembic.ini ./auth_service/

COPY auth_service ./auth_service

CMD ["uvicorn", "auth_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]


