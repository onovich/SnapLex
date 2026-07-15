from snaplex.ui.translation_result import (
    TranslationResultState,
    TranslationResultStatus,
    build_result_display,
)


def test_idle_display_uses_stable_placeholders() -> None:
    display = build_result_display(TranslationResultState())

    assert display.state_label == "Ready"
    assert display.source_text == "No source text yet."
    assert display.translated_text == "Translation will appear here."
    assert display.provider_visible is False
    assert display.error_visible is False


def test_loading_display_keeps_source_context() -> None:
    display = build_result_display(
        TranslationResultState(
            status=TranslationResultStatus.LOADING,
            source_text="hello",
        )
    )

    assert display.state_label == "Working"
    assert display.source_text == "hello"
    assert display.translated_text == "Translating..."


def test_fake_success_display_keeps_provider_warning_visible() -> None:
    display = build_result_display(
        TranslationResultState(
            status=TranslationResultStatus.SUCCESS,
            source_text="hello",
            translated_text="hello [zh]",
            provider_name="fake",
            provider_notice="Fake smoke mode: deterministic placeholder output.",
        )
    )

    assert display.state_label == "Done"
    assert display.provider_text == "Provider: fake"
    assert display.provider_visible is True
    assert display.provider_notice_visible is True


def test_error_display_prioritizes_actionable_error_message() -> None:
    display = build_result_display(
        TranslationResultState(
            status=TranslationResultStatus.ERROR,
            source_text="hello",
            error_message="Translation timed out. Try again.",
        )
    )

    assert display.state_label == "Needs attention"
    assert display.source_text == "hello"
    assert display.translated_text == "No translation available."
    assert display.error_visible is True
