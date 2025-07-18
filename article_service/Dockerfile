FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libffi-dev \
      libssl-dev \
      git \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel \
    && pip install Cython

COPY article_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY article_service ./article_service

CMD ["uvicorn", "article_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8003"]

