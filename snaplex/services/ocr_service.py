"""OCR service contracts."""

from __future__ import annotations

import importlib
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Protocol

from snaplex.services.capture_service import CapturedImage


class OcrError(RuntimeError):
    """Raised when OCR extraction fails."""


class OcrUnavailableError(OcrError):
    """Raised when an optional OCR backend is unavailable."""


@dataclass(frozen=True)
class OcrResult:
    text: str
    confidence: float | None = None


class OcrService(Protocol):
    def extract_text(self, image: CapturedImage) -> OcrResult:
        """Extract text from a captured image."""
        ...


class FakeOcrScenario(str, Enum):
    SUCCESS = "success"
    EMPTY = "empty"
    FAILURE = "failure"


class FakeOcrService:
    def __init__(
        self,
        text: str = "Example screen text",
        confidence: float | None = 1.0,
        scenario: FakeOcrScenario = FakeOcrScenario.SUCCESS,
    ) -> None:
        self._text = text
        self._confidence = confidence
        self._scenario = scenario
        self._fail = False

    def fail_next(self) -> None:
        self._fail = True

    def extract_text(self, image: CapturedImage) -> OcrResult:
        if self._fail or self._scenario == FakeOcrScenario.FAILURE:
            self._fail = False
            raise OcrError("Fake OCR service was configured to fail.")

        if self._scenario == FakeOcrScenario.EMPTY:
            return OcrResult(text="", confidence=self._confidence)

        return OcrResult(text=self._text, confidence=self._confidence)


class PaddleOcrService:
    def __init__(self, ocr_factory: Any) -> None:
        self._ocr_factory = ocr_factory
        self._engine: Any | None = None

    @classmethod
    def from_optional_dependency(cls) -> "PaddleOcrService":
        ocr_factory = _load_paddle_ocr_factory()
        return cls(ocr_factory=ocr_factory)

    def extract_text(self, image: CapturedImage) -> OcrResult:
        engine = self._get_engine()
        temp_path = _write_temp_image(image)
        try:
            raw_result = engine.ocr(str(temp_path))
        except Exception as exc:
            raise OcrError("PaddleOCR failed to extract text.") from exc
        finally:
            temp_path.unlink(missing_ok=True)

        return _parse_paddle_result(raw_result)

    def _get_engine(self) -> Any:
        if self._engine is None:
            try:
                self._engine = self._ocr_factory()
            except Exception as exc:
                raise OcrUnavailableError("PaddleOCR could not be initialized.") from exc

        return self._engine


def _load_paddle_ocr_factory(import_module: Any = importlib.import_module) -> Any:
    try:
        paddleocr_module = import_module("paddleocr")
    except ModuleNotFoundError as exc:
        raise OcrUnavailableError(
            "PaddleOCR is required for real OCR. Install with `python -m pip install -e .[ocr]`."
        ) from exc

    return paddleocr_module.PaddleOCR


def _write_temp_image(image: CapturedImage) -> Path:
    suffix = f".{image.image_format.lstrip('.') or 'png'}"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as image_file:
        image_file.write(image.data)
        return Path(image_file.name)


def _parse_paddle_result(raw_result: Any) -> OcrResult:
    matches = list(_iter_paddle_matches(raw_result))
    if not matches:
        return OcrResult(text="", confidence=None)

    text = "\n".join(match_text for match_text, _confidence in matches if match_text)
    confidences = [confidence for _match_text, confidence in matches if confidence is not None]
    confidence = sum(confidences) / len(confidences) if confidences else None
    return OcrResult(text=text, confidence=confidence)


def _iter_paddle_matches(raw_result: Any):
    if isinstance(raw_result, tuple) and len(raw_result) == 2:
        text, confidence = raw_result
        if isinstance(text, str):
            yield text, float(confidence) if isinstance(confidence, (int, float)) else None
            return

    if isinstance(raw_result, (list, tuple)):
        for item in raw_result:
            yield from _iter_paddle_matches(item)
