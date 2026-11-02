from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
from sqlalchemy.engine import URL

class Settings(BaseSettings):
    PROJECT_NAME: str = "GreenCart API"
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "greencart"
    DATABASE_URL: Union[str, None] = None

    SECRET_KEY: str = "a_super_secret_jwt_key_for_greencart_dev_environment_32chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @model_validator(mode="after")
    def validate_database_config(self):
        if self.DATABASE_URL and self.DATABASE_URL.startswith("sqlite") and self.ENVIRONMENT != "test":
            raise ValueError(
                "SQLite is only permitted in isolated test environments (ENVIRONMENT=test). "
                "GreenCart requires PostgreSQL for all standard execution."
            )
        return self

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            # Strictly restrict SQLite to isolated test environments
            if self.DATABASE_URL.startswith("sqlite") and self.ENVIRONMENT != "test":
                raise ValueError(
                    "SQLite is only permitted in isolated test environments (ENVIRONMENT=test). "
                    "GreenCart requires PostgreSQL for all standard execution."
                )
            return self.DATABASE_URL

        # Default is strictly PostgreSQL
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=int(self.DB_PORT),
            database=self.DB_NAME,
        ).render_as_string(hide_password=False)


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
