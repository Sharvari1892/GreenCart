from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.api import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    On startup: create all SQLite tables and seed demo data.
    NOTE: Data is stored in an in-memory SQLite database and resets on restart.
    """
    import app.db.base  # ensure all models are imported before create_all
    from app.db.session import engine, SessionLocal
    from app.db.base_class import Base
    from app.db.seed import seed_database

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    yield  # app runs here


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "details": str(exc)},
    )


app.include_router(api_router, prefix="/api")
