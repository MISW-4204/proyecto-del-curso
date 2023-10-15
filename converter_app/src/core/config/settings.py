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
    authjwt_algorithm: str = os.getenv('JWT_ALGORITHM')
    authjwt_secret_key:str = os.getenv('JWT_SECRET_KEY')
    authjwt_header_type:str = os.getenv('JWT_TYPE')
    authjwt_header_name:str = os.getenv('JWT_NAME')