from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

uri = settings.SQLALCHEMY_DATABASE_URI

engine_kwargs = {}
if uri.startswith("sqlite"):
    if settings.ENVIRONMENT != "test":
        raise RuntimeError(
            "SQLite is only allowed in isolated test environments. "
            "Please configure PostgreSQL credentials in .env or set ENVIRONMENT=test for tests."
        )
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs["pool_pre_ping"] = True

engine = create_engine(uri, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
