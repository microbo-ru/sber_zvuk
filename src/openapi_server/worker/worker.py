import os
import time

from celery import Celery
from celery.utils.log import get_task_logger

import urllib.request
from urllib.parse import urlparse

import boto3
import os

# from moviepy.editor import *

from preprocess import split_video, combine_video
from pathlib import Path

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
logger = get_task_logger(__name__)

def load_file_to_s3(output_dir_path, file_name, prefix):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://obs.ru-moscow-1.hc.sbercloud.ru/',
        aws_access_key_id=os.environ.get('AWS_S3_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_S3_SECRET_ACCESS_KEY'),
        use_ssl=False,
        verify=False
    )
    res =s3.upload_file(f'{output_dir_path}/{prefix}_{file_name}', 'hackathon-ecs-50', f'{prefix}_{file_name}')

@celery.task(name="process_file")
def process_file(url, prefix):
    logger.info(f'Start Processing:')
    logger.info(f'{prefix} {url}')

    a = urlparse(url)
    file_name = os.path.basename(a.path)
    input_file_path = f'/root/app/store/{prefix}_{file_name}'
    input_file_stem = Path(input_file_path).stem
    logger.info(input_file_stem)
    urllib.request.urlretrieve(url, input_file_path)

    logger.info(f'Start Framing:')

    output_dir_path = f'/root/app/store/dir_{prefix}_{input_file_stem}'
    Path(output_dir_path).mkdir(parents=True, exist_ok=True)

    logger.info(f'Start splitting')
    split_video(input_file_path, prefix, output_dir_path)
    logger.info(f'Finish Framing:')

    logger.info(f'Start combining')
    res_video_file_path = f'{output_dir_path}/{prefix}_extracted_video.mp4'
    res_audio_file_path = f'{output_dir_path}/{prefix}_extracted_audio.wav'
    res_video_combined = f'{output_dir_path}/{prefix}_{file_name}'
    combine_video(res_video_file_path, res_audio_file_path, res_video_combined)
    logger.info(f'Finish combining')

    logger.info(f'Start loading to s3:')
    load_file_to_s3(output_dir_path, file_name, prefix)
    logger.info(f'Finish Processing:')
    return True
