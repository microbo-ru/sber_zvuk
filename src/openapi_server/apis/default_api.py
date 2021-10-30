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
from openapi_server.models.recognize_request import RecognizeRequest
from openapi_server.models.recognize_response import RecognizeResponse
import boto3
import os

from openapi_server.worker.worker import create_task

# import urllib
import urllib.request
from urllib.parse import urlparse

router = APIRouter()


@router.get(
    "/recognize/status/{prefix}",
    responses={
        200: {"model": RecognizeResponse, "description": "successful operation"},
        404: {"description": "Not found"},
    },
    tags=["default"],
    summary="Returns recognition status &amp; results",
)
async def get_recognize_status(
        prefix: str = Path(None, description="Course ID"),
) -> RecognizeResponse:
    task = create_task.delay(1)
    result = {'code': '200', 'message': task.id}
    return result


def process_file(url, prefix):
    a = urlparse(url)
    file_name = os.path.basename(a.path)
    urllib.request.urlretrieve(url, f'/root/app/store/{prefix}_{file_name}')


@router.post(
    "/recognize",
    responses={
        200: {"model": ApiResponse, "description": "successful operation"},
        405: {"description": "Invalid input"},
    },
    tags=["default"],
    summary="Send a recognize request",
)
async def start_recognize(
        body: RecognizeRequest = Body(None, description="Pet object that needs to be added to the store"),
) -> ApiResponse:
    process_file(body.source, body.prefix)

    result = {'code': 200, 'message': 'sheduled'}
    return result
    # ...
