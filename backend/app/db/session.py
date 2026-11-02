from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.config import settings

uri = settings.SQLALCHEMY_DATABASE_URI

if uri.startswith("sqlite"):
    # Use StaticPool so all connections share the same in-memory database.
    # This is the correct approach for SQLite :memory: in a web app.
    engine = create_engine(
        uri,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    engine = create_engine(uri, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
