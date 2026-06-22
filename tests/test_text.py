from snaplex.services import TranslationService, normalize_text
from snaplex.providers import FakeTranslationProvider


def test_normalize_text_trims_lines_and_preserves_line_breaks() -> None:
    assert normalize_text("  Hello\r\n world \rsecond line  ") == "Hello\nworld\nsecond line"


def test_normalize_text_collapses_whitespace_only_input_to_empty() -> None:
    assert normalize_text(" \r\n\t ") == ""


def test_translation_service_normalizes_before_provider_call() -> None:
    provider = FakeTranslationProvider({"Hello\nworld": "HELLO WORLD"})
    service = TranslationService(provider)

    result = service.translate_text("  Hello\r\n world  ")

    assert result.translated_text == "HELLO WORLD"


def test_translation_service_returns_empty_without_provider_lookup() -> None:
    provider = FakeTranslationProvider(fail=True)
    service = TranslationService(provider)

    result = service.translate_text("   ")

    assert result.translated_text == ""
    assert result.provider_name == "fake"
