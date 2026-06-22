"""OCR service contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from snaplex.services.capture_service import CapturedImage


class OcrError(RuntimeError):
    """Raised when OCR extraction fails."""


@dataclass(frozen=True)
class OcrResult:
    text: str
    confidence: float | None = None


class OcrService(Protocol):
    def extract_text(self, image: CapturedImage) -> OcrResult:
        """Extract text from a captured image."""
        ...


class FakeOcrService:
    def __init__(self, text: str = "Example screen text", confidence: float | None = 1.0) -> None:
        self._text = text
        self._confidence = confidence
        self._fail = False

    def fail_next(self) -> None:
        self._fail = True

    def extract_text(self, image: CapturedImage) -> OcrResult:
        if self._fail:
            self._fail = False
            raise OcrError("Fake OCR service was configured to fail.")

        return OcrResult(text=self._text, confidence=self._confidence)
