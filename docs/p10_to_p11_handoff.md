# P10 To P11 Handoff

Date: 2026-07-15
Status: P10 executor-complete; planner check requested

Recommended next phase: P11 Trial Release Hardening.

Candidate P11 guide should preserve P10 credential boundaries while focusing on
visible Windows validation, manual keyring smoke, packaged credential behavior,
and real-provider onboarding clarity.

## Accepted P10 Baseline For Review

P10 leaves SnapLex with:

- credential references/statuses behind `CredentialService`;
- environment-variable compatibility for existing real-provider users;
- optional lazy OS keyring store via the `credentials` extra;
- config serialization that stores credential references, not raw values;
- provider setup, Test Connection, and trial readiness routed through the
  credential boundary;
- Settings credential source/reference/save/delete controls with transient
  password input;
- real trial commands that fail closed when no accepted credential source is
  ready;
- fake trial and package smoke commands that stay deterministic and visibly
  fake;
- account/cloud/token-broker options documented but not implemented.

## Credential Storage Behavior

Environment credentials are read from the current process environment at
runtime. SnapLex stores only env-var names.

Keyring credentials are resolved through a lazy optional store. SnapLex stores
only source `keyring` and a non-secret identifier such as
`snaplex/openai/default`. Automated tests use fake stores and injected fake
keyring modules.

The deterministic base package smoke path does not require keyring. Packaging a
distributable that claims keyring support still needs explicit manual smoke.

## Account And Cloud Decisions

P10 keeps account sign-in disabled. SnapLex Cloud, account OAuth, hosted token
broker, billing, cloud sync, and enterprise account flows remain future
architecture work requiring explicit security and product approval.

`docs/p10_account_strategy.md` records the tradeoffs for env vars, OS keyring,
SnapLex Cloud/token broker, provider OAuth/enterprise identity, and
self-hosted LibreTranslate.

## Known Credential And Security Gaps

- Manual Windows Credential Locker smoke was not run.
- Real provider network smoke was not run.
- Packaged keyring behavior is documented but not productized as a release
  variant.
- Visible Windows GUI smoke with normal desktop fonts remains recommended
  before wider trial distribution.
- Assistive technology checks remain manual future validation.
- Provider-specific least-privilege and key-rotation notes are still light.

## Recommended P11 Scope

P11 should be release-hardening, not feature expansion:

- run visible Windows smoke for shell, Settings, History, long text, focus, and
  real/fake trial commands;
- run Windows Credential Locker smoke with a throwaway provider key;
- decide whether packaged SnapLex should include keyring support by default or
  through an explicit credential-capable variant;
- improve provider onboarding copy where trial users still hesitate;
- add provider key-rotation and least-privilege notes;
- preserve no-network automated validation and fake smoke determinism.

Alternative P11 candidates are localization foundation or broader trial docs,
but credential release hardening is the lowest-risk next step after P10.

## Validation To Preserve

- `Validate.cmd` full validation.
- `git diff --check`.
- `python -m snaplex --version`.
- `python -m snaplex --no-gui`.
- `python scripts\package_windows.py --dry-run --variant base`.
- `python -m snaplex --check-real-provider` expected rejection without real
  provider setup.
- `cmd /c StartTrial.cmd --no-gui` expected rejection without real provider
  setup.
- `cmd /c StartFakeTrial.cmd --no-gui`.
- `cmd /c SmokeTrial.cmd`.
- `python scripts\p9_gui_smoke.py`.
- Credential service/store tests with fake keyring stores only.
- Provider connection tests with mocked HTTP only.
- Artifact and secret boundary scan.

## Explicit Non-Scope For P11 Unless Approved

- Production SnapLex Cloud.
- Account OAuth, billing, remote accounts, or hosted token broker.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to credential/onboarding validation.
- OCR/capture rewrites.
- Full localization implementation.
- Automated tests that require real provider credentials, network calls, or a
  real OS keyring.
- Committed screenshots, package outputs, local app data, `.env`, provider
  secrets, keyring exports, logs, OCR model caches, or smoke data.
