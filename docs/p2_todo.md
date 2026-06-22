# P2 TODO

P2 goal: build the clipboard translation MVP on top of the accepted P1 translation pipeline.

Executable guide: `docs/p2_clipboard_translation_goal_guide.md`

## Tasks

1. Add clipboard translation state/presenter boundary.
2. Add floating widget action for clipboard translation.
3. Add result popup or result view with loading, success, empty, error, retry, copy, and close states.
4. Add concrete desktop clipboard service or Qt clipboard adapter plus fake clipboard tests.
5. Wire clipboard text into `TranslationPipeline.translate_text_async(...)`.
6. Add UI-friendly error mapping for fallback exhaustion, timeout, unknown provider, unsupported language, stale result, and generic provider failure.
7. Investigate Windows hotkey support and implement only if stable inside P2.
8. Update Windows smoke checklist and README with clipboard MVP usage.
9. Create P2 final validation report and P2-to-P3 handoff.

## Deferred Until Later Phases

- Screen capture, region overlay, and OCR adapters belong to P3.
- Real LibreTranslate, OpenAI, or DeepL network adapters belong to P4.
- Persistent history and settings UI belong to P5.
- PyInstaller packaging belongs to P6.

