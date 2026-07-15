# P11 To P12 Handoff

Date: 2026-07-16
Status: P11 executor-complete; ready for planner/checker acceptance

Recommended next phase: P12 Private Trial Pilot And Feedback Triage.

P11 final validation report: `docs/p11_final_validation_report.md`
P11 private trial checklist: `docs/p11_private_trial_release_checklist.md`

## Accepted Input And Executor Baseline

P11 started from planner-accepted P10 at
`5a37564993c67dcf9c5bfe5da2ed06a44327874c`.

The final P11 baseline is the pushed closure commit containing this handoff and
`docs/p11_final_validation_report.md`.

## What P11 Leaves Stable

- P10 credential boundaries remain intact: providers, provider setup, Test
  Connection, trial readiness, SettingsService, and SettingsPresenter resolve
  credentials through services/stores.
- UI widgets remain clients of presenter/service boundaries and do not own
  provider or secret business rules.
- Fake trial/package smoke remains deterministic and visibly fake.
- Real trial commands reject missing real-provider configuration instead of
  falling back to fake translation.
- Base package smoke remains deterministic and does not require keyring,
  provider credentials, network, screen permissions, OCR model downloads, or
  API keys.
- Local app data, screenshots, package outputs, `.env`, logs, keyring exports,
  OCR caches, and provider secrets remain untracked.

## P11 Evidence Package

- `docs/p11_visible_windows_smoke_evidence.md`
- `docs/p11_keyring_smoke_evidence.md`
- `docs/p11_keyring_packaging_decision.md`
- `docs/p11_packaged_trial_evidence.md`
- `docs/p11_provider_onboarding_notes.md`
- `docs/p11_key_rotation_least_privilege.md`
- `docs/p11_private_trial_release_checklist.md`
- `docs/p11_boundary_scan_evidence.md`
- `docs/p11_final_validation_report.md`

## Validation To Preserve In P12

- `Validate.cmd` full validation.
- `git diff --check`.
- `python -m snaplex --version`.
- `python -m snaplex --no-gui`.
- `python -m snaplex --check-real-provider` expected rejection when no real
  provider is configured.
- `python scripts\package_windows.py --dry-run --variant base`.
- `cmd /c StartTrial.cmd --no-gui` expected rejection when no real provider is
  configured.
- `cmd /c StartFakeTrial.cmd --no-gui`.
- `cmd /c SmokeTrial.cmd`.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`.
- `cmd /c StartPackagedTrial.cmd --no-gui` expected rejection when no real
  provider is configured.
- `python scripts\p9_gui_smoke.py`.
- `python scripts\p11_visible_gui_smoke.py`.
- Artifact/secret boundary scan.

## Known Limitations Carrying Forward

- Manual Windows Credential Locker smoke did not run because the executor
  environment lacks the optional `keyring` dependency.
- Base package does not promise local secure credential/keyring support.
- Real provider network smoke was not run.
- Assistive technology, DPI scaling, and multi-monitor visible Windows checks
  remain future manual validation.
- No production account OAuth, SnapLex Cloud, hosted token broker, billing,
  browser extension runtime, AI summary runtime, global hotkeys, provider
  rewrites, OCR/capture rewrites, or full localization has been implemented.

## Recommended P12 Scope

P12 should move from release hardening to controlled private-trial operation:

- create tester-facing release notes and a feedback intake template;
- define pass/fail criteria for first private trial builds;
- run/manual-record assistive technology, DPI scaling, and multi-monitor checks
  where hardware is available;
- optionally run one real-provider smoke only when local credentials already
  exist and a human intentionally approves the network call;
- decide whether a credential-capable package variant is worth building, or
  continue with source checkout plus `.[gui,credentials]` for secure local
  credential testing;
- keep all automated tests deterministic, mocked, no-network, and no-secret.

## P12 Non-Scope Unless Architect Approves

- Production SnapLex Cloud.
- Account OAuth, billing, remote accounts, hosted token broker, or cloud sync.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to private-trial feedback.
- OCR/capture rewrites.
- Full localization implementation.
- Automated validation requiring real provider credentials, network calls, real
  OS keyring state, screen permissions, or model downloads.
- Committed screenshots, package outputs, local app data, `.env`, provider
  secrets, keyring exports, logs, OCR model caches, or smoke data.
