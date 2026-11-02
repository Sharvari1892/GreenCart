from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union


class Settings(BaseSettings):
    PROJECT_NAME: str = "GreenCart API"
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # SQLite in-memory by default — no PostgreSQL required
    DATABASE_URL: Union[str, None] = "sqlite:///:memory:"

    # Legacy PostgreSQL fields (kept so existing .env files don't break)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "greencart"

    SECRET_KEY: str = "a_super_secret_jwt_key_for_greencart_dev_environment_32chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # Fallback to SQLite in-memory if nothing is configured
        return "sqlite:///:memory:"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
