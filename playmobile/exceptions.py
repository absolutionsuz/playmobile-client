from typing import Optional

from playmobile.entities import Error


class PlaymobileBaseError(Exception):
    """Base Exception class."""


class RequestError(PlaymobileBaseError):
    """Exception for failed request."""

    def __init__(
        self,
        http_status: int,
        error: Optional[Error] = None,
    ) -> None:
        message = "Playmobile responded with status {0}.".format(http_status)
        if error:
            error_message = "Error code: {0}. Error description: {1}.".format(
                error.code,
                error.description,
            )
            message = "\n".join((message, error_message))
        super().__init__(message)
        self.http_status = http_status
        self.error = error


class ResponsePayloadSchemaError(PlaymobileBaseError):
    """Exception for unexpected schema in response."""

    def __init__(self, description: dict) -> None:
        super().__init__("Invalid Playmobile response payload")
        self.description = description
