import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    CELERY_QUEUE: str = os.getenv("CELERY_QUEUE")

    class Config:
        case_sensitive = True

class AuthSettings(BaseSettings):
    authjwt_secret_key:str = os.getenv('JWT_SECRET_KEY')