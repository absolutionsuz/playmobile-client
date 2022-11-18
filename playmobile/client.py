from http import HTTPStatus
from typing import Any, final

import attrs
import httpx
from marshmallow import Schema, ValidationError, fields, post_load

from playmobile.abstract import ClientInterface
from playmobile.entities import SMS, Credentials, Error, ErrorCode
from playmobile.exceptions import RequestError, ResponsePayloadSchemaError


class _ErrorSchema(Schema):

    code = fields.Enum(
        ErrorCode,
        by_value=True,
        required=True,
        data_key="error-code",
        error_messages={"unknown": "Unknown value."},
    )
    description = fields.String(required=True, data_key="error-description")

    def handle_error(  # type: ignore
        self,
        error: ValidationError,
        payload: Any,
        *,
        many: bool,
        **kwargs,
    ) -> None:
        raise ResponsePayloadSchemaError(error.messages)  # type: ignore

    @post_load
    def release(self, payload_data: dict, **kwargs) -> Error:
        return Error(**payload_data)


@final
@attrs.frozen
class HttpClient(ClientInterface):
    """Sync implementation of Playmobile client."""

    _account: Credentials   # Credentials
    _base_url: httpx.URL     # Base URL
    _session: httpx.Client  # HTTP Session

    def send_sms(self, sms: SMS) -> None:
        """Send SMS to Playmobile."""
        payload = {
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
        self._fetch("/broker-api/send", payload)

    def _fetch(self, path: str, json: dict) -> None:
        url = self._base_url.copy_with(path=path)
        auth = httpx.BasicAuth(self._account.username, self._account.password)
        response = self._session.post(url, json=json, auth=auth)

        status = response.status_code

        if status < HTTPStatus.BAD_REQUEST:
            return

        if status == HTTPStatus.BAD_REQUEST:
            error = _ErrorSchema().load(response.json())
        else:
            error = None

        raise RequestError(status, error)
