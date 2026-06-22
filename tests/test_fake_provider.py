import pytest

from snaplex.providers import FakeTranslationProvider, TranslationProviderError, TranslationRequest


def test_fake_provider_uses_mapping() -> None:
    provider = FakeTranslationProvider({"hello": "hola"})

    result = provider.translate(TranslationRequest(text="hello", target_lang="es"))

    assert result.translated_text == "hola"
    assert result.provider_name == "fake"
    assert result.source_lang == "auto"
    assert result.target_lang == "es"


def test_fake_provider_has_deterministic_default() -> None:
    provider = FakeTranslationProvider()

    result = provider.translate(TranslationRequest(text="hello", target_lang="ja"))

    assert result.translated_text == "hello [ja]"


def test_fake_provider_can_fail() -> None:
    provider = FakeTranslationProvider(fail=True)

    with pytest.raises(TranslationProviderError):
        provider.translate(TranslationRequest(text="hello"))
