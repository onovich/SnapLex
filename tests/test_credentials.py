import json

import pytest

from snaplex.services.credentials import (
    CredentialMissingError,
    CredentialReference,
    CredentialService,
    CredentialSource,
    CredentialStatusCode,
    CredentialUnsupportedError,
    EnvironmentCredentialStore,
    InMemoryCredentialStore,
    credential_reference_from_dict,
    credential_reference_to_dict,
    create_environment_credential_service,
    environment_credential_reference,
)


def test_credential_reference_serializes_without_secret_value() -> None:
    reference = CredentialReference(
        provider_name="openai",
        source=CredentialSource.KEYRING,
        identifier="snaplex/openai/default",
    )

    serialized = credential_reference_to_dict(reference)
    serialized_text = json.dumps(serialized)

    assert serialized == {
        "provider_name": "openai",
        "source": "keyring",
        "identifier": "snaplex/openai/default",
    }
    assert "secret-value" not in repr(reference)
    assert "secret-value" not in serialized_text


def test_credential_reference_parses_unknown_source_as_unsupported() -> None:
    reference = credential_reference_from_dict(
        {
            "provider_name": "openai",
            "source": "cloud",
            "identifier": "future",
        }
    )

    assert reference.provider_name == "openai"
    assert reference.source == CredentialSource.UNSUPPORTED
    assert reference.identifier == "future"


def test_in_memory_credential_store_resolves_saved_secret_without_repr_leak() -> None:
    reference = CredentialReference(
        provider_name="deepl",
        source=CredentialSource.KEYRING,
        identifier="snaplex/deepl/default",
    )
    store = InMemoryCredentialStore()

    store.save(reference, " secret-value ")

    assert store.resolve(reference) == "secret-value"
    assert store.contains(reference) is True
    assert "secret-value" not in repr(store)


def test_in_memory_credential_store_rejects_empty_secret() -> None:
    reference = CredentialReference(
        provider_name="openai",
        source=CredentialSource.KEYRING,
        identifier="snaplex/openai/default",
    )
    store = InMemoryCredentialStore()

    with pytest.raises(CredentialMissingError) as exc_info:
        store.save(reference, " ")

    assert exc_info.value.reference == reference
    assert "secret" not in repr(exc_info.value).lower()


def test_environment_credential_store_resolves_mapping_without_repr_leak() -> None:
    reference = CredentialReference(
        provider_name="openai",
        source=CredentialSource.ENVIRONMENT,
        identifier="SNAPLEX_OPENAI_API_KEY",
    )
    store = EnvironmentCredentialStore({"SNAPLEX_OPENAI_API_KEY": " secret-value "})

    assert store.resolve(reference) == "secret-value"
    assert store.contains(reference) is True
    assert "secret-value" not in repr(store)


def test_environment_credential_store_rejects_save_and_delete() -> None:
    reference = CredentialReference(
        provider_name="deepl",
        source=CredentialSource.ENVIRONMENT,
        identifier="SNAPLEX_DEEPL_API_KEY",
    )
    store = EnvironmentCredentialStore({"SNAPLEX_DEEPL_API_KEY": "secret-value"})

    with pytest.raises(CredentialUnsupportedError):
        store.save(reference, "secret-value")
    with pytest.raises(CredentialUnsupportedError):
        store.delete(reference)

    assert store.resolve(reference) == "secret-value"


def test_environment_credential_reference_uses_none_for_missing_env_var() -> None:
    reference = environment_credential_reference("openai", " ")

    assert reference.provider_name == "openai"
    assert reference.source == CredentialSource.NONE
    assert reference.identifier == ""


def test_credential_service_reports_missing_none_reference() -> None:
    reference = CredentialReference(provider_name="openai")
    service = CredentialService()

    status = service.status(reference)

    assert status.code == CredentialStatusCode.MISSING
    assert status.can_resolve is False
    assert status.can_save is False


def test_credential_service_reports_environment_ready_as_read_only() -> None:
    reference = environment_credential_reference("openai", "SNAPLEX_OPENAI_API_KEY")
    service = create_environment_credential_service(
        {"SNAPLEX_OPENAI_API_KEY": "secret-value"},
    )

    status = service.status(reference)
    resolved = service.resolve(reference)

    assert status.code == CredentialStatusCode.READY
    assert status.can_resolve is True
    assert status.can_save is False
    assert status.can_delete is False
    assert resolved == "secret-value"
    assert "secret-value" not in repr(status)
    assert "secret-value" not in repr(service)


def test_credential_service_reports_missing_environment_as_read_only() -> None:
    reference = environment_credential_reference("openai", "SNAPLEX_OPENAI_API_KEY")
    service = create_environment_credential_service({})

    status = service.status(reference)

    assert status.code == CredentialStatusCode.MISSING
    assert status.can_resolve is False
    assert status.can_save is False


def test_credential_service_save_resolve_delete_cycle_without_status_leak() -> None:
    reference = CredentialReference(
        provider_name="openai",
        source=CredentialSource.KEYRING,
        identifier="snaplex/openai/default",
    )
    service = CredentialService(
        {CredentialSource.KEYRING: InMemoryCredentialStore()},
    )

    saved = service.save(reference, "secret-value")
    ready = service.status(reference)
    resolved = service.resolve(reference)
    deleted = service.delete(reference)
    missing = service.status(reference)

    assert saved.code == CredentialStatusCode.SAVED
    assert ready.code == CredentialStatusCode.READY
    assert resolved == "secret-value"
    assert deleted.code == CredentialStatusCode.DELETED
    assert missing.code == CredentialStatusCode.MISSING
    assert "secret-value" not in repr(saved)
    assert "secret-value" not in repr(ready)
    assert "secret-value" not in repr(service)


def test_credential_service_rejects_unsupported_source() -> None:
    reference = CredentialReference(
        provider_name="openai",
        source=CredentialSource.ENVIRONMENT,
        identifier="OPENAI_API_KEY",
    )
    service = CredentialService()

    status = service.status(reference)

    assert status.code == CredentialStatusCode.UNSUPPORTED
    with pytest.raises(CredentialUnsupportedError):
        service.resolve(reference)
