import random
import secrets
import string

from faker import Faker

from playmobile.entities import SMS, Error, ErrorCode, Timing

FAKER = Faker()


def generate_string() -> str:
    """Generate random string."""
    size = random.randint(3, 30)
    return secrets.token_hex(size)


def generate_phone() -> str:
    """Generate random mobile phone in UZ format."""
    numbers = "".join(
        random.choice(string.digits) for _ in range(9)
    )
    return "".join(("998", numbers))


def get_error_code() -> ErrorCode:
    """Choose random ErrorCode."""
    return random.choice(tuple(ErrorCode))


def generate_sms() -> SMS:
    """Generate random SMS entity."""
    return SMS(
        id=generate_string(),
        sender=generate_string(),
        recipient=generate_phone(),
        text=generate_string(),
    )


def generate_timing() -> Timing:
    """Generate random SMS entity."""
    end_at = FAKER.future_datetime()
    return Timing(
        start_at=FAKER.future_datetime(end_date=end_at),
        end_at=end_at,
    )


def generate_error() -> Error:
    """Generate random Error entity."""
    return Error(
        code=get_error_code(),
        description=generate_string(),
    )
