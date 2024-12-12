from pydantic_settings import BaseSettings
from cryptography.fernet import Fernet


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    API_V2_PREFIX: str = "/api/v2"
    
    # Add these new fields
    postgres_password: str
    postgres_user: str
    postgres_db: str
    postgres_port: str
    ci: str
    ENCRYPTION_KEY: str = Fernet.generate_key().decode()
    REDIS_URL: str = "redis://localhost:6379"
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_PRICE_ID: str
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
