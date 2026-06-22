import pytest

from snaplex.services import (
    CapturedImage,
    FakeCaptureService,
    FakeOcrScenario,
    FakeOcrService,
    OcrError,
    OcrUnavailableError,
    PaddleOcrService,
    ScreenRegion,
)
from snaplex.services.ocr_service import _load_paddle_ocr_factory


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


def test_fake_ocr_can_return_empty_result() -> None:
    image = FakeCaptureService().capture_region(ScreenRegion(0, 0, 10, 10))

    result = FakeOcrService(text="ignored", scenario=FakeOcrScenario.EMPTY).extract_text(image)

    assert result.text == ""
    assert result.confidence == 1.0


def test_fake_ocr_failure_scenario_always_fails() -> None:
    image = FakeCaptureService().capture_region(ScreenRegion(0, 0, 10, 10))
    service = FakeOcrService(scenario=FakeOcrScenario.FAILURE)

    with pytest.raises(OcrError):
        service.extract_text(image)

    with pytest.raises(OcrError):
        service.extract_text(image)


def test_screen_region_requires_positive_size() -> None:
    with pytest.raises(ValueError):
        ScreenRegion(left=0, top=0, width=0, height=10)


def test_paddle_ocr_service_lazy_initializes_and_parses_results() -> None:
    created: list[str] = []

    class FakePaddleEngine:
        def __init__(self) -> None:
            self.paths: list[str] = []

        def ocr(self, path: str):
            self.paths.append(path)
            return [[[None, ("first line", 0.9)], [None, ("second line", 0.7)]]]

    engine = FakePaddleEngine()

    def factory() -> FakePaddleEngine:
        created.append("created")
        return engine

    service = PaddleOcrService(ocr_factory=factory)
    image = CapturedImage(region=ScreenRegion(0, 0, 10, 10), data=b"png")

    assert created == []

    result = service.extract_text(image)

    assert created == ["created"]
    assert result.text == "first line\nsecond line"
    assert result.confidence == pytest.approx(0.8)
    assert len(engine.paths) == 1


def test_paddle_ocr_service_maps_initialization_failure() -> None:
    def factory():
        raise RuntimeError("model unavailable")

    service = PaddleOcrService(ocr_factory=factory)
    image = CapturedImage(region=ScreenRegion(0, 0, 10, 10), data=b"png")

    with pytest.raises(OcrUnavailableError, match="could not be initialized"):
        service.extract_text(image)


def test_paddle_ocr_dependency_loader_maps_missing_dependency() -> None:
    def missing_import(module_name: str):
        raise ModuleNotFoundError(module_name)

    with pytest.raises(OcrUnavailableError, match="PaddleOCR is required"):
        _load_paddle_ocr_factory(import_module=missing_import)
