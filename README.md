# Python client for Playmobile.uz API (aka smsxabar.uz)

This is Python HTTP Client for [Playmobile.uz](https://playmobile.uz) (aka [smsxabar.uz](https://smsxabar.uz))
based on [httpx](https://github.com/encode/httpx).

Playmobile is a SMS broker which allows you to send messages throughout Uzbekistan.

## Installation

To install playmobile-client, simply:

``` bash
$ pip install playmobile-client
```
This package can be found on [PyPI](https://pypi.org/project/playmobile-client/).

## Usage

```python
import httpx
import playmobile

client = playmobile.HttpClient(
    account=playmobile.Credentials(
        username="example",
        password="example",
    ),
    base_url=httpx.URL("https://playmobile-example.uz"),
    session=httpx.Client(),
)

sms = playmobile.SMS(
    id="unique_string",
    sender="0001",
    recipient="998xx3332211",
    text="Hello world!",
)

# Single SMS
client.send_sms(sms)

# SMS batch
sms_batch = [
    playmobile.SMS(
        id="unique_string_1",
        sender="0001",
        recipient="998xx3332211",
        text="Hello world!",
    ),
    playmobile.SMS(
        id="unique_string_2",
        sender="0001",
        recipient="998xx3332211",
        text="Yankee!",
    ),
]
client.send_sms_batch(sms_batch)  
```

You can set up Timing settings:

```python
import playmobile

sms = playmobile.SMS(...)

timing = playmobile.Timing(
    start_at=datetime(2023, 1, 1, 12, 0),
    end_at=datetime(2023, 1, 1, 14, 0),
)

# Single SMS
client.send_sms(sms, timing=timing)
```

Advanced users can set up HTTPX session with custom parameters. For example:

```python
client = playmobile.Client(
    ...,
    session = httpx.Client(
        timeout=httpx.Timeout(timeout=2.0),
    ),
)
```

Package also have the test utils which will help you test your service:
- playmobile.generate_sms
- playmobile.generate_error
