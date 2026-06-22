"""Screen translation presentation flow."""

from __future__ import annotations

from collections.abc import Callable

from snaplex.errors import TranslationError
from snaplex.services import (
    CaptureError,
    CaptureService,
    OcrError,
    OcrService,
    OcrUnavailableError,
    ScreenRegion,
    ScreenTranslationService,
)
from snaplex.ui.translation_result import (
    TranslationPipelineLike,
    TranslationResultPresenter,
    TranslationResultState,
    TranslationResultStatus,
    friendly_translation_error_message,
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

    def show_selection_cancelled(self) -> ScreenTranslationState:
        self._state = ScreenTranslationState(
            status=ScreenTranslationStatus.CANCELLED,
            status_text="Screen selection cancelled",
            error_message="Select a region to translate.",
            can_retry=True,
        )
        return self._state

    def show_empty_ocr_result(self) -> ScreenTranslationState:
        return self.show_empty(
            status_text="No screen text found",
            message="No text was detected in the selected region.",
        )

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
        screen_translation_service = ScreenTranslationService(
            capture_service=capture_service,
            ocr_service=ocr_service,
            pipeline=pipeline,
        )
        try:
            response = await screen_translation_service.translate_region(region)
        except CaptureError:
            return self.show_error("Could not capture the selected screen region. Try again.")
        except OcrUnavailableError:
            return self.show_error("OCR is unavailable. Install OCR support or use fake OCR mode.")
        except OcrError:
            return self.show_error("OCR failed to read text from the selected region. Try again.")
        except TranslationError as exc:
            return self.show_error(friendly_translation_error_message(exc))
        except Exception:
            return self.show_error("Screen translation failed unexpectedly. Try again.")

        if not response.source_text.strip():
            return self.show_empty_ocr_result()

        return self.show_success(
            source_text=response.source_text,
            translated_text=response.translated_text,
            provider_name=response.provider_name,
        )

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
