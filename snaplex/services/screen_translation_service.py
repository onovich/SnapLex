"""Screen capture, OCR, and translation orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from snaplex.providers import TranslationResponse
from snaplex.services.capture_service import CaptureService, ScreenRegion
from snaplex.services.ocr_service import OcrService


class TranslationPipelineLike(Protocol):
    async def translate_text_async(self, text: str) -> TranslationResponse:
        """Translate text using the P1 pipeline async boundary."""
        ...


@dataclass(frozen=True)
class ScreenTranslationResponse:
    region: ScreenRegion
    source_text: str
    translated_text: str
    provider_name: str
    source_lang: str
    target_lang: str
    ocr_confidence: float | None = None


class ScreenTranslationService:
    def __init__(
        self,
        *,
        capture_service: CaptureService,
        ocr_service: OcrService,
        pipeline: TranslationPipelineLike,
    ) -> None:
        self._capture_service = capture_service
        self._ocr_service = ocr_service
        self._pipeline = pipeline

    async def translate_region(self, region: ScreenRegion) -> ScreenTranslationResponse:
        captured_image = self._capture_service.capture_region(region)
        ocr_result = self._ocr_service.extract_text(captured_image)
        translation_response = await self._pipeline.translate_text_async(ocr_result.text)
        return ScreenTranslationResponse(
            region=region,
            source_text=ocr_result.text,
            translated_text=translation_response.translated_text,
            provider_name=translation_response.provider_name,
            source_lang=translation_response.source_lang,
            target_lang=translation_response.target_lang,
            ocr_confidence=ocr_result.confidence,
        )
