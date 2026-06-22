import asyncio

from snaplex.providers import TranslationResponse
from snaplex.services import (
    FakeCaptureService,
    FakeOcrService,
    ScreenRegion,
    ScreenTranslationService,
    create_default_translation_pipeline,
)


class FakePipeline:
    def __init__(self, response: TranslationResponse) -> None:
        self.response = response
        self.requests: list[str] = []

    async def translate_text_async(self, text: str) -> TranslationResponse:
        self.requests.append(text)
        return self.response


def test_screen_translation_service_uses_capture_ocr_and_pipeline() -> None:
    region = ScreenRegion(left=5, top=10, width=80, height=40)
    capture_service = FakeCaptureService(image_data=b"screen")
    ocr_service = FakeOcrService(text="screen text", confidence=0.8)
    pipeline = FakePipeline(TranslationResponse("translated text", "fake", "auto", "en"))
    service = ScreenTranslationService(
        capture_service=capture_service,
        ocr_service=ocr_service,
        pipeline=pipeline,
    )

    response = asyncio.run(service.translate_region(region))

    assert capture_service.regions == [region]
    assert pipeline.requests == ["screen text"]
    assert response.region == region
    assert response.source_text == "screen text"
    assert response.translated_text == "translated text"
    assert response.provider_name == "fake"
    assert response.ocr_confidence == 0.8


def test_screen_translation_service_works_with_default_p1_pipeline() -> None:
    region = ScreenRegion(left=5, top=10, width=80, height=40)
    service = ScreenTranslationService(
        capture_service=FakeCaptureService(image_data=b"screen"),
        ocr_service=FakeOcrService(text="screen text"),
        pipeline=create_default_translation_pipeline(),
    )

    response = asyncio.run(service.translate_region(region))

    assert response.source_text == "screen text"
    assert response.translated_text == "screen text [en]"
    assert response.provider_name == "fake"
