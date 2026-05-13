from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60*24, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    APP_NAME: str = Field(default="Devinote", env="APP_NAME")
    ENVIRONMENT: str = Field(default="DEV", env="ENVIRONMENT")

    class Config:
        env_file = ".env"

settings = Settings()