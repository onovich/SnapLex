"""Application service contracts and local implementations."""

from snaplex.services.capture_service import (
    CapturedImage,
    CaptureError,
    CaptureService,
    FakeCaptureService,
    MssCaptureService,
    ScreenRegion,
)
from snaplex.services.clipboard_service import (
    ClipboardError,
    ClipboardService,
    InMemoryClipboardService,
    QtClipboardService,
)
from snaplex.services.ocr_service import FakeOcrService, OcrError, OcrResult, OcrService
from snaplex.services.text import normalize_text
from snaplex.services.translation_cache import (
    InMemoryTranslationCache,
    TranslationCache,
    TranslationCacheKey,
)
from snaplex.services.translation_service import (
    TranslationPipeline,
    TranslationService,
    create_default_translation_pipeline,
)

__all__ = [
    "CapturedImage",
    "CaptureError",
    "CaptureService",
    "ClipboardError",
    "ClipboardService",
    "FakeCaptureService",
    "FakeOcrService",
    "InMemoryClipboardService",
    "InMemoryTranslationCache",
    "MssCaptureService",
    "OcrError",
    "OcrResult",
    "OcrService",
    "QtClipboardService",
    "ScreenRegion",
    "TranslationCache",
    "TranslationCacheKey",
    "TranslationPipeline",
    "TranslationService",
    "create_default_translation_pipeline",
    "normalize_text",
]
