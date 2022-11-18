import pytest

from playmobile.entities import SMS
from playmobile.test_utils import generate_phone, generate_string


class TestSMS:

    def test_with_valid_data(self) -> None:
        SMS(
            id=generate_string(),
            sender=generate_string(),
            recipient=generate_phone(),
            text=generate_string(),
        )

    def test_with_invalid_recipient(self) -> None:
        with pytest.raises(ValueError) as exc_info:  # noqa: PT011
            SMS(
                id=generate_string(),
                sender=generate_string(),
                recipient="invalid_phone",
                text=generate_string(),
            )

        assert exc_info.value.args[0] == (
            "'recipient' must match regex " +
            "'(^998[0-9]{9}$)' ('invalid_phone' doesn't)"
        )
