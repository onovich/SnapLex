from __future__ import annotations

from io import BytesIO
import urllib.error

import pytest

from snaplex.providers.http import (
    HttpRequest,
    HttpTransportError,
    HttpTransportTimeout,
    UrllibHttpTransport,
)


class FakeResponse:
    def __init__(
        self,
        *,
        status: int,
        body: bytes,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.status = status
        self._body = body
        self.headers = headers or {}

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return self._body


class FakeOpener:
    def __init__(self, response: object) -> None:
        self.response = response
        self.requests: list[object] = []
        self.timeouts: list[float] = []

    def open(self, request: object, *, timeout: float) -> object:
        self.requests.append(request)
        self.timeouts.append(timeout)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


def test_urllib_transport_sends_request_through_injected_opener() -> None:
    opener = FakeOpener(FakeResponse(status=200, body=b'{"ok": true}'))
    transport = UrllibHttpTransport(opener=opener)

    response = transport.send(
        HttpRequest(
            method="post",
            url="https://example.test/translate",
            headers={"Content-Type": "application/json"},
            body=b"{}",
            timeout_seconds=3.5,
        ),
    )

    sent_request = opener.requests[0]
    assert response.status_code == 200
    assert response.body == b'{"ok": true}'
    assert sent_request.get_method() == "POST"
    assert sent_request.data == b"{}"
    assert opener.timeouts == [3.5]


def test_urllib_transport_returns_http_errors_as_responses() -> None:
    http_error = urllib.error.HTTPError(
        "https://example.test/translate",
        503,
        "unavailable",
        {"Retry-After": "1"},
        BytesIO(b"service unavailable"),
    )
    transport = UrllibHttpTransport(opener=FakeOpener(http_error))

    response = transport.send(HttpRequest(method="POST", url="https://example.test/translate"))

    assert response.status_code == 503
    assert response.body == b"service unavailable"
    assert response.headers["Retry-After"] == "1"


def test_urllib_transport_maps_timeout_errors() -> None:
    timeout_error = urllib.error.URLError(TimeoutError("timed out"))
    transport = UrllibHttpTransport(opener=FakeOpener(timeout_error))

    with pytest.raises(HttpTransportTimeout):
        transport.send(HttpRequest(method="POST", url="https://example.test/translate"))


def test_urllib_transport_maps_network_errors() -> None:
    network_error = urllib.error.URLError("connection refused")
    transport = UrllibHttpTransport(opener=FakeOpener(network_error))

    with pytest.raises(HttpTransportError):
        transport.send(HttpRequest(method="POST", url="https://example.test/translate"))
