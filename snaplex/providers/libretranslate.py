"""LibreTranslate provider adapter."""

from __future__ import annotations

from collections.abc import Mapping

from snaplex.credentials import CredentialService, CredentialSource
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
    provider_credential_reference,
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
from snaplex.providers.json_payload import decode_json_object, encode_json_object


class LibreTranslateProvider:
    """Translation provider for self-hosted or compatible LibreTranslate APIs."""

    def __init__(
        self,
        *,
        config: ProviderRuntimeConfig | None = None,
        transport: HttpTransport | None = None,
        environ: Mapping[str, str] | None = None,
        credential_service: CredentialService | None = None,
        name: str = "libretranslate",
    ) -> None:
        self.name = name
        self._config = config or default_provider_runtime_configs()["libretranslate"]
        self._transport = transport or UrllibHttpTransport()
        self._environ = environ
        self._credential_service = credential_service

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
        credential_reference = provider_credential_reference(self.name, self._config)
        if credential_reference.source != CredentialSource.NONE:
            payload["api_key"] = resolve_api_key(
                self.name,
                self._config,
                environ=self._environ,
                credential_service=self._credential_service,
            )

        http_request = HttpRequest(
            method="POST",
            url=f"{base_url}/translate",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body=encode_json_object(payload),
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

        payload = decode_json_object(response.body, provider_name=self.name)
        translated_text = payload.get("translatedText")
        if not isinstance(translated_text, str):
            raise StaleTranslationResultError(provider_name=self.name)

        return TranslationResponse(
            translated_text=translated_text,
            provider_name=self.name,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )
