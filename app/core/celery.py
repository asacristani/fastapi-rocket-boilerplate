from celery import Celery

from app.settings import settings

celery = Celery(
    "main",
    broker=f"pyamqp://{settings.rabbit_user}:{settings.rabbit_password}@"
    f"{settings.rabbit_host}:{settings.rabbit_port}//",
    backend=f"redis://{settings.redis_host}:{settings.redis_port}/0",
)
