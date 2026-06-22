# P7 AI Summary Capability Design

Date: 2026-06-22
Phase: P7 Expansion Track
Status: design plan

This document designs AI summary as a future optional capability. It must remain
separate from the accepted translation pipeline and must not add real AI
network calls in P7.

## Goals

- Summarize selected, clipboard, OCR, or browser-origin text after translation
  or as a standalone action.
- Keep summary semantics behind a dedicated service/provider boundary.
- Reuse existing provider configuration patterns without merging summary into
  `TranslationProvider`.
- Keep tests deterministic and no-network.
- Keep summary text out of history unless the user explicitly enables future
  summary persistence.

## Non-Goals

- No real AI provider integration in P7.
- No OpenAI, DeepL, or LibreTranslate contract changes.
- No prompt templates that include real provider keys or user secrets.
- No cloud sync, accounts, keychain integration, or remote history.
- No mandatory dependency or package change.

## Proposed Boundaries

Future modules may look like this:

```text
snaplex/summary/
  base.py              # SummaryProvider protocol and request/response models
  fake.py              # deterministic local fake for tests and smoke
  registry.py          # config-driven provider lookup

snaplex/services/
  summary_service.py   # SummaryService orchestration boundary
```

`SummaryService` is the application boundary. UI code may call it, but UI code
must not own prompt construction, provider fallback, privacy policy, or history
rules.

`SummaryProvider` is separate from `TranslationProvider`. A translation provider
may share HTTP transport utilities with a future summary provider, but the
capability contracts remain distinct.

## Request Shape

Future request model:

```python
SummaryRequest(
    text: str,
    source_lang: str | None,
    target_lang: str | None,
    mode: Literal["short", "bullets", "action_items"],
    max_length: int | None,
    context: SummaryContext,
)
```

`SummaryContext` may include:

- `flow`: `clipboard`, `screen`, `browser`, or `manual`.
- `source_kind`: `original_text`, `translated_text`, or `combined`.
- `provider_name`: optional translation provider used before summary.
- `allow_persistence`: explicit user preference for future summary history.

The request must not include provider API key values.

## Response Shape

Future response model:

```python
SummaryResponse(
    summary_text: str,
    provider_name: str,
    mode: str,
    source_lang: str | None,
    target_lang: str | None,
    token_count_estimate: int | None,
    warnings: tuple[str, ...],
)
```

Warnings may include:

- Text was truncated before summary.
- Language was inferred by provider.
- Provider returned a partial result.
- Summary is unavailable offline.

## Failure States

Summary failures should map to UI states without leaking provider internals:

- Empty input.
- Text too long.
- Unsupported language.
- Missing credentials.
- Provider timeout.
- Provider failure.
- Fallback exhausted.
- Unsafe or privacy-restricted input.
- Stale result.

The existing error taxonomy can inspire future summary errors, but summary
should define its own capability-specific exceptions where needed.

## Privacy Rules

Summary text can be more sensitive than translation text because it may combine
or condense multiple inputs. Future summary implementation must follow these
rules:

- Do not send text to a network provider unless the selected summary provider
  requires it and the user has configured that provider.
- Do not persist summary inputs or outputs by default.
- Do not store provider API key values in config, history, logs, docs, tests, or
  package resources.
- Do not include screenshots or OCR image bytes in summary requests.
- If browser-origin text is summarized, record origin metadata only when the
  user explicitly enables it.
- Redaction, if added later, belongs in a service boundary before provider
  calls, not in UI widgets.

## Settings Needs

Future settings should be separate from translation settings:

```text
summary_enabled = false
summary_provider_name = "fake"
summary_provider_order = ("fake",)
summary_default_mode = "short"
summary_max_length = 500
summary_persist_history = false
```

Provider secret handling should mirror P4/P5:

- Store env var names only.
- Read actual secrets from environment at request time.
- Tests use fake or mocked transports.

## History Interaction

Summary history should not reuse translation history entries without a schema
decision. Future options:

- Separate summary history store.
- Extend history entry type with `entry_kind`.
- Store summaries only as metadata attached to a translation entry.

Recommended first implementation: separate summary history store disabled by
default. This avoids changing accepted translation history behavior.

## UI Interaction Model

Potential entry points:

- `Summarize Clipboard`: standalone summary of clipboard text.
- `Summarize Result`: summarize translated text in the result view.
- `Summarize Screen Text`: summarize OCR text before or after translation.
- `Summarize Browser Selection`: future browser bridge handoff.

UI requirements:

- Show loading, success, failure, and retry states.
- Show whether the summary used original text, translated text, or both.
- Never imply offline summary when a network provider is selected.
- Keep copy result separate from translation copy result.

## No-Network Test Strategy

Initial implementation tests should cover:

- Fake summary provider success.
- Empty input.
- Text too long.
- Missing provider.
- Provider failure and timeout.
- Fallback order.
- History disabled by default.
- Config stores env var names, not secrets.
- UI presenter states without PySide6.
- App bootstrap and `--no-gui` remain unchanged.
- Packaged `--smoke-package` remains unchanged.

Mocked HTTP tests may be added only when a real summary provider adapter is
implemented in a later phase.

## Packaging Impact

P7 adds no packaging impact. Later implementation must prove:

- `python -m snaplex --no-gui` still works without summary dependencies.
- `python scripts\package_windows.py --variant base` still builds.
- Packaged `SnapLex.exe --smoke-package` still passes.
- Optional summary provider dependencies are not mandatory in the base package.

## Rollout Plan

1. Add pure summary models and fake provider.
2. Add `SummaryService` with deterministic tests.
3. Add summary config fields disabled by default.
4. Add presenter-level states without PySide6 dependency.
5. Add optional UI entry point after service tests pass.
6. Add real provider adapter only after planner approval and mocked HTTP tests.

## Open Decisions

- Whether summary should operate on original text, translated text, or both by
  default.
- Whether summary history should be separate from translation history.
- Which real provider should be first, if any.
- Whether summary should support action-item extraction as a first-class mode.
- Whether browser-origin summaries require an additional confirmation step.
