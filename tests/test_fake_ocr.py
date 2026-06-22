import pytest

from snaplex.services import FakeCaptureService, FakeOcrService, OcrError, ScreenRegion


def test_fake_ocr_extracts_configured_text() -> None:
    region = ScreenRegion(left=4, top=8, width=120, height=64)
    image = FakeCaptureService(image_data=b"fixture").capture_region(region)

    result = FakeOcrService(text="screen text", confidence=0.95).extract_text(image)

    assert image.region == region
    assert image.data == b"fixture"
    assert result.text == "screen text"
    assert result.confidence == 0.95


def test_fake_ocr_can_fail_once() -> None:
    image = FakeCaptureService().capture_region(ScreenRegion(0, 0, 10, 10))
    service = FakeOcrService(text="after failure")
    service.fail_next()

    with pytest.raises(OcrError):
        service.extract_text(image)

    assert service.extract_text(image).text == "after failure"


def test_screen_region_requires_positive_size() -> None:
    with pytest.raises(ValueError):
        ScreenRegion(left=0, top=0, width=0, height=10)
