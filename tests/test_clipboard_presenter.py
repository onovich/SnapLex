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
