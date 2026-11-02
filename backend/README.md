# GreenCart Backend

FastAPI backend for GreenCart featuring an in-memory SQLite database, 15 famous Indian brands demo catalog, shopping cart & orders API, and Open Food Facts live comparison integration.

## Tech Stack

- **Python 3.10+**
- **FastAPI** & **Uvicorn**
- **SQLAlchemy 2.x** with `StaticPool`
- **SQLite In-Memory** (`sqlite:///:memory:`)
- **Pydantic v2**
- **HTTPX** (Asynchronous client for Open Food Facts API)

## Getting Started

### 1. Setup Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run Server
```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- **API Base:** `http://127.0.0.1:8000/api`
- **Interactive OpenAPI Documentation:** `http://127.0.0.1:8000/docs`

### 3. Automatic Seeding
No manual database setup, migrations, or seed commands required. On startup, the application creates all tables and seeds:
- 8 Product Categories
- 63 Products across 15 Indian Brands (Tata, Amul, Fabindia, Khadi India, Godrej, Patanjali, Himalaya, Mamaearth, boAt, Paper Boat, Asian Paints, Dabur, Aashirvaad, Noise, Forest Essentials)
- 2 Demo Users (`admin@greencart.demo`, `priya@greencart.demo`)

*Note: As an in-memory database, records reset when the server process terminates.*
