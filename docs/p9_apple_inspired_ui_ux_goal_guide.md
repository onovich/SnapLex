# P9 Apple-Inspired UI/UX Polish Goal Mode Guide

Date: 2026-07-15
Status: execution guide for P9 after planner-accepted P8
Estimated budget: 16 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P9 in goal mode:

```text
Execute SnapLex P9 - Apple-Inspired UI/UX Polish in 16 conversation rounds.

Required reading before changes:
- AGENTS.md
- Role.md
- README.md
- TRY.md
- docs/development_plan.md
- docs/phase_plan.md
- docs/p8_final_validation_report.md
- docs/p8_to_p9_handoff.md
- docs/p8_provider_setup_decisions.md
- docs/p8_real_provider_trial_notes.md
- docs/p9_todo.md
- docs/p9_apple_inspired_ui_ux_goal_guide.md
- docs/windows_smoke_checklist.md
- snaplex/ui/app_shell.py
- snaplex/ui/translation_result.py
- snaplex/ui/settings_presenter.py
- snaplex/ui/history_presenter.py
- snaplex/ui/clipboard_presenter.py
- snaplex/ui/screen_presenter.py
- tests/test_settings_presenter.py
- tests/test_settings_service.py
- tests/test_clipboard_presenter.py
- tests/test_screen_presenter.py
- tests/test_history_presenter.py

P8 is planner-accepted. P8 made real-provider setup visible in Settings,
separated fake smoke from real translation, and applied the first UI foundation.

Goal:
Turn the current functional PySide6 shell into a polished, trial-ready desktop
experience inspired by Apple Human Interface Guidelines: clearer hierarchy,
better layout, accessible controls, keyboard/focus quality, robust long-text and
small-window behavior, Settings and History polish, and screenshot-backed GUI
smoke, while preserving P8 provider/setup boundaries and deterministic tests.

Round budget:
- Rounds 1-12: main UI/UX implementation.
- Rounds 13-15: buffer hardening and visual/accessibility fixes.
- Round 16: final validation, report, and P10 handoff.

Rules:
- Keep the first screen as the usable translation tool, not a landing page.
- Use Apple HIG as inspiration for clarity, hierarchy, typography, layout,
  restrained color, accessibility, focus, and direct manipulation; do not clone
  macOS branding or replatform the app.
- Preserve SettingsService, SettingsPresenter, provider registry,
  TranslationPipeline, HistoryService, ClipboardService, CaptureService,
  OcrService, and packaging boundaries.
- UI widgets render presenter/service state and must not own provider,
  credential, translation, history, capture, or OCR business rules.
- Do not introduce SnapLex Cloud, account OAuth, keychain storage, browser
  extension runtime, AI summary runtime, global hotkeys, provider rewrites, or
  capture/OCR rewrites.
- Automated tests and GUI smoke must remain deterministic and no-network.
- Screenshot/smoke artifacts must be written only to ignored/local paths and
  must not be committed.
- Every round must include Debug self-check, architecture self-check,
  validation commands and results, commit hash, push result, next-round target,
  and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to
  the next round.
```

## 1. Required Context

P8 accepted baseline:

- P8 final commit: `d8d451a0c2efc140032737ec2afbbbdb2a4f704c`.
- P8 validation passed with 213 tests.
- Provider setup and `Test Connection` live behind
  `SettingsService` / `SettingsPresenter` / provider registry / provider
  adapters.
- Clipboard and screen translation still execute through `TranslationPipeline`.
- Fake provider is deterministic smoke/dev mode and user-facing fake output is
  labeled as fake.
- Real provider smoke remains optional/manual when local credentials or a
  self-hosted endpoint exist.
- P8 did not implement account OAuth, SnapLex Cloud, keychain integration,
  browser extension runtime, AI summary runtime, global hotkeys, or raw API-key
  persistence.

Apple design references for P9:

- `https://developer.apple.com/design/human-interface-guidelines`
- `https://developer.apple.com/design/human-interface-guidelines/typography`
- `https://developer.apple.com/design/human-interface-guidelines/color`
- `https://developer.apple.com/design/human-interface-guidelines/layout`
- `https://developer.apple.com/design/human-interface-guidelines/accessibility`
- `https://developer.apple.com/design/human-interface-guidelines/writing`

Planner interpretation:

- Apple-inspired means quiet confidence: useful first, visually disciplined,
  accessible, and easy to scan.
- SnapLex is a Windows PySide6 utility. Use native Qt controls and patterns
  where they serve clarity. Do not imitate macOS chrome or Apple trademarks.
- Prefer reusable local UI helpers/tokens only when they remove real duplication
  or make visual validation easier.

## 2. Scope

P9 must complete:

- UI/UX audit of main shell, result states, Settings, History, and region
  selector interaction points.
- Shared visual foundation for spacing, typography, semantic color, focus,
  control sizing, and high-contrast states.
- Main shell polish for primary actions, utility actions, status, empty/loading,
  success, fake warning, error, retry, copy, and close states.
- Result area polish for long source text, long translation text, OCR text,
  provider identity, language pair, selectable text, and small-window behavior.
- Settings polish for provider setup grouping, readiness, connection test
  result, disabled future account affordance, target/source language, history,
  provider order, endpoints, and env var fields.
- History dialog polish for empty state, list scanning, copy/delete/clear, long
  entries, and keyboard operation.
- Keyboard navigation and focus order for shell, Settings, and History.
- Accessible labels, tooltips where icon-only controls are introduced, and
  contrast checks for semantic colors.
- Screenshot-backed offscreen GUI smoke that exercises representative states
  and verifies nonblank rendering/layout constraints without committing image
  artifacts.
- Visible Windows smoke notes for common DPI/small-window/manual inspection
  paths.
- `docs/p9_final_validation_report.md`.
- `docs/p9_to_p10_handoff.md`.
- README, phase plan, development plan, smoke checklist, TODO, and entry point
  updates.

Preferred P9 docs:

- `docs/p9_apple_inspired_ui_ux_goal_guide.md`
- `docs/p9_todo.md`
- `docs/p9_ui_audit.md`
- `docs/p9_visual_smoke_evidence.md`
- `docs/p9_final_validation_report.md`
- `docs/p9_to_p10_handoff.md`

## 3. Non-Scope

Do not implement in P9:

- SnapLex Cloud, account backend, token broker, billing, account OAuth, or
  keychain integration.
- Raw API key persistence in app config.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites, new provider adapters, or real network validation in
  automated tests.
- OCR/capture rewrites, multi-monitor coordinate rearchitecture, or PaddleOCR
  model packaging changes.
- Full localization implementation.
- Marketing landing pages, onboarding carousel, decorative illustration system,
  animated brand system, or a broad replatforming away from PySide6.
- Committing generated screenshots, package outputs, `build/`, `dist/`, local
  smoke data, OCR model caches, `.env`, provider secrets, logs, or user data.

## 4. Planner Decisions And Assumptions

- P9 is a product-quality polish phase, not a feature expansion phase.
- A compact shared UI style module is allowed if it prevents scattered
  stylesheet drift. Do not create a large design system unless repeated UI
  complexity justifies it.
- Iconography is optional. If used, prefer Qt standard icons or tiny local
  helpers over adding a new asset/dependency. Icon-only controls must have
  tooltips and accessible names.
- The result surface should favor selectable text, scrolling, and stable layout
  over decorative cards.
- Screenshot smoke should save local artifacts under ignored paths such as
  `snaplex-smoke-data/p9-screenshots`; final docs should summarize evidence,
  not commit screenshots.
- P10 should likely focus on secure credential/account strategy or localization
  foundation after P9, depending on trial feedback.

## 5. Architecture Boundaries

Hard constraints:

- Presenters and services remain the source of truth for state transitions.
- UI widgets may add layout, style, focus, labels, and event wiring only; they
  must not duplicate translation, provider, credential, capture, OCR, settings,
  or history semantics.
- Any screenshot smoke helper must be a test/support boundary, not a production
  dependency that changes app bootstrap.
- Visual state mapping must flow from existing `TranslationResultState`,
  `SettingsFormState`, provider setup state, and history presenter state.
- Local smoke artifacts remain ignored and untracked.
- No-GUI bootstrap and package dry-run must stay stable.
- Automated validation must not require real provider credentials or network.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P9 Apple-Inspired UI/UX Polish
Round goal:
Completed changes:
Debug self-check:
Architecture self-check:
Validation commands and results:
Commit hash:
Push result:
Buffer consumed:
Risks or blockers:
Next-round target:
```

Progression rules:

- Validation fails: do not commit, do not push, do not move to the next round.
- Validation passes but commit fails: do not move to the next round.
- Commit succeeds but push fails: do not move to the next round.
- Push succeeds: record commit hash and remote branch, then move to the next
  round.
- Any scope expansion beyond this guide must be explicitly approved by the
  architect/PM before implementation.

Debug self-check:

- Can the current UI change be explained by a specific user workflow or visual
  state?
- Can failures be localized to presenter state, widget layout, stylesheet,
  focus order, accessibility metadata, screenshot smoke, packaging, or docs?
- Are success, failure, empty, loading, fake-mode, long-text, small-window,
  keyboard, and disabled states covered where relevant?
- If UI changed, was a repeatable offscreen, screenshot, or manual smoke path
  updated?
- If generated screenshots or package outputs were created, are they ignored and
  left uncommitted?

Architecture self-check:

- Does the presenter/service layer remain the source of truth?
- Did UI code avoid duplicating provider, credential, translation, capture, OCR,
  settings, or history rules?
- Are visual tokens/style helpers separated from business state?
- Did the phase avoid pulling deferred product features into UI polish?
- Are unrelated files, generated outputs, and user changes left alone?

## 7. Round Plan

Round 1 - UI audit, visual targets, and baseline screenshots:

- Revalidate the accepted P8 baseline.
- Create `docs/p9_ui_audit.md` with current-state findings for main shell,
  result states, Settings, History, and region selector.
- Identify target states for screenshot smoke: idle, loading, success, fake,
  error, long text, Settings provider setup, Settings connection result, and
  History empty/list.
- Record non-scope boundaries before code changes.

Round 2 - Shared visual foundation:

- Add a small UI style/token helper only if it reduces duplicated stylesheet
  complexity.
- Define spacing, typography scale, semantic colors, borders, focus treatment,
  and stable control dimensions.
- Add tests for contrast helpers or style constants where practical.
- Keep colors restrained and avoid one-note palettes or decorative gradients.

Round 3 - Main shell action hierarchy:

- Refine the main shell into clear title/status, primary actions, secondary
  actions, result content, and result actions.
- Improve button sizing, focus indicators, disabled states, and action grouping.
- Preserve clipboard/screen translation wiring through existing presenters and
  services.

Round 4 - Result state polish:

- Polish empty, loading, success, fake warning, provider failure, unsupported,
  timeout, retryable, and closed states.
- Make provider identity, language pair, fake warning, and errors clear without
  overwhelming the translated text.
- Add or update presenter/UI tests for fake warning and error visibility.

Round 5 - Long text and small-window behavior:

- Add scrollable/selectable source and translation regions where needed.
- Verify long OCR text, long translation text, and longest provider/error words
  do not overflow or overlap.
- Add layout tests or screenshot smoke checks for constrained window sizes.

Round 6 - Settings information architecture:

- Refine Settings grouping for provider setup, language defaults, provider
  details, connection result, future account affordance, and history.
- Consider tabs or segmented sections if they improve scan speed.
- Keep provider setup logic behind SettingsPresenter/SettingsService.

Round 7 - Settings keyboard and accessibility:

- Fix tab order, default buttons, labels, accessible names, tooltips, and
  disabled future-account copy.
- Ensure env var presence is visible without showing secret values.
- Add focused tests or smoke for Settings loading and connection-test state.

Round 8 - History dialog polish:

- Improve History empty/list states, long entries, copy/delete/clear affordances,
  focus order, and status messages.
- Preserve HistoryPresenter/HistoryService boundaries.
- Add tests for empty and long-entry presentation if missing.

Round 9 - Region selector and screen-flow UI polish:

- Review region selector interaction feedback, cancel behavior, and screen-flow
  result handoff.
- Do not rewrite capture geometry or multi-monitor support in P9.
- Update visible smoke notes for DPI/single-monitor paths if needed.

Round 10 - Iconography and command semantics:

- Add optional icons only where they reduce scanning cost and remain accessible.
- Prefer Qt standard icons or local helpers; do not add a heavy icon dependency.
- Icon-only controls require accessible names and tooltips.
- Keep button text where ambiguity would hurt trial users.

Round 11 - Screenshot-backed GUI smoke:

- Add an offscreen GUI smoke helper or test path that renders representative
  states and writes screenshots to ignored local smoke output.
- Verify screenshots are nonblank and basic layout constraints hold.
- Ensure screenshot artifacts are not committed.

Round 12 - Windows visual QA and docs:

- Run visible Windows smoke where feasible and record results in
  `docs/p9_visual_smoke_evidence.md`.
- Cover common DPI, small window, long text, Settings, History, fake warning,
  and missing-real-provider trial paths.
- Update trial docs or smoke checklist only where P9 behavior changes.

Rounds 13-15 - Buffer hardening:

- Fix visual regressions, focus bugs, text overflow, contrast misses, flaky
  offscreen smoke, package dry-run issues, or docs gaps.
- Preserve P8 provider/setup behavior and no-network validation.
- Consume only as needed; otherwise use these rounds for targeted QA.

Round 16 - Final validation, report, and P10 handoff:

- Create `docs/p9_final_validation_report.md`.
- Create `docs/p9_to_p10_handoff.md`.
- Mark `docs/p9_todo.md` complete.
- Update README, phase plan, development plan, smoke checklist, and AGENTS entry
  points to reflect P9 completion.
- Run final validation, boundary scans, commit, push, and report back to the
  planner/checker session for P9 acceptance.
- Recommend P10 based on trial feedback, with secure credential/account strategy
  as the default candidate unless localization is more urgent.

## 8. Validation Matrix

Required P9 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python scripts\package_windows.py --dry-run --variant base`
- `cmd /c StartTrial.cmd --no-gui` expected rejection when no real provider is
  configured.
- `cmd /c StartFakeTrial.cmd --no-gui`
- `cmd /c SmokeTrial.cmd`
- PySide6 offscreen GUI smoke for main shell, Settings, History, and result
  states.
- Screenshot smoke showing nonblank representative states with artifacts written
  only to ignored local paths.
- Keyboard/focus smoke for shell, Settings, and History.
- Long-text and small-window smoke.
- Docs link/index check for P9 docs.
- Artifact and secret boundary scan showing no committed `build/`, `dist/`,
  packaged binaries, generated config/history, `.env`, provider keys,
  screenshots, OCR model caches, smoke data, local app data, logs, or API
  response captures.

Optional manual validation:

- Visible Windows smoke at common scaling values.
- Real-provider GUI smoke only when local credentials or self-hosted endpoint
  already exist.
- Capture/region-selector visible smoke on a single monitor.

No P9 validation may require:

- Real provider credentials.
- Real network calls in automated tests.
- SnapLex Cloud, account OAuth, keychain, browser extension, AI summary, or
  global hotkeys.
- Committed screenshots or packaged binaries.

## 9. PASS Criteria

P9 passes when:

- Main shell, result states, Settings, and History feel visually coherent and
  trial-ready.
- Apple HIG-inspired principles are reflected in hierarchy, spacing, typography,
  restrained color, focus, accessibility, and writing without cloning macOS.
- Keyboard navigation and focus order are usable for shell, Settings, and
  History.
- Long text and small-window states do not overflow, overlap, or hide required
  actions.
- Fake-mode warning, provider identity, and real-provider setup states remain
  clear.
- P8 provider/setup boundaries and no-secret rules remain intact.
- Screenshot-backed GUI smoke exists and artifacts remain uncommitted.
- Existing P8 validation remains green.
- P9 final validation report and P9 to P10 handoff exist.
- Final P9 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P9 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- UI/UX changes:
- Accessibility and keyboard evidence:
- Screenshot/visual smoke evidence:
- Long-text and small-window evidence:
- Provider/setup boundary preservation:
- Deferred scope:
- Architecture notes:
- Manual smoke evidence:
- Artifact and secret exclusion evidence:
- Commit hashes:
- Push result:
- Request for architect/PM acceptance:
- Recommended next goal:
```

```text
P9 to P10 handoff:
- Accepted P9 baseline:
- Visual system and screenshot smoke:
- Remaining UX/accessibility gaps:
- Provider/credential limitations:
- Recommended P10 scope:
- Validation to preserve:
- Explicit non-scope:
```
