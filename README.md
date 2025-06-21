# FAST_API_PET

## Installation

### Python dependencies
1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install backend requirements:
   ```bash
   pip install -r auth_service/requirements.txt
   ```

### Node dependencies
1. Install front‑end packages:
   ```bash
   cd frontend
   npm install
   ```
   Return to the project root when done.

## Running the application

### Backend
- Using Docker (recommended):
  ```bash
  docker-compose up
  ```
  This starts Postgres, Redis and the FastAPI app.

- Running with Uvicorn directly:
  ```bash
  uvicorn auth_service.main:app --reload
  ```
  Ensure Postgres and Redis are running locally and all environment variables are configured.

### Frontend
In a separate terminal:
```bash
cd frontend
npm run dev
```
This serves the React application using Vite on `http://localhost:3000`.

## Environment variables
Create an `.env` file inside the `auth_service` folder with the following values:

```env
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_PORT=...
DB_NAME=...
SECRET_KEY=...
ALGORITHM=...
ACCESS_TOKEN_EXPIRE_MINUTES=...
REFRESH_TOKEN_EXPIRE_DAYS=...
REDIS_HOST=...
REDIS_PORT=...
REDIS_DB=...
```
These variables are required for the backend to connect to the database, issue JWT tokens and communicate with Redis.
