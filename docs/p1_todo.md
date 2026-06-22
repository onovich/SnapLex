# P1 TODO

P1 goal: build the core non-UI translation pipeline that clipboard and OCR flows will reuse.

Executable guide: `docs/p1_core_pipeline_goal_guide.md`

Status: complete. See `docs/p1_final_validation_report.md`.

## Tasks

1. Done - Expand text normalization for repeated whitespace, empty input, and language-safe line handling.
2. Done - Add provider error models for empty input, provider failure, timeout, unsupported language, stale result, and fallback exhaustion.
3. Done - Add provider registry and config-driven provider selection.
4. Done - Add deterministic fake providers for fallback and failure-order tests.
5. Done - Add translation cache keying and an in-memory cache.
6. Done - Add translation pipeline orchestration around normalization, provider selection, cache, fallback, and error mapping.
7. Done - Add async-friendly boundaries so later PySide6 calls do not block the UI thread.
8. Done - Add tests for cache hits, fallback order, provider errors, timeouts, and config defaults.
9. Done - Update README and handoff docs.

## P2 Entry

Use `docs/p1_to_p2_handoff.md` before starting P2.

## Deferred Until Later Phases

- Clipboard hotkeys and popup UI belong to P2.
- Screen capture, region overlay, and OCR adapters belong to P3.
- Real LibreTranslate, OpenAI, or DeepL network adapters belong to P4.
- Persistent history and settings UI belong to P5.
