import os

os.environ["STRIPE_SECRET_KEY"] = "REDACTED"
os.environ["STRIPE_WEBHOOK_SECRET"] = "REDACTED"
os.environ["DATABASE_URL"] = "sqlite:///database.db"
os.environ["SECRET_KEY"] = "REDACTED"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["OPENAI_API_KEY"] = "REDACTED"
# --------------------------------------------------------------------------------------

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    DATABASE_URL: str = "sqlite:///database.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OPENAI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=None, 
        extra="ignore"
    )

settings = Settings()
