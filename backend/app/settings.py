from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://ipam:ipam@db:5432/ipam"
    redis_url: str = "redis://redis:6379/0"
    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
