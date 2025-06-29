FROM python:3.12-alpine

WORKDIR /app

COPY auth_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY auth_service/alembic.ini ./auth_service/

COPY auth_service ./auth_service

CMD ["uvicorn", "auth_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

