import os
from celery import Celery
from .settings import settings

celery = Celery(__name__, broker=settings.redis_url, backend=settings.redis_url)

@celery.task
def ping():
    return "pong"
