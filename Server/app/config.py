from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DB_NAME: str = "entertainment_tracker"

    class Config:
        env_file = ".env"


settings = Settings()
