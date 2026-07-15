from snaplex.ui.clipboard_presenter import (
    ClipboardTranslationPresenter,
    ClipboardTranslationStatus,
)


def test_presenter_starts_idle() -> None:
    presenter = ClipboardTranslationPresenter()

    assert presenter.state.status == ClipboardTranslationStatus.IDLE
    assert presenter.state.status_text == "Ready"
    assert presenter.state.can_copy is False
    assert presenter.state.can_retry is False


def test_presenter_enters_loading_when_translation_requested() -> None:
    calls: list[str] = []
    presenter = ClipboardTranslationPresenter(on_translate_requested=lambda: calls.append("called"))

    state = presenter.request_clipboard_translation()

    assert calls == ["called"]
    assert state.status == ClipboardTranslationStatus.LOADING
    assert state.status_text == "Translating clipboard..."
    assert state.can_copy is False
    assert state.can_retry is False


def test_presenter_can_reset_to_idle() -> None:
    presenter = ClipboardTranslationPresenter()
    presenter.request_clipboard_translation()

    state = presenter.reset()

    assert state.status == ClipboardTranslationStatus.IDLE
    assert state.status_text == "Ready"


def test_presenter_can_show_success_and_copy_result() -> None:
    copied: list[str] = []
    presenter = ClipboardTranslationPresenter(on_copy_result=copied.append)

    state = presenter.show_success(
        source_text="hello",
        translated_text="hola",
        provider_name="fake",
    )
    copied_result = presenter.copy_result()

    assert state.status == ClipboardTranslationStatus.SUCCESS
    assert state.source_text == "hello"
    assert state.translated_text == "hola"
    assert state.provider_name == "fake"
    assert "not real translation" in state.provider_notice
    assert state.can_copy is True
    assert state.can_retry is True
    assert copied_result is True
    assert copied == ["hola"]


def test_presenter_does_not_copy_when_not_successful() -> None:
    copied: list[str] = []
    presenter = ClipboardTranslationPresenter(on_copy_result=copied.append)

    copied_result = presenter.copy_result()

    assert copied_result is False
    assert copied == []


def test_presenter_success_omits_fake_notice_for_real_provider() -> None:
    presenter = ClipboardTranslationPresenter()

    state = presenter.show_success(
        source_text="hello",
        translated_text="hola",
        provider_name="openai",
    )

    assert state.provider_notice == ""


def test_presenter_can_show_empty_clipboard() -> None:
    presenter = ClipboardTranslationPresenter()

    state = presenter.show_empty_clipboard()

    assert state.status == ClipboardTranslationStatus.EMPTY
    assert state.status_text == "Clipboard is empty"
    assert state.error_message == "Copy text before translating."
    assert state.can_copy is False
    assert state.can_retry is True


def test_presenter_can_show_error() -> None:
    presenter = ClipboardTranslationPresenter()

    state = presenter.show_error("Provider timed out.", source_text="hello")

    assert state.status == ClipboardTranslationStatus.ERROR
    assert state.status_text == "Translation failed"
    assert state.source_text == "hello"
    assert state.error_message == "Provider timed out."
    assert state.can_copy is False
    assert state.can_retry is True


def test_presenter_close_result_resets_state() -> None:
    presenter = ClipboardTranslationPresenter()
    presenter.show_success(source_text="hello", translated_text="hola")

    state = presenter.close_result()

    assert state.status == ClipboardTranslationStatus.IDLE
    assert state.status_text == "Ready"
