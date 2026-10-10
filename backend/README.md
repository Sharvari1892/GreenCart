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
- PostgreSQL database server running locally or accessible remotely.

### 2. Virtual Environment & Dependencies
Create a virtual environment and install requirements:
```powershell
# Create venv
python -m venv venv

# Activate venv (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 3. Configuration
Copy the `.env.example` file to `.env` and fill in your actual PostgreSQL credentials:
```powershell
cp .env.example .env
```
Ensure that `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` match your Postgres setup. The app defaults to connecting to a database named `greencart` on localhost port 5432.

### 4. Database Initialization & Migrations
First, create a PostgreSQL database named `greencart` (or whatever you named it in your `.env`).

Then, apply the Alembic migrations to build the schema:
```powershell
# Set PYTHONPATH so alembic can find the app module
$env:PYTHONPATH="."
alembic upgrade head
```

### 5. Seeding Data
Run the seed script to populate the database with sample categories, products, and sustainability evidence:
```powershell
python scripts/seed.py
```

### 6. Starting the Server
Start the FastAPI application using `uvicorn`:
```powershell
uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.
- API Health Check: `http://127.0.0.1:8000/api/health`
- Swagger UI (Interactive API Docs): `http://127.0.0.1:8000/api/openapi.json` and `/docs`

### 7. Running Tests
Tests use an in-memory SQLite database.
```powershell
$env:PYTHONPATH="."
python -m pytest
```
