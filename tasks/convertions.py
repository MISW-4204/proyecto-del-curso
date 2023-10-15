from celery import Celery
from settings import Settings

settings = Settings()
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

celery_app = Celery(__name__, broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0")