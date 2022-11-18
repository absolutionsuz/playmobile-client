# Python client for Playmobile.uz API (aka smsxabar.uz)

This is Python HTTP Client for [Playmobile.uz](https://playmobile.uz) (aka [smsxabar.uz](https://smsxabar.uz))
based on [httpx](https://github.com/encode/httpx).

Playmobile is a SMS broker which allows you to send messages throughout Uzbekistan.

## Installation

To install playmobile-client, simply:

``` bash
$ pip install playmobile-client
```
This package can be found on [PyPI](https://pypi.org).

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
client.send_sms(sms)
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


