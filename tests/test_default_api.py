# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.api_response import ApiResponse  # noqa: F401
from openapi_server.models.recognize_request import RecognizeRequest  # noqa: F401
from openapi_server.models.recognize_response import RecognizeResponse  # noqa: F401


def test_get_recognize_status(client: TestClient):
    """Test case for get_recognize_status

    Returns recognition status & results
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/recognize/status/{prefix}".format(prefix='prefix_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_start_recognize(client: TestClient):
    """Test case for start_recognize

    Send a recognize request
    """
    body = {"prefix":"prefix","source":"https://openapi-generator.tech"}

    headers = {
    }
    response = client.request(
        "POST",
        "/recognize",
        headers=headers,
        json=body,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

