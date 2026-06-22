"""OpenAI Responses API translation provider adapter."""

from __future__ import annotations

from collections.abc import Mapping

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


class OpenAITranslationProvider:
    """Translation provider backed by the OpenAI Responses API."""

    def __init__(
        self,
        *,
        config: ProviderRuntimeConfig | None = None,
        transport: HttpTransport | None = None,
        environ: Mapping[str, str] | None = None,
        name: str = "openai",
    ) -> None:
        self.name = name
        self._config = config or default_provider_runtime_configs()["openai"]
        self._transport = transport or UrllibHttpTransport()
        self._environ = environ

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        response = self._send_translate_request(request)
        return self._parse_response(request, response)

    def _send_translate_request(self, request: TranslationRequest) -> HttpResponse:
        base_url = self._config.base_url_without_trailing_slash()
        if not base_url:
            raise TranslationProviderError(
                "OpenAI base URL is not configured.",
                provider_name=self.name,
            )

        api_key = resolve_api_key(self.name, self._config, environ=self._environ)
        payload: dict[str, object] = {
            "model": self._config.options.get("model", "gpt-5.5"),
            "instructions": _translation_instructions(request),
            "input": request.text,
            "store": False,
        }
        http_request = HttpRequest(
            method="POST",
            url=f"{base_url}/responses",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}",
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
                f"OpenAI returned HTTP {response.status_code}.",
                provider_name=self.name,
            )

        translated_text = _extract_response_text(payload)
        if not translated_text:
            raise StaleTranslationResultError(provider_name=self.name)

        return TranslationResponse(
            translated_text=translated_text,
            provider_name=self.name,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )


def _translation_instructions(request: TranslationRequest) -> str:
    return (
        "Translate the user-provided text "
        f"from {request.source_lang} to {request.target_lang}. "
        "Return only the translated text."
    )


def _decode_response_body(response: HttpResponse, *, provider_name: str) -> dict[str, object]:
    if not response.body:
        return {}
    return decode_json_object(response.body, provider_name=provider_name)


def _extract_response_text(payload: Mapping[str, object]) -> str:
    output_text = payload.get("output_text")
    if isinstance(output_text, str):
        return output_text.strip()

    output = payload.get("output")
    if not isinstance(output, list):
        return ""

    text_parts: list[str] = []
    for output_item in output:
        if not isinstance(output_item, dict):
            continue
        content = output_item.get("content")
        if not isinstance(content, list):
            continue
        for content_item in content:
            if not isinstance(content_item, dict):
                continue
            text = content_item.get("text")
            if isinstance(text, str) and content_item.get("type") == "output_text":
                text_parts.append(text)
    return "".join(text_parts).strip()


def _payload_mentions_language(payload: Mapping[str, object]) -> bool:
    error = payload.get("error")
    message = ""
    if isinstance(error, dict):
        raw_message = error.get("message")
        message = raw_message if isinstance(raw_message, str) else ""
    elif isinstance(error, str):
        message = error
    lowered = message.lower()
    return "language" in lowered or "unsupported" in lowered
