import asyncio

from snaplex.errors import (
    FallbackExhaustedError,
    TranslationProviderError,
    TranslationProviderTimeoutError,
    UnknownTranslationProviderError,
    UnsupportedLanguageError,
)
from snaplex.providers import TranslationResponse
from snaplex.services import InMemoryClipboardService
from snaplex.ui.clipboard_presenter import (
    ClipboardTranslationPresenter,
    ClipboardTranslationStatus,
)


class FakePipeline:
    def __init__(
        self,
        response: TranslationResponse | None = None,
        *,
        error: Exception | None = None,
    ) -> None:
        self.response = response
        self.error = error
        self.requests: list[str] = []

    async def translate_text_async(self, text: str) -> TranslationResponse:
        self.requests.append(text)
        if self.error is not None:
            raise self.error
        if self.response is None:
            raise AssertionError("FakePipeline requires a response or error.")
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


def test_presenter_maps_timeout_error_and_disables_copy() -> None:
    clipboard = InMemoryClipboardService("hello")
    pipeline = FakePipeline(error=TranslationProviderTimeoutError(provider_name="fake"))
    copied: list[str] = []
    presenter = ClipboardTranslationPresenter(on_copy_result=copied.append)

    state = asyncio.run(
        presenter.translate_clipboard(
            clipboard_service=clipboard,
            pipeline=pipeline,
        )
    )
    copied_result = presenter.copy_result()

    assert pipeline.requests == ["hello"]
    assert state.status == ClipboardTranslationStatus.ERROR
    assert state.source_text == "hello"
    assert state.error_message == "Translation timed out. Try again."
    assert state.can_retry is True
    assert state.can_copy is False
    assert copied_result is False
    assert copied == []


def test_presenter_maps_provider_failure_error() -> None:
    clipboard = InMemoryClipboardService("hello")
    pipeline = FakePipeline(error=TranslationProviderError(provider_name="fake"))
    presenter = ClipboardTranslationPresenter()

    state = asyncio.run(
        presenter.translate_clipboard(
            clipboard_service=clipboard,
            pipeline=pipeline,
        )
    )

    assert state.status == ClipboardTranslationStatus.ERROR
    assert state.error_message == "Translation provider failed. Try again."


def test_presenter_maps_fallback_exhausted_error() -> None:
    clipboard = InMemoryClipboardService("hello")
    pipeline = FakePipeline(
        error=FallbackExhaustedError(
            provider_errors=(TranslationProviderError(provider_name="fake"),)
        )
    )
    presenter = ClipboardTranslationPresenter()

    state = asyncio.run(
        presenter.translate_clipboard(
            clipboard_service=clipboard,
            pipeline=pipeline,
        )
    )

    assert state.status == ClipboardTranslationStatus.ERROR
    assert state.error_message == "All configured translation providers failed. Try again."


def test_presenter_maps_unknown_provider_error() -> None:
    clipboard = InMemoryClipboardService("hello")
    pipeline = FakePipeline(error=UnknownTranslationProviderError(provider_name="missing"))
    presenter = ClipboardTranslationPresenter()

    state = asyncio.run(
        presenter.translate_clipboard(
            clipboard_service=clipboard,
            pipeline=pipeline,
        )
    )

    assert state.status == ClipboardTranslationStatus.ERROR
    assert state.error_message == "Configured translation provider is not available."


def test_presenter_maps_unsupported_language_error() -> None:
    clipboard = InMemoryClipboardService("hello")
    pipeline = FakePipeline(
        error=UnsupportedLanguageError(
            source_lang="ja",
            target_lang="xx",
            provider_name="fake",
        )
    )
    presenter = ClipboardTranslationPresenter()

    state = asyncio.run(
        presenter.translate_clipboard(
            clipboard_service=clipboard,
            pipeline=pipeline,
        )
    )

    assert state.status == ClipboardTranslationStatus.ERROR
    assert state.error_message == "Language pair ja -> xx is not supported."


def test_presenter_retries_last_source_text() -> None:
    clipboard = InMemoryClipboardService("new clipboard")
    presenter = ClipboardTranslationPresenter()
    presenter.show_error("Translation timed out. Try again.", source_text="previous")
    pipeline = FakePipeline(TranslationResponse("retry result", "fake", "auto", "es"))

    state = asyncio.run(
        presenter.retry_translation(
            clipboard_service=clipboard,
            pipeline=pipeline,
        )
    )

    assert pipeline.requests == ["previous"]
    assert state.status == ClipboardTranslationStatus.SUCCESS
    assert state.source_text == "previous"
    assert state.translated_text == "retry result"


def test_presenter_retry_reads_clipboard_when_no_source_exists() -> None:
    clipboard = InMemoryClipboardService("fresh")
    presenter = ClipboardTranslationPresenter()
    presenter.show_empty_clipboard()
    pipeline = FakePipeline(TranslationResponse("fresh result", "fake", "auto", "es"))

    state = asyncio.run(
        presenter.retry_translation(
            clipboard_service=clipboard,
            pipeline=pipeline,
        )
    )

    assert pipeline.requests == ["fresh"]
    assert state.status == ClipboardTranslationStatus.SUCCESS
    assert state.source_text == "fresh"
