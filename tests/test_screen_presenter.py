import asyncio

from snaplex.errors import TranslationProviderError
from snaplex.providers import TranslationResponse
from snaplex.services import (
    FakeCaptureService,
    FakeOcrScenario,
    FakeOcrService,
    OcrResult,
    OcrUnavailableError,
    ScreenRegion,
)
from snaplex.ui.screen_presenter import ScreenTranslationPresenter, ScreenTranslationStatus


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


class RecordingOcrService:
    def __init__(self, text: str) -> None:
        self.text = text
        self.calls = 0

    def extract_text(self, image) -> OcrResult:
        self.calls += 1
        return OcrResult(text=self.text)


class UnavailableOcrService:
    def extract_text(self, image) -> OcrResult:
        raise OcrUnavailableError("missing model")


class RecordingHistoryService:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def add_translation(self, **kwargs: str) -> object:
        self.calls.append(kwargs)
        return object()


def test_screen_presenter_starts_idle() -> None:
    presenter = ScreenTranslationPresenter()

    assert presenter.state.status == ScreenTranslationStatus.IDLE
    assert presenter.state.status_text == "Ready"
    assert presenter.state.can_copy is False
    assert presenter.state.can_retry is False


def test_screen_presenter_enters_loading_when_translation_requested() -> None:
    calls: list[str] = []
    presenter = ScreenTranslationPresenter(on_translate_requested=lambda: calls.append("called"))

    state = presenter.request_screen_translation()

    assert calls == ["called"]
    assert state.status == ScreenTranslationStatus.LOADING
    assert state.status_text == "Translating screen..."
    assert state.can_copy is False
    assert state.can_retry is False


def test_screen_presenter_translates_region_through_capture_ocr_and_pipeline() -> None:
    region = ScreenRegion(left=10, top=20, width=120, height=80)
    capture_service = FakeCaptureService()
    ocr_service = FakeOcrService(text="screen text")
    pipeline = FakePipeline(TranslationResponse("translated screen", "fake", "auto", "en"))
    presenter = ScreenTranslationPresenter()

    state = asyncio.run(
        presenter.translate_region(
            region=region,
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
    )

    assert capture_service.regions == [region]
    assert pipeline.requests == ["screen text"]
    assert state.status == ScreenTranslationStatus.SUCCESS
    assert state.source_text == "screen text"
    assert state.translated_text == "translated screen"
    assert state.provider_name == "fake"
    assert state.can_copy is True
    assert state.can_retry is True


def test_screen_presenter_records_successful_translation_history() -> None:
    region = ScreenRegion(left=10, top=20, width=120, height=80)
    capture_service = FakeCaptureService()
    ocr_service = FakeOcrService(text="screen text")
    pipeline = FakePipeline(TranslationResponse("translated screen", "fake", "en", "es"))
    history_service = RecordingHistoryService()
    presenter = ScreenTranslationPresenter(history_service=history_service)

    asyncio.run(
        presenter.translate_region(
            region=region,
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
    )

    assert history_service.calls == [
        {
            "source_text": "screen text",
            "translated_text": "translated screen",
            "provider_name": "fake",
            "source_lang": "en",
            "target_lang": "es",
            "flow": "screen",
        }
    ]


def test_screen_presenter_maps_invalid_region_points_without_capture() -> None:
    capture_service = FakeCaptureService()
    ocr_service = RecordingOcrService("unused")
    pipeline = FakePipeline(TranslationResponse("unused", "fake", "auto", "en"))
    presenter = ScreenTranslationPresenter()

    state = asyncio.run(
        presenter.translate_region_from_points(
            start_x=5,
            start_y=5,
            end_x=5,
            end_y=30,
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
    )

    assert capture_service.regions == []
    assert ocr_service.calls == 0
    assert pipeline.requests == []
    assert state.status == ScreenTranslationStatus.ERROR
    assert state.error_message == "Select a non-empty screen region."


def test_screen_presenter_can_show_selection_cancelled() -> None:
    presenter = ScreenTranslationPresenter()

    state = presenter.show_selection_cancelled()

    assert state.status == ScreenTranslationStatus.CANCELLED
    assert state.status_text == "Screen selection cancelled"
    assert state.error_message == "Select a region to translate."
    assert state.can_copy is False
    assert state.can_retry is True


def test_screen_presenter_maps_empty_ocr_result() -> None:
    region = ScreenRegion(left=10, top=20, width=120, height=80)
    capture_service = FakeCaptureService()
    ocr_service = FakeOcrService(scenario=FakeOcrScenario.EMPTY)
    pipeline = FakePipeline(TranslationResponse("", "fake", "auto", "en"))
    presenter = ScreenTranslationPresenter()

    state = asyncio.run(
        presenter.translate_region(
            region=region,
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
    )

    assert pipeline.requests == [""]
    assert state.status == ScreenTranslationStatus.EMPTY
    assert state.status_text == "No screen text found"
    assert state.error_message == "No text was detected in the selected region."
    assert state.can_copy is False
    assert state.can_retry is True


def test_screen_presenter_maps_capture_failure_without_ocr_or_pipeline() -> None:
    region = ScreenRegion(left=10, top=20, width=120, height=80)
    capture_service = FakeCaptureService()
    capture_service.fail_next()
    ocr_service = RecordingOcrService("unused")
    pipeline = FakePipeline(TranslationResponse("unused", "fake", "auto", "en"))
    presenter = ScreenTranslationPresenter()

    state = asyncio.run(
        presenter.translate_region(
            region=region,
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
    )

    assert capture_service.regions == [region]
    assert ocr_service.calls == 0
    assert pipeline.requests == []
    assert state.status == ScreenTranslationStatus.ERROR
    assert state.error_message == "Could not capture the selected screen region. Try again."
    assert state.can_copy is False
    assert state.can_retry is True


def test_screen_presenter_maps_ocr_failure_without_pipeline() -> None:
    region = ScreenRegion(left=10, top=20, width=120, height=80)
    capture_service = FakeCaptureService()
    ocr_service = FakeOcrService(scenario=FakeOcrScenario.FAILURE)
    pipeline = FakePipeline(TranslationResponse("unused", "fake", "auto", "en"))
    presenter = ScreenTranslationPresenter()

    state = asyncio.run(
        presenter.translate_region(
            region=region,
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
    )

    assert pipeline.requests == []
    assert state.status == ScreenTranslationStatus.ERROR
    assert state.error_message == "OCR failed to read text from the selected region. Try again."
    assert presenter.copy_result() is False


def test_screen_presenter_maps_unavailable_ocr_without_pipeline() -> None:
    region = ScreenRegion(left=10, top=20, width=120, height=80)
    capture_service = FakeCaptureService()
    pipeline = FakePipeline(TranslationResponse("unused", "fake", "auto", "en"))
    presenter = ScreenTranslationPresenter()

    state = asyncio.run(
        presenter.translate_region(
            region=region,
            capture_service=capture_service,
            ocr_service=UnavailableOcrService(),
            pipeline=pipeline,
        )
    )

    assert pipeline.requests == []
    assert state.status == ScreenTranslationStatus.ERROR
    assert state.error_message == "OCR is unavailable. Install OCR support or use fake OCR mode."


def test_screen_presenter_maps_translation_failure() -> None:
    region = ScreenRegion(left=10, top=20, width=120, height=80)
    capture_service = FakeCaptureService()
    ocr_service = FakeOcrService(text="screen text")
    pipeline = FakePipeline(error=TranslationProviderError(provider_name="fake"))
    presenter = ScreenTranslationPresenter()

    state = asyncio.run(
        presenter.translate_region(
            region=region,
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
    )

    assert pipeline.requests == ["screen text"]
    assert state.status == ScreenTranslationStatus.ERROR
    assert state.error_message == "Translation provider failed. Try again."
    assert presenter.copy_result() is False


def test_screen_presenter_retries_last_region() -> None:
    region = ScreenRegion(left=10, top=20, width=120, height=80)
    capture_service = FakeCaptureService()
    ocr_service = FakeOcrService(text="screen text")
    pipeline = FakePipeline(TranslationResponse("translated screen", "fake", "auto", "en"))
    presenter = ScreenTranslationPresenter()

    asyncio.run(
        presenter.translate_region(
            region=region,
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
    )
    state = asyncio.run(
        presenter.retry_translation(
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
    )

    assert capture_service.regions == [region, region]
    assert pipeline.requests == ["screen text", "screen text"]
    assert state.status == ScreenTranslationStatus.SUCCESS


def test_screen_presenter_close_result_resets_state() -> None:
    presenter = ScreenTranslationPresenter()
    presenter.show_success(source_text="screen", translated_text="translated")

    state = presenter.close_result()

    assert state.status == ScreenTranslationStatus.IDLE
    assert state.status_text == "Ready"
