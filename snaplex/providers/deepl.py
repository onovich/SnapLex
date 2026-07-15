"""DeepL provider adapter."""

from __future__ import annotations

from collections.abc import Mapping

from snaplex.credentials import CredentialService
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
from snaplex.providers.json_payload import decode_json_object, encode_json_object


class DeepLTranslationProvider:
    """Translation provider backed by the DeepL text translation API."""

    def __init__(
        self,
        *,
        config: ProviderRuntimeConfig | None = None,
        transport: HttpTransport | None = None,
        environ: Mapping[str, str] | None = None,
        credential_service: CredentialService | None = None,
        name: str = "deepl",
    ) -> None:
        self.name = name
        self._config = config or default_provider_runtime_configs()["deepl"]
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
                "DeepL base URL is not configured.",
                provider_name=self.name,
            )

        api_key = resolve_api_key(
            self.name,
            self._config,
            environ=self._environ,
            credential_service=self._credential_service,
        )
        payload = _build_payload(request, self._config.options)
        http_request = HttpRequest(
            method="POST",
            url=f"{base_url}/translate",
            headers={
                "Accept": "application/json",
                "Authorization": f"DeepL-Auth-Key {api_key}",
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
        payload = _decode_response_body(response, provider_name=self.name)
        if response.status_code == 400 and _payload_mentions_language(payload):
            raise UnsupportedLanguageError(
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                provider_name=self.name,
            )
        if response.status_code >= 400:
            raise TranslationProviderError(
                f"DeepL returned HTTP {response.status_code}.",
                provider_name=self.name,
            )

        translated_text, source_lang = _extract_translation(payload, request)
        if not translated_text:
            raise StaleTranslationResultError(provider_name=self.name)

        return TranslationResponse(
            translated_text=translated_text,
            provider_name=self.name,
            source_lang=source_lang,
            target_lang=request.target_lang,
        )


def _build_payload(
    request: TranslationRequest,
    options: Mapping[str, str],
) -> dict[str, object]:
    payload: dict[str, object] = {
        "text": [request.text],
        "target_lang": _deepl_lang(request.target_lang),
    }
    if request.source_lang != "auto":
        payload["source_lang"] = _deepl_lang(request.source_lang)
    model_type = options.get("model_type", "").strip()
    if model_type:
        payload["model_type"] = model_type
    return payload


def _deepl_lang(language: str) -> str:
    return language.replace("_", "-").upper()


def _decode_response_body(response: HttpResponse, *, provider_name: str) -> dict[str, object]:
    if not response.body:
        return {}
    return decode_json_object(response.body, provider_name=provider_name)


def _extract_translation(
    payload: Mapping[str, object],
    request: TranslationRequest,
) -> tuple[str, str]:
    translations = payload.get("translations")
    if not isinstance(translations, list) or not translations:
        return "", request.source_lang

    first_translation = translations[0]
    if not isinstance(first_translation, dict):
        return "", request.source_lang

    text = first_translation.get("text")
    if not isinstance(text, str):
        return "", request.source_lang

    detected_source = first_translation.get("detected_source_language")
    source_lang = request.source_lang
    if request.source_lang == "auto" and isinstance(detected_source, str):
        source_lang = detected_source.lower()
    return text.strip(), source_lang


def _payload_mentions_language(payload: Mapping[str, object]) -> bool:
    message = ""
    raw_message = payload.get("message")
    if isinstance(raw_message, str):
        message = raw_message
    error = payload.get("error")
    if isinstance(error, dict):
        raw_error_message = error.get("message")
        if isinstance(raw_error_message, str):
            message = f"{message} {raw_error_message}"
    lowered = message.lower()
    return "language" in lowered or "source_lang" in lowered or "target_lang" in lowered
