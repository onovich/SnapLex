"""LibreTranslate provider adapter."""

from __future__ import annotations

from collections.abc import Mapping
import json

from snaplex.errors import (
    StaleTranslationResultError,
    TranslationProviderError,
    TranslationProviderTimeoutError,
    UnsupportedLanguageError,
)
from snaplex.providers.base import TranslationRequest, TranslationResponse
from snaplex.providers.config import (
    ProviderRuntimeConfig,
    default_provider_runtime_configs,
    resolve_api_key,
)
from snaplex.providers.http import (
    HttpRequest,
    HttpResponse,
    HttpTransport,
    HttpTransportError,
    HttpTransportTimeout,
    UrllibHttpTransport,
)


class LibreTranslateProvider:
    """Translation provider for self-hosted or compatible LibreTranslate APIs."""

    def __init__(
        self,
        *,
        config: ProviderRuntimeConfig | None = None,
        transport: HttpTransport | None = None,
        environ: Mapping[str, str] | None = None,
        name: str = "libretranslate",
    ) -> None:
        self.name = name
        self._config = config or default_provider_runtime_configs()["libretranslate"]
        self._transport = transport or UrllibHttpTransport()
        self._environ = environ

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        response = self._send_translate_request(request)
        return self._parse_response(request, response)

    def _send_translate_request(self, request: TranslationRequest) -> HttpResponse:
        base_url = self._config.base_url_without_trailing_slash()
        if not base_url:
            raise TranslationProviderError(
                "LibreTranslate base URL is not configured.",
                provider_name=self.name,
            )

        payload: dict[str, str] = {
            "q": request.text,
            "source": request.source_lang,
            "target": request.target_lang,
            "format": "text",
        }
        if self._config.api_key_env_var.strip():
            payload["api_key"] = resolve_api_key(
                self.name,
                self._config,
                environ=self._environ,
            )

        http_request = HttpRequest(
            method="POST",
            url=f"{base_url}/translate",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body=json.dumps(payload).encode("utf-8"),
            timeout_seconds=self._config.timeout_seconds,
        )
        try:
            return self._transport.send(http_request)
        except HttpTransportTimeout as exc:
            raise TranslationProviderTimeoutError(provider_name=self.name) from exc
        except HttpTransportError as exc:
            raise TranslationProviderError(str(exc), provider_name=self.name) from exc

    def _parse_response(
        self,
        request: TranslationRequest,
        response: HttpResponse,
    ) -> TranslationResponse:
        if response.status_code == 400:
            raise UnsupportedLanguageError(
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                provider_name=self.name,
            )
        if response.status_code >= 400:
            raise TranslationProviderError(
                f"LibreTranslate returned HTTP {response.status_code}.",
                provider_name=self.name,
            )

        payload = _decode_json_object(response.body, provider_name=self.name)
        translated_text = payload.get("translatedText")
        if not isinstance(translated_text, str):
            raise StaleTranslationResultError(provider_name=self.name)

        return TranslationResponse(
            translated_text=translated_text,
            provider_name=self.name,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )


def _decode_json_object(body: bytes, *, provider_name: str) -> dict[str, object]:
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StaleTranslationResultError(provider_name=provider_name) from exc

    if not isinstance(payload, dict):
        raise StaleTranslationResultError(provider_name=provider_name)
    return payload
