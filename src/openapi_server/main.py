# coding: utf-8

"""
    Swagger SberZvuk

    SberZvuk API

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from fastapi import FastAPI

from openapi_server.apis.default_api import router as DefaultApiRouter
from openapi_server.apis.s3_api import router as S3ApiRouter
# from worker import create_task

app = FastAPI(
    title="Swagger SberZvuk",
    description="SberZvuk API",
    version="1.0.0",
)

app.include_router(DefaultApiRouter)
app.include_router(S3ApiRouter)
