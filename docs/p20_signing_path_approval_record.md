# P20 Signing Path Approval Record

Date: 2026-07-17
Phase: P20 Approved Signing Path Acquisition And Rehearsal Setup Gate
Status: rebaseline complete; approval decision pending Round 2

P20 decides whether SnapLex has explicit approval for a safe throwaway/test
signing path. Round 1 revalidates the accepted P19 baseline and records the
approval inputs that must exist before any signing command can run.

No signing command runs in Round 1. No certificate is created, imported,
purchased, invented, or used. No signed binary, package output, timestamp
response, screenshot, log, `.env`, keyring export, tester data, local app data,
smoke data, OCR cache, provider secret, private key, or signing material is
committed.

## Accepted Baseline Revalidated

P19 remains the accepted baseline for P20:

- accepted P19 commit:
  `11001b64a4b5e093c7ee57615e7e5dbbb288749f`;
- planner P20 guide commit:
  `b63588c44ec760344a5be15edfac6b3e487bcfb2`;
- current Round 1 HEAD:
  `a0a08e3c4bc7d753607b830fae3e729c19aa08b3`;
- `main` is aligned with `origin/main`;
- `base` remains the deterministic, keyring-free package lane;
- `credentials` remains explicit and private-trial only;
- P19 recorded signing rehearsal as SKIPPED because no approved safe
  throwaway/test signing path was supplied;
- P19 did not run signing commands, create signed artifacts, introduce a
  production certificate path, or approve public release.

Round 1 revalidation results:

- `Validate.cmd` passed with 264 tests.
- `git diff --check` passed.
- `python -m snaplex --version` passed and reported `SnapLex 0.1.0`.
- `python -m snaplex --no-gui` passed.
- `python -m snaplex --check-real-provider` rejected missing real provider
  setup as expected.
- `python scripts\package_windows.py --dry-run --variant base` passed.
- `python scripts\package_windows.py --dry-run --variant credentials` passed.

## Local Ignored Artifact State

`git status --short --ignored` showed only ignored local outputs and caches:

- `.codex/Role.md`
- `.mypy_cache/`
- `.pytest_cache/`
- `.ruff_cache/`
- `build/`
- `dist/`
- `scripts/__pycache__/`
- `snaplex-smoke-data/`
- `snaplex.egg-info/`
- package `__pycache__/` directories
- `tests/__pycache__/`
- `tmp/`

No nonignored package output, signing material, certificate, private key,
signed binary, timestamp response, screenshot, log, `.env`, keyring export,
tester data, local app data, smoke data, OCR cache, or provider secret was
present at the start of P20 editing.

## Required Approval Inputs

P20 may mark signing as APPROVED only when all of these are recorded before any
signing command runs:

- explicit human/architect approval for a safe throwaway/test signing path;
- confirmation that no production certificate is being used unless separately
  approved outside P20;
- signing path type, such as local throwaway certificate, hardware token test
  certificate, managed signing sandbox, or another safe non-production path;
- signer identity label, certificate subject or test identity, issuer, and
  non-secret thumbprint or identifier when present;
- private-key custody rule and cleanup rule;
- ignored local artifact directory for unsigned and signed rehearsal outputs;
- command discovery result and exact signing command shape;
- timestamp policy, including whether timestamping is skipped for local
  throwaway rehearsal or uses an approved safe endpoint;
- verification commands and expected evidence;
- evidence retention rule that keeps only non-secret text and hashes in git;
- post-rehearsal cleanup and boundary scan commands.

Current evidence does not include explicit approval for a safe signing path.
Round 2 will record the formal P20 approval decision.

## Round 1 Self-Checks

Debug self-check:

- The result is explained by the smallest P20 starting workflow: accept P19,
  confirm HEAD, confirm deterministic validation, confirm package dry-runs, and
  list approval inputs.
- Success, expected rejection, missing approval, ignored local output,
  no-certificate, no-signing-command, no-artifact, and no-secret states are
  covered.

Architecture self-check:

- Rebaseline work does not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
