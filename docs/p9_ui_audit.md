# P9 UI Audit

Date: 2026-07-15
Phase: P9 Apple-Inspired UI/UX Polish
Status: Round 1 current-state audit

P9 starts from the planner-accepted P8 baseline at
`d8d451a0c2efc140032737ec2afbbbdb2a4f704c`. The goal is product-quality polish
for the existing PySide6 utility, not feature expansion.

## Baseline Validation

Round 1 revalidated the accepted baseline before UI changes:

- `Validate.cmd`: PASS with 213 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: `SnapLex bootstrap OK (PySide6 available).`
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- Offscreen baseline screenshot: PASS, written locally to
  `snaplex-smoke-data\p9-screenshots\round1-main-shell-baseline.png`.

Screenshot artifacts are local smoke output and must remain ignored/untracked.

## Main Shell Findings

- The first screen is already the usable tool, with clipboard and screen
  translation actions visible immediately.
- Primary and secondary actions are visually separated, but all four top
  buttons use similar size and placement. The primary path needs stronger
  action hierarchy and predictable tab order.
- The title, subtitle, result group, and status are present, but the status is
  visually quiet and disconnected from the current result state.
- The current offscreen baseline screenshot renders visible text as square
  glyphs in this environment. P9 should set an explicit native font preference
  and make screenshot smoke catch text rendering regressions.
- Current button labels are text-only. Icons are optional later, but any
  icon-only control must include accessible names and tooltips.

## Result State Findings

- Result state is driven by `TranslationResultState`, which is the right
  presentation boundary to preserve.
- Source and translation labels are selectable, but they are fixed labels rather
  than scrollable text regions. Long OCR or translation text can make the
  window grow or crowd actions.
- Provider identity, fake warning, and error messaging exist. P9 should refine
  visual hierarchy so fake warning and errors remain clear without competing
  with translated text.
- Empty, loading, cancelled, retryable, provider-failure, timeout, unsupported
  language, and stale states are covered in presenters, but screenshot smoke
  does not yet exercise representative rendered states.

## Settings Findings

- Settings exposes provider selection, provider order, source/target language,
  readiness, details, env var presence, `Test Connection`, disabled
  `Connect account (future)`, provider-specific fields, and history controls.
- The dialog is functional but dense. It uses stacked groups for every provider,
  so scan speed is low and keyboard traversal is long.
- Readiness and connection result labels are text-only. They should become
  clearer semantic status rows without exposing secret values.
- Accessibility metadata, tooltips, default buttons, and tab order are not yet
  explicit.
- Provider setup is correctly routed through `SettingsPresenter` /
  `SettingsService`; P9 must keep widgets as render/wiring clients.

## History Findings

- History dialog supports status, list, copy, delete, clear, and close.
- Empty and disabled states are only status text above an empty list. They need
  clearer copy and stable disabled button behavior.
- Long entries are flattened into one list string, which hurts scanning and can
  overflow horizontally.
- Keyboard operation exists through native controls, but focus order,
  accessible names, and button enablement should be made explicit.

## Region Selector And Screen Flow Findings

- Region selection has a simple full-screen overlay with a rubber band and
  `Esc` cancel path.
- The overlay interaction is intentionally minimal. P9 should improve smoke
  notes and feedback expectations without rewriting capture geometry,
  multi-monitor behavior, or OCR/capture services.
- Screen result handoff already shares the same result view, so result polish
  benefits both clipboard and screen workflows.

## Screenshot Smoke Target States

P9 screenshot-backed smoke should render these deterministic states:

- Main shell idle.
- Loading state.
- Success state with a real-provider name.
- Fake success state with fake warning.
- Provider/error state.
- Long source and long translation text at a constrained small window size.
- Settings provider setup with readiness.
- Settings connection result.
- History empty state.
- History list state with a long entry.

The smoke should verify nonblank images, basic dimensions, expected visible
widgets/text, and local artifact placement under an ignored path such as
`snaplex-smoke-data\p9-screenshots`.

## Non-Scope Boundaries

P9 must not introduce SnapLex Cloud, account OAuth, keychain integration,
browser extension runtime, AI summary runtime, global hotkeys, provider
rewrites, OCR/capture rewrites, real network validation, or committed generated
screenshots/package outputs.

## Round 1 Conclusion

The P8 baseline is stable and ready for P9 UI polish. Highest-priority P9
targets are shared visual tokens, explicit font/focus treatment, scrollable
result regions, Settings information architecture, History long-entry behavior,
and screenshot smoke that catches the text-rendering issue seen in the baseline
offscreen screenshot.
