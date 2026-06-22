import asyncio

from snaplex.providers import TranslationResponse
from snaplex.services import CapturedImage, FakeOcrService, ScreenRegion
from snaplex.ui.screen_presenter import ScreenTranslationPresenter, ScreenTranslationStatus


class FakePipeline:
    def __init__(self, response: TranslationResponse) -> None:
        self.response = response
        self.requests: list[str] = []

    async def translate_text_async(self, text: str) -> TranslationResponse:
        self.requests.append(text)
        return self.response


class RecordingCaptureService:
    def __init__(self) -> None:
        self.regions: list[ScreenRegion] = []

    def capture_region(self, region: ScreenRegion) -> CapturedImage:
        self.regions.append(region)
        return CapturedImage(region=region, data=b"fake-screen")


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
    capture_service = RecordingCaptureService()
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


def test_screen_presenter_close_result_resets_state() -> None:
    presenter = ScreenTranslationPresenter()
    presenter.show_success(source_text="screen", translated_text="translated")

    state = presenter.close_result()

    assert state.status == ScreenTranslationStatus.IDLE
    assert state.status_text == "Ready"
