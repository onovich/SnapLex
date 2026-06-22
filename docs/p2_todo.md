# P2 TODO

P2 goal: build the clipboard translation MVP on top of the accepted P1 translation pipeline.

Status: implementation complete, ready for validation.

Executable guide: `docs/p2_clipboard_translation_goal_guide.md`

## Tasks

- [x] Add clipboard translation state/presenter boundary.
- [x] Add floating widget action for clipboard translation.
- [x] Add result popup or result view with loading, success, empty, error, retry, copy, and close states.
- [x] Add concrete desktop clipboard service or Qt clipboard adapter plus fake clipboard tests.
- [x] Wire clipboard text into `TranslationPipeline.translate_text_async(...)`.
- [x] Add UI-friendly error mapping for fallback exhaustion, timeout, unknown provider, unsupported language, stale result, and generic provider failure.
- [x] Investigate Windows hotkey support and defer because global hotkeys are not stable enough for P2.
- [x] Update Windows smoke checklist and README with clipboard MVP usage.
- [x] Create P2 final validation report and P2-to-P3 handoff.

## Deferred Until Later Phases

- Screen capture, region overlay, and OCR adapters belong to P3.
- Real LibreTranslate, OpenAI, or DeepL network adapters belong to P4.
- Persistent history and settings UI belong to P5.
- PyInstaller packaging belongs to P6.
