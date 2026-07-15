# P11 Final Validation Report

Date: 2026-07-16
Phase: P11 Trial Release Hardening
Status: PASS, planner-accepted

Accepted input baseline: P10 at
`5a37564993c67dcf9c5bfe5da2ed06a44327874c`.

## Summary

P11 hardens SnapLex for private Windows trial distribution without adding new
runtime product scope. It revalidates the P10 credential boundary, adds visible
Windows GUI smoke evidence, records the local keyring smoke blocker and lazy
unavailable behavior, documents the package/keyring decision, verifies packaged
fake smoke and real-trial fail-closed behavior, polishes provider onboarding,
adds key rotation and least-privilege guidance, consolidates the private-trial
release checklist, and records final artifact/secret boundary evidence.

P11 does not add production SnapLex Cloud, account OAuth, billing, a hosted token
broker, browser extension runtime, AI summary runtime, global hotkeys, provider
rewrites, OCR/capture rewrites, or full localization.

Rounds used: 10 of 12.

Buffer rounds consumed: 1.

## Planner Acceptance

- Rechecked by planner on 2026-07-16.
- Acceptance result: PASS.
- Recheck validation: `Validate.cmd` PASS with 255 tests, `git diff --check`
  PASS, CLI bootstrap PASS, real-provider readiness expected rejection PASS,
  package dry-run PASS, source/package real/fake trial smoke PASS,
  `SmokeTrial.cmd` PASS, P9 GUI smoke PASS, P11 visible GUI smoke PASS, keyring
  unavailable smoke PASS, focused credential/readiness tests PASS, P11 docs
  index check PASS, and artifact/secret boundary scan PASS.
- Accepted commit: `66d3cef11db492b6c6170c26b69e483528186767`.

## Main Deliverables

- `scripts/p11_visible_gui_smoke.py` for native Windows Qt-platform GUI smoke.
- `docs/p11_visible_windows_smoke_evidence.md`.
- `docs/p11_keyring_smoke_evidence.md`.
- `docs/p11_keyring_packaging_decision.md`.
- `docs/p11_packaged_trial_evidence.md`.
- `docs/p11_provider_onboarding_notes.md`.
- `docs/p11_key_rotation_least_privilege.md`.
- `docs/p11_private_trial_release_checklist.md`.
- `docs/p11_boundary_scan_evidence.md`.
- Updated `TRY.md`, `.env.example`, `RequireRealProvider.cmd`,
  `packaging/README.md`, `docs/windows_smoke_checklist.md`, `README.md`,
  `docs/phase_plan.md`, and `docs/development_plan.md`.

## Validation Commands And Results

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`:
  PASS with 255 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, prints `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS, PySide6 bootstrap OK.
- `python -m snaplex --check-real-provider`: expected rejection PASS when no
  real provider is configured.
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: expected rejection PASS when no real
  provider is configured.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS, fake smoke mode labeled.
- `cmd /c SmokeTrial.cmd`: PASS, including packaged executable smoke because a
  local `dist\SnapLex\SnapLex.exe` existed.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`: PASS, fake smoke mode labeled.
- `cmd /c StartPackagedTrial.cmd --no-gui`: expected rejection PASS when no
  real provider is configured.
- `python scripts\p9_gui_smoke.py`: PASS with seven ignored local screenshots.
- `python scripts\p11_visible_gui_smoke.py`: PASS with six ignored local
  screenshots.
- `python -c "import importlib.util; print('keyring' if importlib.util.find_spec('keyring') else 'missing')"`:
  PASS, result `missing`.
- Lazy keyring unavailable smoke: PASS, status `unavailable`, text
  `Credential source unavailable`, detail
  `Install the optional credentials extra to use local secure storage.`
- `python -m pytest tests\test_credentials.py tests\test_trial_readiness.py tests\test_release_smoke.py --basetemp tmp\pytest-p11-boundary`:
  PASS with 22 tests.
- `git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs`:
  PASS, no tracked files.
- Secret-pattern scan: PASS with only historical no-token documentation lines
  and placeholder-only `your_trial_key` examples in `RequireRealProvider.cmd`.

## Visible Windows GUI Smoke

P11 added and ran `scripts/p11_visible_gui_smoke.py` against the native Windows
Qt platform plugin. The helper opened shell, result, Settings, History, and
focus states, verified desktop font availability and expected visible text, and
captured ignored local screenshots under
`snaplex-smoke-data\p11-visible-screenshots`.

This is automated visible-platform evidence. Human assistive-technology, DPI,
and multi-monitor validation remain future manual trial checks.

## Credential And Keyring Result

The current executor environment does not have the optional `keyring` package
installed, so manual Windows Credential Locker smoke was blocked. P11 recorded
the exact blocker and revalidated that missing keyring support reports a
controlled unavailable credential state instead of breaking bootstrap,
Settings, readiness, package dry-run, or deterministic tests.

The accepted P11 package decision keeps the deterministic base package free of
keyring requirements. Source checkout plus `.[gui,credentials]` remains the
documented local secure credential path until a future credential-capable
package variant is explicitly built and manually smoked.

## Package And Trial Behavior

The base package remains deterministic, fake-provider based, and does not
require keyring, real provider credentials, real network calls, screen
permissions, OCR model downloads, or API keys. Fake trial commands remain
visibly labeled as fake smoke mode. Real trial commands fail closed when no real
provider credential or accepted endpoint exists and do not silently fall back to
fake translation.

## Provider Onboarding

P11 clarifies the three trial paths:

- fake smoke mode for UI/package validation without real translation;
- environment variables for real providers from source or package;
- optional local secure credential from source when `keyring` is installed.

P11 also adds private-trial key rotation and least-privilege guidance:
separate short-lived trial keys, lowest practical quota/budget/access, local
secret-only storage, cleanup, and suspected exposure response.

## Artifact And Secret Boundary

P11 stores only env-var names or keyring identifiers. It does not store raw
provider keys in config, history, docs, tests, screenshots, logs, package
resources, or git. Generated screenshots, package outputs, local app data,
pytest temp data, OCR caches, `.env`, logs, and keyring exports remain
untracked.

## Known Limitations

- Manual Windows Credential Locker smoke was blocked by the missing optional
  `keyring` dependency in the executor environment.
- Real provider network smoke was not run and remains optional/manual only.
- Base package does not promise keyring support in P11.
- Human assistive-technology, DPI scaling, and multi-monitor checks remain
  future manual private-trial validation.
- Production account/OAuth/cloud/billing/token-broker work remains out of
  runtime scope.

## Commit Hashes

P11 was delivered through incremental pushed commits:

- `c8c246b` - release smoke audit.
- `2034d3c` - visible GUI smoke.
- `fd07d93` - keyring smoke blocker.
- `59c78c4` - keyring packaging decision.
- `c7dbdb2` - packaged trial evidence.
- `4582c80` - provider onboarding polish.
- `d0e208e` - key rotation guidance.
- `13ce69c` - private trial checklist.
- `ca90b5b` - boundary scan evidence.
- `66d3cef` - final trial release hardening report and P11-to-P12 handoff.

## Push Result

P11 implementation and closure docs through
`66d3cef11db492b6c6170c26b69e483528186767` are pushed to `origin/main`.

## Request For Acceptance

P11 is accepted against `docs/p11_trial_release_hardening_goal_guide.md`.
Recommended next goal: P12 Private Trial Pilot And Feedback Triage, focused on
tester-facing release notes, private-trial feedback intake, manual
assistive-technology/DPI/multi-monitor checks, optional real-provider smoke when
local credentials already exist, and a decision on whether a credential-capable
package variant is worth building.
