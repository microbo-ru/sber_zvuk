import os
import time

from celery import Celery
from celery.utils.log import get_task_logger

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

logger = get_task_logger(__name__)

@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 1)
    logger.info(f'Test task')
    return True
