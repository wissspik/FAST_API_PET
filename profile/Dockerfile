FROM python:3.12-alpine

WORKDIR /app

COPY profile/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY profile/alembic.ini ./profile/

COPY profile ./profile

CMD ["uvicorn", "profile.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

