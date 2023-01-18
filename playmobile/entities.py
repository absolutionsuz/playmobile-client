from datetime import datetime
from enum import IntEnum, unique

import attrs


@attrs.frozen
class Credentials:
    """Учетные данные к Playmobile."""

    username: str
    password: str


@attrs.frozen
class SMS:
    """Основные данные SMS."""

    id: str                       # Уникальный идентификтор сообщения
    sender: str                   # Номер отправителя
    recipient: str = attrs.field(  # Номер получателя в формате 998[0-9]{9}
        validator=attrs.validators.matches_re("(^998[0-9]{9}$)"),
    )
    text: str                     # Текст сообщения


def _start_date_validator(instance: "Timing", _, start_date: datetime) -> None:
    if datetime.now() > start_date:
        raise ValueError("'start_at' can not be in past")
    if start_date > instance.end_at:
        raise ValueError("'start_at' can not be bigger than 'end_at'")


@attrs.frozen
class Timing:
    """Настройка времени рассылки сообщений."""

    start_at: datetime = attrs.field(  # Дата и время начала рассылки
        validator=_start_date_validator,
    )
    end_at: datetime                  # Дата и время окончания рассылки
    evenly: bool = False              # Равномерное раcпределение рассылки


@unique
class ErrorCode(IntEnum):
    """Коды ошибок Playmobile."""

    INTERNAL_SERVER_ERROR = 100      # Внутренняя ошибка сервера
    SYNTAX_ERROR = 101               # Синтаксическая ошибка
    ACCOUNT_LOCK = 102               # Аккаунт клиента заблокирован
    EMPTY_CHANNEL = 103              # Не задан канал для отправки сообщений
    INVALID_PRIORITY = 104           # Некорректное значение priority
    TO_MUCH_IDS = 105                # Cлишком много идентификаторов сообщений

    EMPTY_RECIPIENT = 202            # Адрес получателя не задан
    EMPTY_EMAIL_ADDRESS = 204        # Адрес почты получателя не задан
    EMPTY_MESSAGE_ID = 205           # Идентификатор сообщения не задан
    INVALID_VARIABLES = 206          # Некорректное значение variables

    INVALID_LOCALTIME = 301          # Некорректное значение localtime
    INVALID_START_DATETIME = 302     # Некорректное значение start-datetime
    INVALID_END_DATETIME = 303       # Некорректное значение end-datetime
    INVALID_ALLOWED_STARTTIME = 304  # Некорректное значение allowed-starttime
    INVALID_ALLOWED_ENDTIME = 305    # Некорректное значение allowed-endtime
    INVALID_SEND_EVENLY = 306        # Некорректное значение send-evenly

    EMPTY_ORIGINATOR = 401           # Адрес отправителя не указан
    EMPTY_APPLICATION = 402          # Приложение не указано
    EMPTY_TTL = 403                  # Значение ttl не указано
    EMPTY_CONTENT = 404              # Содержимое сообщения не указано
    CONTENT_ERROR = 405              # Некорректный формат содержимого контента
    INVALID_CONTENT = 406            # Некорректное значение content
    INVALID_TTL = 407                # Некорректно значение TTL  # noqa: WPS115
    INVALID_ATTACHED_FILES = 408     # Файлы имеют слишком большой объем
    INVALID_RETRY_ATTEMPTS = 410     # Некорректное значение retry-attempts
    INVALID_RETRY_TIMEOUT = 411      # Некорректное значение retry-timeout


@attrs.frozen
class Error:
    """Тело ответа Playmobile при ошибке."""

    code: ErrorCode
    description: str
