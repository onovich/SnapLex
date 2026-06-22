"""Application service contracts and local implementations."""

from snaplex.services.capture_service import (
    CapturedImage,
    CaptureError,
    CaptureService,
    FakeCaptureService,
    ScreenRegion,
)
from snaplex.services.clipboard_service import ClipboardError, ClipboardService, InMemoryClipboardService
from snaplex.services.ocr_service import FakeOcrService, OcrError, OcrResult, OcrService
from snaplex.services.text import normalize_text
from snaplex.services.translation_service import TranslationService

__all__ = [
    "CapturedImage",
    "CaptureError",
    "CaptureService",
    "ClipboardError",
    "ClipboardService",
    "FakeCaptureService",
    "FakeOcrService",
    "InMemoryClipboardService",
    "OcrError",
    "OcrResult",
    "OcrService",
    "ScreenRegion",
    "TranslationService",
    "normalize_text",
]
