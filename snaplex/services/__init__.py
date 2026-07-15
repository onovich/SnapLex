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
from snaplex.services.ocr_service import (
    FakeOcrScenario,
    FakeOcrService,
    OcrError,
    OcrResult,
    OcrService,
    OcrUnavailableError,
    PaddleOcrService,
)
from snaplex.services.provider_setup import (
    ProviderConnectionTestResult,
    ProviderSetupState,
    ProviderSetupStatus,
    describe_provider_setup,
    describe_provider_setups,
    test_provider_connection,
)
from snaplex.services.screen_translation_service import (
    ScreenTranslationResponse,
    ScreenTranslationService,
)
from snaplex.services.history_service import HistoryService
from snaplex.services.settings_service import SettingsService
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
    "FakeOcrScenario",
    "FakeOcrService",
    "HistoryService",
    "InMemoryClipboardService",
    "InMemoryTranslationCache",
    "MssCaptureService",
    "OcrError",
    "OcrResult",
    "OcrService",
    "OcrUnavailableError",
    "PaddleOcrService",
    "ProviderConnectionTestResult",
    "ProviderSetupState",
    "ProviderSetupStatus",
    "QtClipboardService",
    "ScreenRegion",
    "ScreenTranslationResponse",
    "ScreenTranslationService",
    "SettingsService",
    "TranslationCache",
    "TranslationCacheKey",
    "TranslationPipeline",
    "TranslationService",
    "create_default_translation_pipeline",
    "describe_provider_setup",
    "describe_provider_setups",
    "normalize_text",
    "test_provider_connection",
]
