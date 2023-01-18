from http import HTTPStatus
from typing import Any, Iterable, Optional, final

import attrs
import httpx
from marshmallow import Schema, ValidationError, fields, post_load

from playmobile.abstract import ClientInterface
from playmobile.entities import SMS, Credentials, Error, ErrorCode, Timing
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

    def send_sms(self, sms: SMS, *, timing: Optional[Timing] = None) -> None:
        """Send single SMS to Playmobile."""
        self.send_sms_batch((sms,), timing=timing)

    def send_sms_batch(
        self,
        sms_batch: Iterable[SMS],
        *,
        timing: Optional[Timing] = None,
    ) -> None:
        """Send batch of SMS to Playmobile."""
        payload: dict = {
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
                } for sms in sms_batch
            ],
        }
        if timing is not None:
            payload = {
                **payload,
                "timing": {
                    "start-datetime": timing.start_at.strftime(
                        "%Y-%m-%d %H:%M",
                    ),
                    "end-datetime": timing.end_at.strftime("%Y-%m-%d %H:%M"),
                    "send-evenly": int(timing.evenly),
                },
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
