import pytest

from snaplex.providers import (
    FakeTranslationProvider,
    FakeTranslationScenario,
    StaleTranslationResultError,
    TranslationProviderError,
    TranslationProviderTimeoutError,
    TranslationRequest,
    UnsupportedLanguageError,
)


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


@pytest.mark.parametrize(
    ("scenario", "error_type"),
    [
        (FakeTranslationScenario.FAILURE, TranslationProviderError),
        (FakeTranslationScenario.TIMEOUT, TranslationProviderTimeoutError),
        (FakeTranslationScenario.UNSUPPORTED_LANGUAGE, UnsupportedLanguageError),
        (FakeTranslationScenario.STALE_RESULT, StaleTranslationResultError),
    ],
)
def test_fake_provider_supports_deterministic_error_scenarios(
    scenario: FakeTranslationScenario,
    error_type: type[Exception],
) -> None:
    provider = FakeTranslationProvider(name="scenario", scenario=scenario)

    with pytest.raises(error_type) as exc_info:
        provider.translate(TranslationRequest(text="hello", target_lang="xx"))

    assert getattr(exc_info.value, "provider_name") == "scenario"
