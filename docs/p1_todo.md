# P1 TODO

P1 goal: build the core non-UI translation pipeline that clipboard and OCR flows will reuse.

## Tasks

1. Expand text normalization for repeated whitespace, empty input, and language-safe line handling.
2. Add provider error models for empty input, provider failure, timeout, unsupported language, stale result, and fallback exhaustion.
3. Add provider registry and config-driven provider selection.
4. Add deterministic fake providers for fallback and failure-order tests.
5. Add translation cache keying and an in-memory cache.
6. Add translation pipeline orchestration around normalization, provider selection, cache, fallback, and error mapping.
7. Add async-friendly boundaries so later PySide6 calls do not block the UI thread.
8. Add tests for cache hits, fallback order, provider errors, timeouts, and config defaults.
9. Update README and workflow docs with any new stable commands.

## Deferred Until Later Phases

- Clipboard hotkeys and popup UI belong to P2.
- Screen capture, region overlay, and OCR adapters belong to P3.
- Real LibreTranslate, OpenAI, or DeepL network adapters belong to P4.
- Persistent history and settings UI belong to P5.
