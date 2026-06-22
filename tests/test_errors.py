from snaplex.errors import (
    EmptyTranslationInputError,
    FallbackExhaustedError,
    MissingProviderCredentialError,
    StaleTranslationResultError,
    TranslationProviderError,
    TranslationProviderTimeoutError,
    UnknownTranslationProviderError,
    UnsupportedLanguageError,
)


def test_translation_errors_have_stable_codes_and_messages() -> None:
    errors = [
        EmptyTranslationInputError(),
        TranslationProviderError(provider_name="fake"),
        TranslationProviderTimeoutError(provider_name="slow"),
        MissingProviderCredentialError(env_var="SNAPLEX_EXAMPLE_API_KEY", provider_name="api"),
        StaleTranslationResultError(provider_name="stale"),
        UnknownTranslationProviderError(provider_name="missing"),
    ]

    assert [error.code for error in errors] == [
        "empty_input",
        "provider_failure",
        "provider_timeout",
        "missing_provider_credential",
        "stale_result",
        "unknown_provider",
    ]
    assert str(errors[1]) == "Translation provider failed."
    assert errors[1].provider_name == "fake"
    assert errors[3].env_var == "SNAPLEX_EXAMPLE_API_KEY"


def test_unsupported_language_error_keeps_language_pair() -> None:
    error = UnsupportedLanguageError(
        source_lang="en",
        target_lang="xx",
        provider_name="fake",
    )

    assert error.code == "unsupported_language"
    assert error.source_lang == "en"
    assert error.target_lang == "xx"
    assert error.provider_name == "fake"


def test_fallback_exhausted_error_keeps_provider_errors() -> None:
    first = TranslationProviderError("first failed", provider_name="first")
    second = TranslationProviderTimeoutError(provider_name="second")

    error = FallbackExhaustedError(provider_errors=(first, second))

    assert error.code == "fallback_exhausted"
    assert error.provider_errors == (first, second)
