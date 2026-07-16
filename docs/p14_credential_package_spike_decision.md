# P14 Credential Package Spike Decision

Date: 2026-07-16
Phase: P14 Manual Environment And Source Keyring Validation
Status: recommend a later isolated spike; do not implement a credential-capable package in P14

P14 revisits the P13 credential package feasibility question after source
keyring support became available in the executor environment. The decision is
to recommend a later isolated credential-capable package spike, under explicit
architect approval, while keeping P14 as validation and documentation only.

## Decision

Evidence now justifies a later isolated credential package spike.

P14 must not implement, ship, or promise a credential-capable package variant.
The accepted base package path remains the deterministic fake/private-trial
smoke path. A future spike may prototype packaged keyring behavior only if it
is explicitly scoped as a spike and keeps the base package, no-gui mode, fake
trial smoke, and automated tests deterministic and no-network.

## Evidence

| Evidence | Result | Impact |
| --- | --- | --- |
| External tester feedback | NOT SUPPLIED | No external S0/S1 report requires package credential support. |
| Source optional credential support | PASS | P14 installed the optional `credentials` extra locally and confirmed `keyring_available=True`. |
| Source keyring backend | PASS | Source checkout resolved `keyring.backends.Windows.WinVaultKeyring`. |
| Source save/read/delete smoke | PASS | `python tmp\p14_keyring_smoke.py` saved, read, deleted, and verified cleanup with a throwaway fake value. |
| Real provider readiness | PASS fail-closed | `python -m snaplex --check-real-provider` rejects when no real provider is configured. |
| Base package dry-run | PASS | `python scripts\package_windows.py --dry-run --variant base` preserves the current base package command. |
| Full package dry-run | PASS | `python scripts\package_windows.py --dry-run --variant full` remains capture/OCR dependency scope, not credential scope. |
| Focused tests | PASS | Packaging, release smoke, and credential tests passed with 23 tests. |

## Command Evidence

Base package dry-run:

```cmd
python scripts\package_windows.py --dry-run --variant base
```

Result: PASS.

```text
SNAPLEX_PACKAGE_VARIANT=base
C:\Python314\python.exe -m PyInstaller --distpath D:\ToolProjects\SnapLex\dist --workpath D:\ToolProjects\SnapLex\build\pyinstaller --clean --noconfirm D:\ToolProjects\SnapLex\packaging\snaplex.spec
```

Full package dry-run:

```cmd
python scripts\package_windows.py --dry-run --variant full
```

Result: PASS.

```text
SNAPLEX_PACKAGE_VARIANT=full
C:\Python314\python.exe -m PyInstaller --distpath D:\ToolProjects\SnapLex\dist --workpath D:\ToolProjects\SnapLex\build\pyinstaller --clean --noconfirm D:\ToolProjects\SnapLex\packaging\snaplex.spec
```

Focused deterministic tests:

```cmd
python -m pytest tests\test_package_windows.py tests\test_release_smoke.py tests\test_credentials.py --basetemp tmp\pytest-p14-credential-package-spike
```

Result: PASS with 23 tests. Pytest emitted a non-blocking local cache warning
for `.pytest_cache`; no test failed.

Real provider readiness guard:

```cmd
python -m snaplex --check-real-provider
```

Result: expected rejection PASS.

```text
Real translation provider is not configured.
```

## Later Spike Scope

A later spike may investigate:

- an explicit credential-capable package variant or prototype entry point;
- packaged keyring backend inclusion and import discovery;
- packaged save/read/delete with a throwaway fake value;
- restart readiness after a packaged credential save;
- clear failure messaging when keyring support is missing, locked, or unusable;
- cleanup guidance for throwaway/manual credentials;
- artifact, local-data, and no-secret hygiene for package smoke.

The spike must not include production SnapLex Cloud, account OAuth, billing,
hosted token broker, provider rewrites, OCR/capture rewrites, browser extension
runtime, AI summary runtime, global hotkeys, full localization, or real network
automation.

## Spike Entry Criteria

Before a future credential package spike starts:

- the architect explicitly approves the spike and scope;
- source keyring save/read/delete remains green with a throwaway fake value;
- base package dry-run and fake package smoke remain deterministic;
- automated tests remain no-network and do not require real keyring state;
- manual smoke instructions forbid real secrets, screenshots with sensitive
  content, keyring exports, `.env` files, logs, tester personal data, OCR
  caches, package outputs in git, or provider keys.

## Spike Exit Criteria

The future spike should not be accepted until it proves:

- packaged save/read/delete with a throwaway fake value;
- packaged restart readiness without printing or exposing the fake value;
- fail-closed real trial behavior when no real provider is configured;
- base package fake smoke unchanged and deterministic;
- no raw secrets in config, history, docs, tests, logs, screenshots, package
  resources, git, or local smoke artifacts;
- a clear decision on whether to promote the spike to a release variant,
  continue investigation, or abandon package credential support.

## Round 8 Self-Checks

Debug self-check:

- The decision is tied to new P14 source keyring evidence and current packaging
  dry-runs.
- P14 still records no external tester feedback and does not fabricate demand.
- The decision recommends a later spike without implementing or promising a
  credential-capable package.

Architecture self-check:

- Credential behavior remains behind `CredentialService` and credential stores.
- Provider execution remains behind `TranslationProvider`, provider registry,
  and `TranslationPipeline`.
- Packaging remains a thin release wrapper and does not own provider, keyring,
  settings, history, OCR, capture, or UI business rules.
