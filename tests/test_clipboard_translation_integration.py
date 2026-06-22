import asyncio

from snaplex.providers import TranslationResponse
from snaplex.services import InMemoryClipboardService
from snaplex.ui.clipboard_presenter import (
    ClipboardTranslationPresenter,
    ClipboardTranslationStatus,
)


class FakePipeline:
    def __init__(self, response: TranslationResponse) -> None:
        self.response = response
        self.requests: list[str] = []

    async def translate_text_async(self, text: str) -> TranslationResponse:
        self.requests.append(text)
        return self.response


def test_presenter_translates_clipboard_text_through_pipeline() -> None:
    clipboard = InMemoryClipboardService("hello")
    pipeline = FakePipeline(TranslationResponse("hola", "fake", "auto", "es"))
    presenter = ClipboardTranslationPresenter()

    state = asyncio.run(
        presenter.translate_clipboard(
            clipboard_service=clipboard,
            pipeline=pipeline,
        )
    )

    assert pipeline.requests == ["hello"]
    assert state.status == ClipboardTranslationStatus.SUCCESS
    assert state.source_text == "hello"
    assert state.translated_text == "hola"
    assert state.provider_name == "fake"
    assert state.can_copy is True


def test_presenter_maps_empty_clipboard_without_calling_pipeline() -> None:
    clipboard = InMemoryClipboardService("   ")
    pipeline = FakePipeline(TranslationResponse("unused", "fake", "auto", "es"))
    presenter = ClipboardTranslationPresenter()

    state = asyncio.run(
        presenter.translate_clipboard(
            clipboard_service=clipboard,
            pipeline=pipeline,
        )
    )

    assert pipeline.requests == []
    assert state.status == ClipboardTranslationStatus.EMPTY
    assert state.error_message == "Copy text before translating."
