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

from openapi_server.worker.worker import process_file
from celery.result import AsyncResult

from openapi_server.worker.worker import celery

# import urllib.request
# from urllib.parse import urlparse

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
        prefix: str = Path(None, description="Task Id"),
) -> RecognizeResponse:
    # task = create_task.delay(1)
    # result = {'code': '200', 'message': task.id}
    # return result
    # ...
    res = AsyncResult(prefix, app=celery)
    result = {'code': '200', 'message': res.state}
    return result


def submit_task(url, prefix):
    task = process_file.delay(url, prefix)
    return task.id


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
    task_id = submit_task(body.source, body.prefix)

    result = {'code': 200, 'message': task_id}
    return result
