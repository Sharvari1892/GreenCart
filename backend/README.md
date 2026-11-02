# GreenCart Backend

Phase 1 Backend foundation for the GreenCart platform.

## Architecture & Tech Stack

- **Python 3.x**
- **FastAPI**
- **PostgreSQL** (via `psycopg2`)
- **SQLAlchemy 2.x** (ORM)
- **Alembic** (Migrations)
- **Pytest** (Testing)
- **Pydantic** (Validation & Settings)

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- PostgreSQL database server

### 2. Virtual Environment & Dependencies
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configuration
Copy the `.env.example` file to `.env` and fill in your actual PostgreSQL credentials and JWT secret:
```powershell
cp .env.example .env
```
Ensure you generate a secure random string for `SECRET_KEY`.

### 4. Database Initialization & Migrations
Create a PostgreSQL database named `greencart`.
Apply the Alembic migrations:
```powershell
$env:PYTHONPATH="."
alembic upgrade head
```

### 5. Seeding Data
```powershell
python scripts/seed.py
```

### 6. Starting the Server
```powershell
uvicorn app.main:app --reload
```
API runs on `http://127.0.0.1:8000`. Refer to `API_DOCUMENTATION.md` for endpoint details.

### 7. Running Tests
Tests use an in-memory SQLite database and do not touch production data.
```powershell
$env:PYTHONPATH="."
python -m pytest
```
