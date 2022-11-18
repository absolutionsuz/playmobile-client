import random
import secrets
import string

import factory

from playmobile.entities import SMS, Error, ErrorCode


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


class SMSFactory(factory.Factory):
    """SMS Factory."""

    class Meta:
        model = SMS

    id = factory.LazyFunction(generate_string)
    sender = factory.LazyFunction(generate_string)
    recipient = factory.LazyFunction(generate_phone)
    text = factory.LazyFunction(generate_string)


class ErrorFactory(factory.Factory):
    """Error Factory."""

    class Meta:
        model = Error

    code = factory.LazyFunction(get_error_code)
    description = factory.LazyFunction(generate_string)
