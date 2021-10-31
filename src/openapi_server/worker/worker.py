import os
import time

from celery import Celery
from celery.utils.log import get_task_logger

import urllib.request
from urllib.parse import urlparse

import boto3
import os

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
logger = get_task_logger(__name__)

def load_file_to_s3(file_name, prefix):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://obs.ru-moscow-1.hc.sbercloud.ru/',
        aws_access_key_id=os.environ.get('AWS_S3_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_S3_SECRET_ACCESS_KEY'),
        use_ssl=False,
        verify=False
    )
    res =s3.upload_file(f'/root/app/store/{prefix}_{file_name}', 'hackathon-ecs-50', {prefix}_{file_name})
    logger.info(f'S3 loading: {res}')

@celery.task(name="process_file")
def process_file(url, prefix):
    logger.info(f'Start Processing:')
    logger.info(f'{prefix} {url}')

    a = urlparse(url)
    file_name = os.path.basename(a.path)
    urllib.request.urlretrieve(url, f'/root/app/store/{prefix}_{file_name}')

    logger.info(f'Start Framing:')
    #todo:
    logger.info(f'Finish Framing:')

    logger.info(f'Finish Processing:')
    return True
