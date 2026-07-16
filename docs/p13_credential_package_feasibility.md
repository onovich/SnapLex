# P13 Credential Package Feasibility

Date: 2026-07-16
Phase: P13 Private Trial Feedback Response And Credential Package Feasibility
Status: defer implementation; recommend a later isolated feasibility spike only

P13 reviewed whether SnapLex should implement a credential-capable package
variant after the first private-trial feedback loop. The answer for P13 is:
defer implementation. A later explicit phase may prototype packaged keyring
support, but P13 should not add a new package variant or promise packaged
keyring behavior.

## Decision

Do not implement a credential-capable package variant in P13.

Recommended next action: run a later isolated credential-package spike only
after source keyring smoke can run with optional `keyring` support installed and
a throwaway fake value. The spike should prove packaged save/read/delete,
restart readiness, failure messaging, cleanup guidance, and artifact/secret
hygiene before any release promise.

## Evidence

| Evidence | Result | Impact |
| --- | --- | --- |
| No external tester feedback supplied | PASS evidence source | No pilot report currently requires packaged keyring support as an S0/S1 fix. |
| Source keyring availability | BLOCKED | `docs/p13_keyring_source_smoke_record.md` shows `keyring_available=False`; source OS keyring smoke did not run. |
| Existing package variants | PASS known scope | `scripts\package_windows.py` supports `base`, `capture`, `ocr`, and `full`; none is a credential package variant. |
| Base package dry-run | PASS | `python scripts\package_windows.py --dry-run --variant base` prints `SNAPLEX_PACKAGE_VARIANT=base` and the tracked PyInstaller spec command. |
| Full package dry-run | PASS | `python scripts\package_windows.py --dry-run --variant full` prints `SNAPLEX_PACKAGE_VARIANT=full`; this is capture/OCR dependency scope, not keyring scope. |
| Focused packaging and credential tests | PASS | `python -m pytest tests\test_package_windows.py tests\test_release_smoke.py tests\test_credentials.py --basetemp tmp\pytest-p13-credential-package` passed with 23 tests. |

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

Focused tests:

```cmd
python -m pytest tests\test_package_windows.py tests\test_release_smoke.py tests\test_credentials.py --basetemp tmp\pytest-p13-credential-package
```

Result: PASS with 23 tests. Pytest emitted a non-blocking local cache warning
for `.pytest_cache`; no test failed.

## Feasibility Assessment

Feasible later, but not proven enough to ship or implement now.

Reasons to defer:

- Source OS keyring smoke is blocked because optional `keyring` is unavailable
  in the executor environment.
- Packaged save/read/delete has not been tested with a throwaway fake value.
- The current base package is already the deterministic private-trial smoke
  path and must remain usable without keyring, provider credentials, network,
  screen permissions, model downloads, or API keys.
- Adding a credential-capable package surface now would expand support,
  cleanup, installer, and failure-mode obligations without an accepted S0/S1
  pilot blocker.
- P13 boundaries prohibit implementing a credential-capable package variant
  without later explicit architect approval.

Reasons to keep a later spike open:

- P10 credential services already isolate credential behavior behind stores and
  provider readiness boundaries.
- Existing packaging infrastructure can pass explicit variant state through
  `SNAPLEX_PACKAGE_VARIANT`.
- Focused packaging and credential tests remain deterministic and no-network.

## Later Spike Entry Criteria

A future P14 or later spike may start only when:

- source checkout optional credentials support is installed;
- source OS keyring save/read/delete passes with a throwaway fake value;
- package build environment can include the necessary keyring backend modules
  deliberately, not accidentally;
- the spike has explicit architect approval to add a credential-capable package
  variant or prototype;
- automated validation remains deterministic and no-network;
- manual package keyring smoke never prints or commits secret values.

## Later Spike Exit Criteria

A future package credential spike should not be accepted until it proves:

- packaged save/read/delete with a throwaway fake value;
- package restart readiness without displaying the secret;
- clear failure messaging when the keyring backend is missing or locked;
- cleanup guidance for local credentials;
- no raw secrets in config, history, docs, tests, logs, screenshots, package
  resources, git, or local smoke artifacts;
- base fake package smoke remains unchanged and deterministic.

## Round 7 Self-Checks

Debug self-check:

- The decision is tied to P13 credential package feasibility.
- No credential package variant was built or promised.
- Base and full package dry-runs plus focused tests provide deterministic
  evidence without network or real credentials.

Architecture self-check:

- Credential behavior remains behind services/stores and trial readiness.
- Packaging remains a thin wrapper and does not move provider, keyring, config,
  settings, history, OCR, or capture logic into scripts.
- P13 continues to preserve no-secret and no-artifact repository hygiene.
