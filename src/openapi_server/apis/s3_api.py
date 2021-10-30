# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.api_response import ApiResponse
from openapi_server.models.file_response import FileResponse
import boto3
import os

router = APIRouter()

def check_s3():
  session = boto3.session.Session()
  s3 = session.client(
      service_name='s3',
      endpoint_url='https://obs.ru-moscow-1.hc.sbercloud.ru/',
      aws_access_key_id=os.environ.get('AWS_S3_ACCESS_KEY_ID'),
      aws_secret_access_key=os.environ.get('AWS_S3_SECRET_ACCESS_KEY'),
      use_ssl=False,
      verify=False
  )
  s3_response = s3.list_objects(Bucket='hackathon-ecs-50')['Contents']
  items = []
  for i in s3_response:
    items.append(i['Key'])
  return ' '.join(items)

@router.get(
    "/s3/files",
    responses={
        200: {"model": FileResponse, "description": "successful operation"},
        404: {"description": "Not found"},
    },
    tags=["s3"],
    summary="Returns recognition status &amp; results",
)
async def get_files(
) -> FileResponse:
    d = {}
    d['code'] = '200'
    d['message'] = check_s3()
    return d

