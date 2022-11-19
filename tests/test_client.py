import json
from base64 import b64encode
from http import HTTPStatus

import httpx
import pytest
from pytest_httpx import HTTPXMock

from playmobile.client import HttpClient, _ErrorSchema  # noqa: WPS450
from playmobile.entities import Credentials
from playmobile.exceptions import RequestError, ResponsePayloadSchemaError
from playmobile.test_utils import (
    generate_error,
    generate_sms,
    generate_string,
    get_error_code,
)


def assert_request(
    request: httpx.Request,
    *,
    url: httpx.URL,
    account: Credentials,
    data: dict,
) -> None:
    assert request.url == url
    assert json.loads(request.content) == data

    token = b64encode(
        ":".join((account.username, account.password)).encode(),
    ).decode("ascii")
    assert request.headers["Authorization"] == "Basic {0}".format(token)


class TestErrorSchema:

    def test_with_valid_data(self) -> None:
        expected_error = generate_error()
        data = {
            "error-code": expected_error.code,
            "error-description": expected_error.description,
        }
        error = _ErrorSchema().load(data)

        assert error == expected_error

    def test_with_invalid_keys(self) -> None:
        data = {
            "error_code": get_error_code().value,
            "description": generate_string(),
        }

        with pytest.raises(ResponsePayloadSchemaError) as exc_info:
            _ErrorSchema().load(data)

        assert str(exc_info.value) == "Invalid Playmobile response payload"
        assert exc_info.value.description == {
            "error-code": ["Missing data for required field."],
            "error_code": ["Unknown field."],
            "error-description": ["Missing data for required field."],
            "description": ["Unknown field."],
        }

    def test_with_invalid_error_code(self) -> None:
        data = {
            "error-code": 600,
            "error-description": generate_string(),
        }

        with pytest.raises(ResponsePayloadSchemaError) as exc_info:
            _ErrorSchema().load(data)

        assert str(exc_info.value) == "Invalid Playmobile response payload"
        assert exc_info.value.description == {
            "error-code": ["Unknown value."],
        }


class TestHTTPClient:

    def test_send_sms_success(
        self,
        client: HttpClient,
        base_url: httpx.URL,
        account: Credentials,
        httpx_mock: HTTPXMock,
    ) -> None:
        sms = generate_sms()
        expected_data = {
            "messages": [
                {
                    "message-id": sms.id,
                    "recipient": sms.recipient,
                    "sms": {
                        "originator": sms.sender,
                        "content": {
                            "text": sms.text,
                        },
                    },
                },
            ],
        }
        httpx_mock.add_response(text="Request is received")

        client.send_sms(sms)
        request = httpx_mock.get_request()
        assert request is not None

        url = base_url.copy_with(path="/broker-api/send")
        assert_request(request, url=url, account=account, data=expected_data)

    def test_send_sms_bad_request(
        self,
        client: HttpClient,
        httpx_mock: HTTPXMock,
    ) -> None:
        sms = generate_sms()
        expected_status = HTTPStatus.BAD_REQUEST
        expected_error = generate_error()

        httpx_mock.add_response(
            status_code=expected_status,
            json={
                "error-code": expected_error.code,
                "error-description": expected_error.description,
            },
        )

        with pytest.raises(RequestError) as exc_info:
            client.send_sms(sms)

        assert exc_info.value.http_status == expected_status
        assert exc_info.value.error == expected_error
        assert str(exc_info.value) == (
            "Playmobile responded with status 400.\n" +
            "Error code: {0}. Error description: {1}."
        ).format(expected_error.code, expected_error.description)

    def test_send_sms_not_found(
        self,
        client: HttpClient,
        httpx_mock: HTTPXMock,
    ) -> None:
        sms = generate_sms()
        expected_status = HTTPStatus.GATEWAY_TIMEOUT

        httpx_mock.add_response(
            status_code=expected_status,
        )

        with pytest.raises(RequestError) as exc_info:
            client.send_sms(sms)

        assert exc_info.value.http_status == expected_status
        assert exc_info.value.error is None
        assert str(exc_info.value) == "Playmobile responded with status 504."
