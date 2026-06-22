"""JSON helpers shared by HTTP-backed providers."""

from __future__ import annotations

import json
from collections.abc import Mapping

from snaplex.errors import StaleTranslationResultError


def encode_json_object(payload: Mapping[str, object]) -> bytes:
    return json.dumps(payload).encode("utf-8")


def decode_json_object(body: bytes, *, provider_name: str) -> dict[str, object]:
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StaleTranslationResultError(provider_name=provider_name) from exc

    if not isinstance(payload, dict):
        raise StaleTranslationResultError(provider_name=provider_name)
    return payload
