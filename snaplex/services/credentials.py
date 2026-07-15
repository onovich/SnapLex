"""Credential service boundaries that keep secret values out of config."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class CredentialSource(str, Enum):
    NONE = "none"
    ENVIRONMENT = "environment"
    KEYRING = "keyring"
    UNSUPPORTED = "unsupported"


class CredentialStatusCode(str, Enum):
    READY = "ready"
    MISSING = "missing"
    SAVED = "saved"
    DELETED = "deleted"
    UNSUPPORTED = "unsupported"
    UNAVAILABLE = "unavailable"
    FAILED = "failed"


@dataclass(frozen=True)
class CredentialReference:
    """Non-secret pointer to a provider credential."""

    provider_name: str
    source: CredentialSource = CredentialSource.NONE
    identifier: str = ""

    @property
    def is_configured(self) -> bool:
        return self.source not in {CredentialSource.NONE, CredentialSource.UNSUPPORTED} and bool(
            self.identifier.strip()
        )


@dataclass(frozen=True)
class CredentialStatus:
    """User-facing credential state without secret material."""

    reference: CredentialReference
    code: CredentialStatusCode
    status_text: str
    detail_text: str = ""
    can_resolve: bool = False
    can_save: bool = False
    can_delete: bool = False


class CredentialStore(Protocol):
    source: CredentialSource

    def resolve(self, reference: CredentialReference) -> str:
        """Return the secret for a reference or raise CredentialStoreError."""
        ...

    def save(self, reference: CredentialReference, secret: str) -> None:
        """Persist a secret for a reference."""
        ...

    def delete(self, reference: CredentialReference) -> None:
        """Delete a secret for a reference."""
        ...

    def contains(self, reference: CredentialReference) -> bool:
        """Return whether the reference can resolve to a secret."""
        ...


class CredentialStoreError(RuntimeError):
    def __init__(self, message: str, *, reference: CredentialReference) -> None:
        super().__init__(message)
        self.reference = reference

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(provider_name={self.reference.provider_name!r}, "
            f"source={self.reference.source.value!r}, identifier={self.reference.identifier!r})"
        )


class CredentialMissingError(CredentialStoreError):
    pass


class CredentialUnsupportedError(CredentialStoreError):
    pass


class InMemoryCredentialStore:
    """Deterministic fake credential store for tests and smoke paths."""

    source = CredentialSource.KEYRING

    def __init__(self, initial_secrets: Mapping[CredentialReference, str] | None = None) -> None:
        self._secrets: dict[tuple[str, str, str], str] = {}
        for reference, secret in (initial_secrets or {}).items():
            self.save(reference, secret)

    def __repr__(self) -> str:
        return f"InMemoryCredentialStore(count={len(self._secrets)})"

    def resolve(self, reference: CredentialReference) -> str:
        secret = self._secrets.get(_reference_key(reference))
        if not secret:
            raise CredentialMissingError("Credential is missing.", reference=reference)
        return secret

    def save(self, reference: CredentialReference, secret: str) -> None:
        cleaned_secret = secret.strip()
        if not cleaned_secret:
            raise CredentialMissingError("Credential value is empty.", reference=reference)
        self._secrets[_reference_key(reference)] = cleaned_secret

    def delete(self, reference: CredentialReference) -> None:
        self._secrets.pop(_reference_key(reference), None)

    def contains(self, reference: CredentialReference) -> bool:
        return bool(self._secrets.get(_reference_key(reference)))


class CredentialService:
    """Resolve credential references through source-specific stores."""

    def __init__(self, stores: Mapping[CredentialSource, CredentialStore] | None = None) -> None:
        self._stores = dict(stores or {})

    def __repr__(self) -> str:
        return f"CredentialService(sources={tuple(source.value for source in self._stores)})"

    def status(self, reference: CredentialReference) -> CredentialStatus:
        if reference.source == CredentialSource.NONE:
            return CredentialStatus(
                reference=reference,
                code=CredentialStatusCode.MISSING,
                status_text="Credential not configured",
                detail_text="Choose an environment variable or local secure credential source.",
            )
        store = self._stores.get(reference.source)
        if store is None:
            return CredentialStatus(
                reference=reference,
                code=CredentialStatusCode.UNSUPPORTED,
                status_text="Credential source unsupported",
                detail_text=f"{reference.source.value} is not available in this SnapLex runtime.",
            )
        if not reference.identifier.strip():
            return CredentialStatus(
                reference=reference,
                code=CredentialStatusCode.MISSING,
                status_text="Credential reference missing",
                detail_text="Configure a non-secret credential reference before testing.",
                can_save=True,
            )
        if store.contains(reference):
            return CredentialStatus(
                reference=reference,
                code=CredentialStatusCode.READY,
                status_text="Credential ready",
                detail_text=_ready_detail(reference),
                can_resolve=True,
                can_save=True,
                can_delete=True,
            )
        return CredentialStatus(
            reference=reference,
            code=CredentialStatusCode.MISSING,
            status_text="Credential missing",
            detail_text=_missing_detail(reference),
            can_save=True,
        )

    def resolve(self, reference: CredentialReference) -> str:
        store = self._require_store(reference)
        return store.resolve(reference)

    def save(self, reference: CredentialReference, secret: str) -> CredentialStatus:
        store = self._require_store(reference)
        store.save(reference, secret)
        return CredentialStatus(
            reference=reference,
            code=CredentialStatusCode.SAVED,
            status_text="Credential saved",
            detail_text=_ready_detail(reference),
            can_resolve=True,
            can_save=True,
            can_delete=True,
        )

    def delete(self, reference: CredentialReference) -> CredentialStatus:
        store = self._require_store(reference)
        store.delete(reference)
        return CredentialStatus(
            reference=reference,
            code=CredentialStatusCode.DELETED,
            status_text="Credential deleted",
            detail_text=_missing_detail(reference),
            can_save=True,
        )

    def _require_store(self, reference: CredentialReference) -> CredentialStore:
        store = self._stores.get(reference.source)
        if store is None:
            raise CredentialUnsupportedError(
                "Credential source is unsupported.", reference=reference
            )
        return store


def credential_reference_to_dict(reference: CredentialReference) -> dict[str, str]:
    """Serialize a credential reference without secret material."""

    return {
        "provider_name": reference.provider_name,
        "source": reference.source.value,
        "identifier": reference.identifier,
    }


def credential_reference_from_dict(payload: Mapping[object, object]) -> CredentialReference:
    provider_name = _string_value(payload.get("provider_name"))
    source = _credential_source_value(payload.get("source"))
    identifier = _string_value(payload.get("identifier"))
    return CredentialReference(
        provider_name=provider_name,
        source=source,
        identifier=identifier,
    )


def _reference_key(reference: CredentialReference) -> tuple[str, str, str]:
    return (
        reference.provider_name.strip().lower(),
        reference.source.value,
        reference.identifier.strip(),
    )


def _ready_detail(reference: CredentialReference) -> str:
    if reference.source == CredentialSource.ENVIRONMENT:
        return f"{reference.identifier} is set in this process. The value is not stored."
    if reference.source == CredentialSource.KEYRING:
        return "Local secure credential is available. The value is not shown or stored in config."
    return "Credential reference is available."


def _missing_detail(reference: CredentialReference) -> str:
    if reference.source == CredentialSource.ENVIRONMENT:
        return f"Set {reference.identifier} in your shell before testing."
    if reference.source == CredentialSource.KEYRING:
        return "Save a local secure credential before testing."
    return "Configure a credential source before testing."


def _credential_source_value(value: object) -> CredentialSource:
    if not isinstance(value, str):
        return CredentialSource.NONE
    try:
        return CredentialSource(value.strip().lower())
    except ValueError:
        return CredentialSource.UNSUPPORTED


def _string_value(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""
