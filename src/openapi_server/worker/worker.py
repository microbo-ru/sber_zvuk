import os
import time

from celery import Celery
from celery.utils.log import get_task_logger

import urllib.request
from urllib.parse import urlparse

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

logger = get_task_logger(__name__)

# import glob


@celery.task(name="process_file")
def process_file(url, prefix):
    # time.sleep(int(task_type) * 1)
    logger.info(f'Start Processing:')
    # files = glob.glob("/root/app/store/*")
    logger.info(f'{prefix} {url}')

    a = urlparse(url)
    file_name = os.path.basename(a.path)
    urllib.request.urlretrieve(url, f'/root/app/store/{prefix}_{file_name}')
    return True
    # return
