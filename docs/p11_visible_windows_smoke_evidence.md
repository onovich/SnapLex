# P11 Visible Windows Smoke Evidence

Date: 2026-07-16
Phase: P11 Trial Release Hardening
Status: planned; baseline revalidation complete

P11 starts from the planner-accepted P10 baseline at
`5a37564993c67dcf9c5bfe5da2ed06a44327874c`. The release-hardening risk is no
longer core service behavior; it is whether the P8-P10 trial experience is
clear and stable on a normal Windows desktop and in packaged/credential smoke
paths.

## Round 1 Baseline Revalidation

The P10 baseline was revalidated before visible-smoke work:

- `Validate.cmd`: PASS with 255 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS, PySide6 bootstrap OK.
- `python -m snaplex --check-real-provider`: expected rejection PASS when no
  real provider is configured.
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: expected missing-provider rejection PASS.

No real provider credentials, real network calls, real OS keyring access,
screen permissions, model downloads, package builds, or committed screenshots
were required for this baseline.

## Visible Smoke Coverage Target

The P11 visible desktop smoke should cover:

- main shell launch, normal Windows desktop fonts, window sizing, and
  always-on-top behavior;
- primary clipboard and screen actions, secondary Settings/History actions, and
  visible focus outlines;
- fake-provider result state with explicit fake warning;
- loading, error, and long-text result states;
- Settings provider setup tabs, credential source/readiness fields, and
  disabled future account affordance;
- History empty and list states;
- real trial fail-closed behavior when no real provider credential exists;
- fake trial path remains deterministic and visibly fake.

If the executor environment cannot expose a visible Windows desktop to Qt, P11
must record the exact blocker and keep release readiness scoped accordingly.
Offscreen screenshot smoke remains useful regression evidence, but it does not
replace a visible desktop-font pass for broader private trial readiness.

## Initial Release-Risk Audit

Known P10 limitations carried into P11:

- visible Windows GUI smoke with normal desktop fonts was not run;
- manual Windows Credential Locker/keyring smoke was not run;
- packaged keyring behavior is documented but not productized as a package
  variant;
- real provider network smoke was not run and must remain optional;
- provider key-rotation and least-privilege guidance is still light;
- assistive technology, DPI, and multi-monitor checks remain manual future
  validation.

Release-hardening should fix only narrow validation, packaging, onboarding copy,
and evidence gaps. It must not add production cloud accounts, OAuth, billing,
global hotkeys, browser extension runtime, AI summary runtime, provider
rewrites, OCR/capture rewrites, or full localization.

## Artifact Boundary

Visible smoke screenshots, app data, logs, package outputs, keyring exports,
OCR caches, `.env`, and provider secrets must remain local ignored artifacts.
Any manual throwaway credential value used for smoke must be deleted and must
not appear in docs, tests, screenshots, logs, config, history, package
resources, or git.
