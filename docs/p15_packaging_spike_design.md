# P15 Packaging Spike Design

Date: 2026-07-16
Phase: P15 Isolated Credential-Capable Package Spike Design Gate
Status: explicit spike boundary selected

P15 starts from the planner-accepted P14 baseline. Source checkout keyring
save/read/delete passed with a throwaway fake value on Windows
WinVaultKeyring, but packaged keyring behavior was not implemented, tested,
shipped, or promised. P15 is the narrow design gate that proves, rejects, or
defers packaged credential support without changing the deterministic base
package path.

## Round 1 Baseline

| Check | Result | Evidence |
| --- | --- | --- |
| Full validation | PASS | `Validate.cmd` passed ruff, format check, mypy, compileall, and 255 tests. |
| Version bootstrap | PASS | `python -m snaplex --version` printed `SnapLex 0.1.0`. |
| No-GUI bootstrap | PASS | `python -m snaplex --no-gui` printed PySide6 bootstrap OK. |
| Real provider readiness | PASS fail-closed | `python -m snaplex --check-real-provider` rejected missing real setup. |
| Base package dry-run | PASS | `python scripts\package_windows.py --dry-run --variant base` printed `SNAPLEX_PACKAGE_VARIANT=base`. |
| Source real trial | PASS fail-closed | `cmd /c StartTrial.cmd --no-gui` rejected missing real provider setup. |
| Source fake trial | PASS | `cmd /c StartFakeTrial.cmd --no-gui` remained visibly fake and bootstrapped no-gui. |

## Selected Spike Shape

P15 will use an explicit package variant plus explicit smoke entry point:

- package variant: `credentials`;
- expected build command: `python scripts\package_windows.py --variant credentials`;
- deterministic dry-run command:
  `python scripts\package_windows.py --dry-run --variant credentials`;
- packaged smoke command:
  `dist\SnapLex\SnapLex.exe --smoke-credentials`;
- optional repeat/restart command:
  `dist\SnapLex\SnapLex.exe --smoke-credentials --smoke-credentials-check-only`.

The variant name is intentionally separate from `base`, `capture`, `ocr`, and
`full`. It should include credential/keyring dependencies only when the
maintainer asks for that variant. The base package remains the deterministic
private-trial smoke path and must not require keyring, provider credentials,
network, screen permissions, model downloads, or API keys.

## Spike Boundaries

The credential-capable path may change only:

- `scripts/package_windows.py` variant choices and dry-run output;
- `packaging/snaplex.spec` hidden imports/excludes for the explicit
  `credentials` variant;
- a SnapLex CLI smoke entry point that calls existing credential service/store
  boundaries;
- deterministic tests and P15 evidence docs.

The credential-capable path must not:

- silently add keyring to the base package;
- store, print, log, screenshot, package, or commit raw credential values;
- create a production release promise;
- perform real provider network calls;
- move provider, credential, settings, trial readiness, OCR, capture, or UI
  business rules into packaging scripts.

## Smoke Data And Credential Rules

P15 credential smoke uses only a throwaway fake value owned by the smoke
process. The value must not appear in command output, docs, tests, screenshots,
logs, config/history files, package resources, or git. The smoke must delete
the credential before finishing unless a restart-readiness round deliberately
uses a two-step save/check/delete sequence with the same throwaway reference.

The reference identifier may be recorded because it is non-secret. The raw
credential value may not be recorded.

## Failure Semantics

P15 evidence may end in PASS, FAIL, BLOCKED, or DEFER:

- PASS: packaged import/backend discovery and credential smoke work with a
  throwaway fake value and cleanup.
- FAIL: packaged keyring modules are present enough to run but save/read/delete
  or restart readiness fails in a concrete way.
- BLOCKED: package build, OS keyring, or execution environment prevents a fair
  packaged smoke.
- DEFER: evidence is insufficient for production hardening despite partial
  success.

Any outcome must preserve the base package path.

## Round 1 Self-Checks

Debug self-check:

- The current change is explained by package spike design and P14 rebaseline.
- Pass, fail-closed, explicit variant, no-secret, and no-production-promise
  states are covered.
- Generated outputs remain ignored and uncommitted.

Architecture self-check:

- P15 avoids silently changing the base package path.
- Credential behavior remains behind `CredentialService` and credential stores.
- Packaging remains a thin variant/hidden-import wrapper and does not own
  provider, credential, settings, history, OCR, capture, or UI business rules.
