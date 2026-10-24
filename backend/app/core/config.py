from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
from sqlalchemy.engine import URL

class Settings(BaseSettings):
    PROJECT_NAME: str = "GreenCart API"
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
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
