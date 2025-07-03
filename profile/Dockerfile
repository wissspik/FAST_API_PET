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

COPY profile/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY profile/alembic.ini ./profile/

COPY profile ./profile

CMD ["uvicorn", "profile.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

