"""Small HTTP transport boundary for translation providers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol
import urllib.error
import urllib.request


@dataclass(frozen=True)
class HttpRequest:
    method: str
    url: str
    headers: Mapping[str, str] = field(default_factory=dict)
    body: bytes | None = None
    timeout_seconds: float = 10.0


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    body: bytes
    headers: Mapping[str, str] = field(default_factory=dict)


class HttpTransportError(RuntimeError):
    """Raised when the HTTP boundary cannot return a provider response."""


class HttpTransportTimeout(HttpTransportError):
    """Raised when the HTTP boundary times out."""


class HttpTransport(Protocol):
    def send(self, request: HttpRequest) -> HttpResponse:
        """Send a request and return an HTTP response."""
        ...


class UrllibHttpTransport:
    """Standard-library HTTP transport used by real provider adapters."""

    def __init__(self, opener: Any | None = None) -> None:
        self._opener = opener or urllib.request.build_opener()

    def send(self, request: HttpRequest) -> HttpResponse:
        urllib_request = urllib.request.Request(
            request.url,
            data=request.body,
            headers=dict(request.headers),
            method=request.method.upper(),
        )
        try:
            with self._opener.open(urllib_request, timeout=request.timeout_seconds) as response:
                return HttpResponse(
                    status_code=response.status,
                    body=response.read(),
                    headers=_headers_to_dict(response.headers),
                )
        except urllib.error.HTTPError as exc:
            return HttpResponse(
                status_code=exc.code,
                body=exc.read(),
                headers=_headers_to_dict(exc.headers),
            )
        except TimeoutError as exc:
            raise HttpTransportTimeout(str(exc)) from exc
        except urllib.error.URLError as exc:
            if isinstance(exc.reason, TimeoutError):
                raise HttpTransportTimeout(str(exc.reason)) from exc
            raise HttpTransportError(str(exc.reason)) from exc


def _headers_to_dict(headers: Any) -> dict[str, str]:
    if headers is None:
        return {}
    return {str(key): str(value) for key, value in headers.items()}
