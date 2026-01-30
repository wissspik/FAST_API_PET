FROM python:3.12-slim

WORKDIR /app

COPY backend/entrance/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY alembic.ini /app/alembic.ini
COPY backend /app/backend

ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.entrance.main:app", "--host", "0.0.0.0", "--port", "8001"]
