# P17 Package Candidate Pre-Share Gate Evidence

Date: 2026-07-17
Phase: P17 Limited Credential Package Pilot And Signing Decision
Status: pre-share package gate PASS for controlled private-trial candidate

P17 Round 2 rehearsed the P16 pre-share gate from a clean source commit. The
credential-capable package remains explicit as the `credentials` variant, and
the deterministic `base` package remains the default keyring-free control lane.

## Source Commit

Gate source commit:
`c4b8193a7dd748c4a0cdd1287b6de3d9f0a5280f`.

Candidate artifact label for local private-trial handling:
`SnapLex-c4b8193-credentials-20260717-unsigned-private-trial`.

Artifact location during this executor run: local ignored
`dist\SnapLex`. No package output, installer, archive, screenshot, log, local
app data, smoke data, keyring export, `.env`, provider secret, or tester data is
committed.

## Source Gate

Commands and results:

- `git status --short --branch`: PASS, clean at gate start.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS.
- `python -m snaplex --check-real-provider`: expected rejection PASS with
  `Real translation provider is not configured.`
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `python scripts\package_windows.py --dry-run --variant credentials`: PASS.

No real-provider network call was run.

## Base Control Lane

Commands and results:

- `python scripts\package_windows.py --variant base`: PASS.
- `cmd /c SmokeTrial.cmd`: PASS.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`: PASS.
- `cmd /c StartPackagedTrial.cmd --no-gui`: expected rejection PASS.
- `dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import`:
  expected rejection PASS with `keyring is not available in this runtime`.

The base package remained deterministic, fake-smoke capable, real-trial
fail-closed, and keyring-free.

## Credential Candidate Lane

Commands and results:

- `python scripts\package_windows.py --variant credentials`: PASS.
- PyInstaller credential signal: PASS; build output analyzed
  `keyring.backends.Windows`, `hook-keyring.py`, and `hook-pywintypes.py`.
- `dist\SnapLex\SnapLex.exe --version`: PASS, `SnapLex 0.1.0`.
- `dist\SnapLex\SnapLex.exe --no-gui`: PASS.
- `dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import`:
  PASS.
- `dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle`:
  PASS.
- `dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save`:
  PASS.
- `dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete`:
  PASS.
- Source cleanup status check for `snaplex/package-credential-smoke`: PASS,
  `missing`.

Credential smoke backend:
`keyring.backends.Windows.WinVaultKeyring`.

Credential smoke reference:
`snaplex/package-credential-smoke`.

The smoke output did not print a raw credential value. The saved throwaway value
was runtime-generated and was deleted by `check-delete`.

## Pre-Share Decision

The credential candidate is eligible for controlled private-trial handling only
inside the P17 pilot lane. It must remain:

- explicit `credentials` variant only;
- unsigned/private-trial labeled only;
- transferred only after current source, base, credential, artifact, and secret
  gates pass;
- accompanied by tester setup, cleanup, keyring failure, and no-secret feedback
  guidance.

This evidence does not approve public release, signed installer, updater,
silent base-package keyring support, cloud accounts, OAuth, billing, token
broker, browser extension runtime, AI summary runtime, global hotkeys, provider
rewrites, OCR/capture rewrites, or full localization.

## Round 2 Self-Checks

Debug self-check:

- The current result is explained by the smallest package workflow: source gate,
  base control lane, credential candidate lane, restart readiness, and cleanup
  status.
- PASS, expected rejection, no-network, cleanup, unsigned/private-trial, and
  no-secret states are covered.

Architecture self-check:

- The credential package remains explicit and separate from base.
- The base package remains deterministic and keyring-free.
- Credential behavior remains behind `CredentialService`, credential stores,
  and release smoke boundaries.
- Provider behavior remains behind provider registry and `TranslationPipeline`;
  no provider or HTTP code moved into UI or packaging scripts.
- Generated outputs and local smoke data remain ignored local artifacts.
