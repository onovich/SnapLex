# P8 To P9 Handoff

Date: 2026-07-15
Status: P8 executor-complete, pending planner acceptance

Recommended next phase: P9 Apple-Inspired UI/UX Polish

## Accepted P8 Baseline

P8 adds real-provider setup UX without introducing cloud accounts or raw secret
persistence:

- Provider setup state model in `snaplex/services/provider_setup.py`.
- Settings service/presenter readiness and connection-test boundaries.
- Mocked HTTP tests for OpenAI, DeepL, and LibreTranslate connection tests.
- Settings UI provider controls, readiness display, env var presence, and
  disabled future account-connect affordance.
- Fake-mode result warning in shared result presentation state.
- Trial docs/scripts that keep real provider and fake smoke paths separate.
- First main shell/result visual foundation.

## Provider Setup Behavior

- `fake`: deterministic smoke/dev mode, not real translation.
- `libretranslate`: endpoint-first setup, optional env var name when a key is
  required by the user's endpoint.
- `openai`: requires an API-key env var name and a present env var value before
  connection testing.
- `deepl`: requires an API-key env var name and a present env var value before
  connection testing.
- `Test Connection` runs a probe translation through provider adapters and
  mocked transports in tests.

## Credential Limitations

- P8 does not store raw provider keys.
- P8 does not implement account OAuth, SnapLex Cloud, a token broker, billing,
  or keychain integration.
- Environment variables remain the supported local secret boundary.
- Future secure credential work should be scoped explicitly before enabling any
  account sign-in UI.

## UI/UX Baseline

- Main shell uses clear primary and secondary action hierarchy.
- Result view separates source text, translated text, provider identity,
  fake-mode warning, errors, copy, retry, close, and status.
- Settings dialog is provider-setup oriented and no longer only a raw config
  field list.
- Styling is restrained and native-feeling, with neutral surfaces and limited
  semantic color.

## Known Visual And Accessibility Gaps

- No screenshot-backed visual regression test exists yet.
- Settings remains dense and should be reviewed for keyboard navigation,
  grouping, tab order, and long text behavior.
- Main window needs visible Windows smoke at common DPI scaling values.
- Result area can be refined for long OCR text and long translations.
- Icons, shortcuts, and focus indicators can be improved in P9.

## Recommended P9 Scope

- Visual QA for main shell, result states, Settings, and History.
- Keyboard navigation and focus order.
- Accessible labels and contrast checks.
- Long text and small window behavior.
- Screenshot-backed offscreen smoke where feasible.
- Optional iconography using native/simple symbols if it improves clarity.

## Validation To Preserve

- `Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python scripts\package_windows.py --dry-run --variant base`
- Fake/real trial command smoke.
- Provider connection tests with mocked HTTP only.
- Artifact and secret boundary scan.

## Explicit Non-Scope

- SnapLex Cloud, account OAuth, billing, token broker, or keychain integration.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites or real network validation in automated tests.
- Committing generated screenshots, packages, local data, `.env`, or secrets.

