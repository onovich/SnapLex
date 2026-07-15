# P9 To P10 Handoff

Date: 2026-07-15
Status: P9 executor-complete; pending planner acceptance

Recommended next phase: P10 Secure Credential/Account Strategy, unless trial
feedback makes localization more urgent.

## Accepted P9 Baseline

P9 leaves SnapLex as a polished Windows desktop trial candidate:

- first screen is still the usable translation shell;
- clipboard and screen actions remain manual, explicit, and deterministic;
- result states use shared presenter data and stable scrollable text regions;
- Settings provider setup is tabbed and keyboard-accessible;
- History has clearer empty/list/long-entry states;
- fake-provider output remains visibly labeled as fake smoke/dev mode;
- real trial launch paths still reject missing real provider configuration;
- automated validation and GUI smoke remain deterministic and no-network.

## Visual System And Screenshot Smoke

Shared visual tokens live in `snaplex/ui/style.py`. The P9 GUI smoke helper is
`scripts/p9_gui_smoke.py`; it writes local screenshots to
`snaplex-smoke-data\p9-screenshots` and verifies representative shell,
Settings, History, error, fake-success, loading, and long-small-window states.

Screenshots and smoke data are intentionally ignored local artifacts. Do not
commit them.

## Remaining UX And Accessibility Gaps

- Visible Windows smoke still needs a normal desktop-font pass before broader
  trial distribution.
- The Codex offscreen Qt environment reports zero font families, so offscreen
  screenshots show square glyphs even though geometry and state checks pass.
- Assistive technology verification remains a manual future pass.
- DPI, multi-monitor, and real capture/OCR visible smoke remain important
  before marketing or wider end-user trial distribution.

## Provider And Credential Limitations

P8/P9 deliberately avoid raw API-key persistence. Provider setup records env
var names, endpoints, timeouts, retries, model options, and provider order, but
not secret values.

This means ordinary users still need local environment variables for real
providers. The disabled future account-connect affordance is only a placeholder;
there is no token broker, account OAuth, billing, cloud account, or keychain
flow.

## Recommended P10 Scope

Default P10 candidate: Secure Credential/Account Strategy.

Suggested planning questions:

- Should SnapLex remain local-env-var based for private trial, add OS keychain
  storage, or introduce an account/token-broker architecture?
- What is the minimum credential path that preserves no-secret docs, logs,
  tests, screenshots, history, package resources, and git boundaries?
- How should Test Connection and trial scripts behave when secure credential
  storage exists?
- Should a future account flow remain disabled until a real backend exists?
- What migration path should preserve existing env-var based P8/P9 users?

Alternative P10 candidate: localization foundation. Choose this first only if
trial feedback says UI language polish is more urgent than credential setup.

## Validation To Preserve

- `Validate.cmd` full validation.
- `git diff --check`.
- `python -m snaplex --version`.
- `python -m snaplex --no-gui`.
- `python scripts\package_windows.py --dry-run --variant base`.
- `cmd /c StartTrial.cmd --no-gui` rejects missing real-provider configuration.
- `cmd /c StartFakeTrial.cmd --no-gui` stays deterministic fake smoke.
- `cmd /c SmokeTrial.cmd`.
- `python scripts\p9_gui_smoke.py`.
- Artifact and secret boundary scan.

## Explicit Non-Scope For P10 Unless Approved

- Browser extension runtime.
- AI summary runtime.
- Cloud sync/accounts beyond an explicitly approved credential strategy.
- Billing or production account OAuth.
- Provider rewrites unrelated to credential setup.
- Capture/OCR rewrites.
- Global hotkeys.
- Committed screenshots, smoke data, local config/history, `.env`, package
  outputs, OCR model caches, or provider secrets.
