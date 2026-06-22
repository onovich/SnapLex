"""Screen translation presentation flow."""

from __future__ import annotations

from collections.abc import Callable

from snaplex.services import CaptureError, CaptureService, OcrService, ScreenRegion
from snaplex.ui.translation_result import (
    TranslationPipelineLike,
    TranslationResultPresenter,
    TranslationResultState,
    TranslationResultStatus,
)

ScreenTranslationStatus = TranslationResultStatus
ScreenTranslationState = TranslationResultState


class ScreenTranslationPresenter(TranslationResultPresenter):
    def __init__(
        self,
        on_translate_requested: Callable[[], None] | None = None,
        on_copy_result: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__(
            loading_status_text="Translating screen...",
            on_translate_requested=on_translate_requested,
            on_copy_result=on_copy_result,
        )
        self._last_region: ScreenRegion | None = None

    def request_screen_translation(
        self,
        *,
        source_text: str = "",
    ) -> ScreenTranslationState:
        return self.request_translation(source_text=source_text)

    async def translate_region(
        self,
        *,
        region: ScreenRegion,
        capture_service: CaptureService,
        ocr_service: OcrService,
        pipeline: TranslationPipelineLike,
    ) -> ScreenTranslationState:
        self._last_region = region
        self.request_screen_translation()
        try:
            captured_image = capture_service.capture_region(region)
        except CaptureError:
            return self.show_error("Could not capture the selected screen region. Try again.")

        ocr_result = ocr_service.extract_text(captured_image)
        return await self.translate_source_text(source_text=ocr_result.text, pipeline=pipeline)

    async def translate_region_from_points(
        self,
        *,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        capture_service: CaptureService,
        ocr_service: OcrService,
        pipeline: TranslationPipelineLike,
    ) -> ScreenTranslationState:
        try:
            region = ScreenRegion.from_points(start_x, start_y, end_x, end_y)
        except ValueError:
            return self.show_error("Select a non-empty screen region.")

        return await self.translate_region(
            region=region,
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )

    async def retry_translation(
        self,
        *,
        capture_service: CaptureService,
        ocr_service: OcrService,
        pipeline: TranslationPipelineLike,
    ) -> ScreenTranslationState:
        if self._last_region is None:
            return self.show_error("Select a screen region before retrying.")

        return await self.translate_region(
            region=self._last_region,
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
