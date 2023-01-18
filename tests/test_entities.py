import pytest

from playmobile.entities import SMS, Timing
from playmobile.test_utils import FAKER, generate_phone, generate_string


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


class TestTiming:

    def test_with_valid_data(self) -> None:
        end_at = FAKER.future_datetime()
        Timing(
            start_at=FAKER.future_datetime(end_date=end_at),
            end_at=end_at,
        )

    def test_with_invalid_start_date(self) -> None:
        with pytest.raises(ValueError) as exc_info:  # noqa: PT011
            Timing(
                start_at=FAKER.past_datetime(),
                end_at=FAKER.future_datetime(),
            )

        assert exc_info.value.args[0] == "'start_at' can not be in past"

    def test_with_invalid_end_date(self) -> None:
        with pytest.raises(ValueError) as exc_info:  # noqa: PT011
            Timing(
                start_at=FAKER.future_datetime(),
                end_at=FAKER.past_datetime(),
            )

        assert exc_info.value.args[0] == (
            "'start_at' can not be bigger than 'end_at'"
        )
