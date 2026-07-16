"""Deterministic release smoke checks for packaged SnapLex builds."""

from __future__ import annotations

import asyncio
import os
import uuid
from pathlib import Path
from typing import Any

from snaplex.credentials import (
    CredentialReference,
    CredentialMissingError,
    CredentialService,
    CredentialSource,
    CredentialStatusCode,
    CredentialStoreError,
    CredentialUnavailableError,
    CredentialUnsupportedError,
    KeyringCredentialStore,
    keyring_credential_reference,
)
from snaplex.services import (
    FakeCaptureService,
    FakeOcrService,
    HistoryService,
    InMemoryClipboardService,
    ScreenRegion,
    ScreenTranslationService,
    SettingsService,
    create_default_translation_pipeline,
)
from snaplex.storage import (
    APP_DATA_DIR_ENV_VAR,
    CONFIG_FILE_NAME,
    HISTORY_FILE_NAME,
    JsonFileConfigStore,
    JsonFileHistoryStore,
    default_app_data_dir,
)


class PackagedSmokeError(RuntimeError):
    """Raised when deterministic packaged workflow smoke fails."""


CREDENTIAL_SMOKE_MODES = ("import", "cycle", "save", "check-delete")
CREDENTIAL_SMOKE_IDENTIFIER = "snaplex/package-credential-smoke"
CREDENTIAL_SMOKE_SERVICE_NAME = "SnapLexPackageCredentialSmoke"


def run_packaged_workflow_smoke() -> tuple[str, ...]:
    """Run clipboard/settings/history smoke against packaged runtime modules."""

    if not os.environ.get(APP_DATA_DIR_ENV_VAR, "").strip():
        raise PackagedSmokeError(f"{APP_DATA_DIR_ENV_VAR} must point to a smoke data directory.")

    app_data_dir = default_app_data_dir()
    config_store = JsonFileConfigStore(app_data_dir / CONFIG_FILE_NAME)
    history_store = JsonFileHistoryStore(app_data_dir / HISTORY_FILE_NAME)
    settings_service = SettingsService(config_store)
    history_service = HistoryService(
        config_store=config_store,
        history_store=history_store,
        id_factory=lambda: "packaged-smoke-entry",
    )
    clipboard_service = InMemoryClipboardService("hello")

    settings_service.update_provider_selection(provider_name="fake", provider_order=("fake",))
    settings_service.update_language_defaults(source_lang="auto", target_lang="en")
    settings_service.update_history_preferences(enabled=True, max_entries=5)

    config = settings_service.load()
    if config.provider_name != "fake" or config.provider_order != ("fake",):
        raise PackagedSmokeError("fake provider settings were not persisted.")
    if not config.history_enabled or config.history_max_entries != 5:
        raise PackagedSmokeError("history settings were not persisted.")

    pipeline = create_default_translation_pipeline(config_store=config_store)
    response = pipeline.translate_text(clipboard_service.get_text())
    if response.provider_name != "fake" or response.translated_text != "hello [en]":
        raise PackagedSmokeError("fake clipboard translation did not return the expected result.")
    clipboard_service.set_text(response.translated_text)
    if clipboard_service.get_text() != "hello [en]":
        raise PackagedSmokeError("clipboard copy smoke did not preserve the translated result.")

    entry = history_service.add_translation(
        source_text="hello",
        translated_text=response.translated_text,
        provider_name=response.provider_name,
        source_lang=response.source_lang,
        target_lang=response.target_lang,
        flow="clipboard",
    )
    if entry is None:
        raise PackagedSmokeError("history entry was not recorded while history was enabled.")
    if len(history_service.list_recent()) != 1:
        raise PackagedSmokeError("history list did not contain the recorded entry.")
    if not history_service.delete(entry.id):
        raise PackagedSmokeError("history delete did not remove the recorded entry.")

    screen_service = ScreenTranslationService(
        capture_service=FakeCaptureService(),
        ocr_service=FakeOcrService(text="screen hello"),
        pipeline=pipeline,
    )
    screen_response = asyncio.run(screen_service.translate_region(ScreenRegion(0, 0, 10, 10)))
    if (
        screen_response.source_text != "screen hello"
        or screen_response.translated_text != "screen hello [en]"
    ):
        raise PackagedSmokeError("screen fake capture/OCR translation smoke failed.")

    history_service.add_translation(
        source_text="again",
        translated_text="again [en]",
        provider_name="fake",
        source_lang="auto",
        target_lang="en",
        flow="clipboard",
    )
    history_service.clear()
    if history_service.list_recent():
        raise PackagedSmokeError("history clear left entries behind.")

    _assert_inside_app_data(config_store.config_path, app_data_dir, "config")
    _assert_inside_app_data(history_store.history_path, app_data_dir, "history")

    return (
        f"app data: {app_data_dir}",
        "settings persistence: fake provider, history enabled",
        "clipboard translation: hello -> hello [en]",
        "screen fake capture/OCR translation: screen hello -> screen hello [en]",
        "history record/list/delete/clear: PASS",
    )


def run_packaged_credential_smoke(
    *,
    mode: str = "cycle",
    keyring_module: Any | None = None,
) -> tuple[str, ...]:
    """Run explicit credential package smoke without printing credential values."""

    if mode not in CREDENTIAL_SMOKE_MODES:
        raise PackagedSmokeError(f"unknown credential smoke mode: {mode}")

    keyring = keyring_module or _import_keyring()
    backend_label = _keyring_backend_label(keyring)
    reference = keyring_credential_reference("openai", CREDENTIAL_SMOKE_IDENTIFIER)
    service = CredentialService(
        {
            CredentialSource.KEYRING: KeyringCredentialStore(
                service_name=CREDENTIAL_SMOKE_SERVICE_NAME,
                keyring_module=keyring,
            ),
        },
    )
    base_lines = [
        f"credential smoke mode: {mode}",
        f"keyring backend: {backend_label}",
        f"credential reference: {reference.identifier}",
    ]

    if mode == "import":
        return (*base_lines, "keyring import/backend discovery: PASS")

    if mode == "save":
        _delete_if_present(service, reference)
        try:
            service.save(reference, _throwaway_credential_value())
        except CredentialStoreError as exc:
            raise _packaged_credential_store_error("save", exc) from exc
        status = service.status(reference)
        if status.code != CredentialStatusCode.READY:
            raise PackagedSmokeError(f"credential save did not become ready: {status.status_text}")
        return (*base_lines, "credential save: PASS", "credential retained for restart check")

    if mode == "check-delete":
        status = service.status(reference)
        if status.code != CredentialStatusCode.READY:
            raise PackagedSmokeError(
                f"credential was not ready after restart: {status.status_text}"
            )
        try:
            resolved = service.resolve(reference)
        except CredentialStoreError as exc:
            raise _packaged_credential_store_error("restart readiness check", exc) from exc
        if not resolved.strip():
            raise PackagedSmokeError("credential resolved to an empty value after restart.")
        try:
            service.delete(reference)
        except CredentialStoreError as exc:
            raise _packaged_credential_store_error("cleanup", exc) from exc
        missing = service.status(reference)
        if missing.code != CredentialStatusCode.MISSING:
            raise PackagedSmokeError("credential cleanup did not return to missing state.")
        return (
            *base_lines,
            "credential restart readiness: PASS",
            "credential cleanup: PASS",
        )

    _delete_if_present(service, reference)
    secret = _throwaway_credential_value()
    try:
        service.save(reference, secret)
    except CredentialStoreError as exc:
        raise _packaged_credential_store_error("save", exc) from exc
    try:
        resolved = service.resolve(reference)
    except CredentialStoreError as exc:
        raise _packaged_credential_store_error("read", exc) from exc
    if resolved != secret:
        raise PackagedSmokeError("credential read did not match the saved throwaway value.")
    try:
        service.delete(reference)
    except CredentialStoreError as exc:
        raise _packaged_credential_store_error("cleanup", exc) from exc
    missing = service.status(reference)
    if missing.code != CredentialStatusCode.MISSING:
        raise PackagedSmokeError("credential cleanup did not return to missing state.")
    return (
        *base_lines,
        "credential save/read/delete: PASS",
        "credential cleanup: PASS",
    )


def _assert_inside_app_data(path: Path, app_data_dir: Path, label: str) -> None:
    try:
        path.resolve().relative_to(app_data_dir.resolve())
    except ValueError as exc:
        raise PackagedSmokeError(f"{label} file escaped the smoke app data directory.") from exc


def _import_keyring() -> Any:
    try:
        import keyring
    except Exception as exc:
        raise PackagedSmokeError("keyring is not available in this runtime.") from exc
    return keyring


def _keyring_backend_label(keyring_module: Any) -> str:
    get_keyring = getattr(keyring_module, "get_keyring", None)
    if callable(get_keyring):
        try:
            backend = get_keyring()
        except Exception as exc:
            raise PackagedSmokeError("keyring backend discovery failed.") from exc
        return f"{backend.__class__.__module__}.{backend.__class__.__name__}"
    return f"{keyring_module.__class__.__module__}.{keyring_module.__class__.__name__}"


def _throwaway_credential_value() -> str:
    return uuid.uuid4().hex


def _packaged_credential_store_error(
    action: str,
    exc: CredentialStoreError,
) -> PackagedSmokeError:
    if isinstance(exc, CredentialMissingError):
        reason = "credential missing"
    elif isinstance(exc, CredentialUnsupportedError):
        reason = "credential source unsupported"
    elif isinstance(exc, CredentialUnavailableError):
        reason = "credential source unavailable"
    else:
        reason = "credential store failed"
    return PackagedSmokeError(f"credential {action} failed: {reason}.")


def _delete_if_present(service: CredentialService, reference: CredentialReference) -> None:
    try:
        if service.status(reference).code == CredentialStatusCode.READY:
            service.delete(reference)
    except CredentialStoreError:
        return
