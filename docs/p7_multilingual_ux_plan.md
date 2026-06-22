# P7 Multilingual UX And Localization Plan

Date: 2026-06-22
Phase: P7 Expansion Track
Status: design plan

This document defines how SnapLex should approach multilingual UX after the
Windows MVP release baseline. It is a product and architecture plan only; P7
does not implement a broad i18n layer.

## Goals

- Make the desktop utility understandable for users who work across multiple
  languages.
- Separate UI locale from translation source/target language settings.
- Preserve deterministic fake-provider smoke and existing app bootstrap.
- Keep provider language support and OCR language hints behind service/config
  boundaries.
- Avoid turning localized copy into business logic inside PySide6 widgets.

## Non-Goals

- No runtime i18n framework in P7.
- No new mandatory dependency for locale catalogs, ICU, CLDR, or provider
  language packs.
- No broad UI redesign.
- No automatic OCR language detection implementation.
- No provider API changes or real network validation.

## Concepts

`ui_locale`

: The locale used for app labels, buttons, statuses, and help text.

`translation_source_lang`

: The language passed to `TranslationPipeline` as source language, usually
  `auto`.

`translation_target_lang`

: The target translation language stored in `AppConfig.target_lang`.

`ocr_language_hint`

: A future optional hint passed to an OCR service implementation. It must not
  be required by fake OCR or by app bootstrap.

`provider_language_support`

: Provider-specific supported language metadata, resolved through provider
  capability/config boundaries rather than UI assumptions.

## UX Model

The user should be able to adjust three separate choices:

- App language: controls visible UI copy.
- Translation pair: controls source/target language defaults.
- OCR hint: improves future real OCR selection when available.

These choices may share labels but should not share storage fields. A user can
run the UI in Simplified Chinese while translating Japanese to English and
hinting OCR toward Japanese.

## Visible Copy Boundaries

Future localized copy should be grouped by stable message ids rather than
hard-coded strings in widgets. Suggested groups:

- Shell actions: `translate_clipboard`, `translate_screen`, `settings`,
  `history`.
- Result states: idle, loading, success, empty clipboard, empty OCR, provider
  failure, timeout, unsupported language, stale result.
- Settings fields: source, target, provider, fallback order, history,
  provider URLs, API key environment variable names.
- History actions: copy, delete, clear, close.
- Packaging/release smoke text can remain English unless a release-specific
  localization requirement appears.

Widget code may render localized strings, but it should not decide provider
support, OCR behavior, history retention, or settings migration.

## Locale Selection

Recommended first locales:

- `en-US`: default development and release smoke locale.
- `zh-CN`: primary Simplified Chinese app locale.
- `ja-JP`: useful for OCR/translation workflows in the target user set.

Future storage field:

```text
ui_preferences["ui_locale"] = "en-US"
```

Storage notes:

- Missing or unsupported locales fall back to `en-US`.
- Locale selection should be optional and should not change translation source
  or target defaults by itself.
- Migration should tolerate older configs without `ui_locale`.
- No locale should store provider secrets or local user text.

## Language-Pair Defaults

Existing `AppConfig.source_lang` and `AppConfig.target_lang` remain the source
of truth for translation defaults.

Future UX requirements:

- Show source and target language labels using the active UI locale.
- Keep provider language codes visible for troubleshooting when needed.
- If a provider does not support a selected pair, show a provider support error
  from service/provider state, not from hard-coded UI tables.
- Retain fake provider behavior for deterministic tests.

## OCR Language Hints

OCR language hints are future optional settings. They should live in app config
or a dedicated OCR config model, not in UI widget state.

Future shape:

```text
ocr_language_hints = ("en", "zh", "ja")
```

Boundary requirements:

- `FakeOcrService` should continue to work without hints.
- `PaddleOcrService` may map hints to PaddleOCR parameters in a later phase.
- Missing hint support must produce a documented fallback, not a launch failure.
- Hints must not trigger model downloads during app bootstrap or no-GUI mode.

## Provider Support Messaging

Provider support should come from provider capabilities or provider errors.

Future messaging examples:

- Unsupported pair: provider rejected source/target language pair.
- Missing credentials: provider requires an API key environment variable.
- Fallback used: provider failed and the next configured provider succeeded.
- Offline mode: fake provider is active for local smoke.

These messages should remain separate from translation response data. History
entries should store provider and language metadata, but not UI-localized
status text.

## Fallback And Empty States

Localized fallback states must cover:

- Empty clipboard.
- Empty OCR result.
- Unsupported language pair.
- Provider timeout.
- Provider failure.
- Fallback exhausted.
- Stale result.
- Missing optional OCR/capture dependency.
- Settings save failure.
- History disabled or empty.

The same error semantics should be available to tests without PySide6.

## Testing Strategy

When implementation is approved later:

- Unit-test message lookup fallback without PySide6.
- Unit-test `ui_locale` default and migration behavior.
- Unit-test language-pair display mapping separately from provider execution.
- Keep fake provider and fake OCR tests deterministic.
- Keep network provider tests mocked.
- Run `python -m snaplex --no-gui` to prove localization does not affect
  bootstrap.
- Run packaged `--smoke-package` to prove release smoke remains stable.

## Rollout Plan

1. Add a small locale catalog boundary with English defaults.
2. Add settings storage for `ui_locale`.
3. Localize shell/result/settings/history strings.
4. Add localized provider support messages from existing error types.
5. Add optional OCR hint config only after the OCR service contract is ready.
6. Re-run package smoke and update release docs.

## Open Decisions

- Whether initial localized UI copy should include only English and Simplified
  Chinese or include Japanese at the first implementation pass.
- Whether locale catalogs should be plain Python dictionaries, JSON files, or a
  standard localization library.
- Whether OCR language hints belong in the existing `AppConfig` or a future
  `OcrConfig`.
- Whether history should display original provider language codes, localized
  language names, or both.
