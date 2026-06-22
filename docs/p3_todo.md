# P3 TODO

P3 goal: build the screen capture and OCR MVP on top of the accepted P1 translation pipeline and P2 result-flow pattern.

Status: implementation complete, planner-accepted.

Executable guide: `docs/p3_screen_capture_ocr_goal_guide.md`

## Tasks

- [x] Add screen translation shell action and presenter/service skeleton.
- [x] Strengthen capture geometry and fake capture integration tests.
- [x] Add region selection overlay with confirm and cancel behavior.
- [x] Add screenshot backend behind `CaptureService`.
- [x] Add OCR service adapter boundary, fake OCR scenarios, and optional lazy PaddleOCR adapter.
- [x] Wire capture -> OCR -> `TranslationPipeline.translate_text_async(...)` -> result view.
- [x] Add user-friendly states for cancel, invalid region, capture failure, OCR failure, empty OCR result, retry, copy, and close.
- [x] Verify OCR lazy loading and missing dependency/model behavior.
- [x] Record Windows smoke evidence for capture/OCR flow and DPI/multi-monitor limitations.
- [x] Create P3 final validation report and P3-to-P4 handoff.

## Deferred Until Later Phases

- Real LibreTranslate, OpenAI, or DeepL network adapters belong to P4.
- Persistent history and settings UI belong to P5.
- PyInstaller packaging belongs to P6.
- Browser extension, AI summary, and post-MVP expansion belong to P7.
