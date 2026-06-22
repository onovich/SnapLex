import pytest

from snaplex.errors import UnknownTranslationProviderError
from snaplex.providers import (
    FakeTranslationProvider,
    ProviderRegistry,
    create_default_provider_registry,
)


def test_registry_returns_registered_provider() -> None:
    provider = FakeTranslationProvider(name="local")
    registry = ProviderRegistry([provider])

    assert registry.get("local") is provider
    assert registry.names() == ("local",)


def test_registry_replaces_provider_by_name() -> None:
    old_provider = FakeTranslationProvider(name="fake", translations={"hello": "old"})
    new_provider = FakeTranslationProvider(name="fake", translations={"hello": "new"})
    registry = ProviderRegistry([old_provider])

    registry.register(new_provider)

    assert registry.get("fake") is new_provider


def test_registry_raises_for_unknown_provider() -> None:
    registry = ProviderRegistry()

    with pytest.raises(UnknownTranslationProviderError) as exc_info:
        registry.get("missing")

    assert exc_info.value.code == "unknown_provider"
    assert exc_info.value.provider_name == "missing"


def test_registry_resolves_provider_order() -> None:
    first = FakeTranslationProvider(name="first")
    second = FakeTranslationProvider(name="second")
    registry = ProviderRegistry([first, second])

    assert registry.resolve_order(["second", "first"]) == (second, first)


def test_default_registry_contains_fake_provider() -> None:
    registry = create_default_provider_registry()

    assert registry.get("fake").name == "fake"
