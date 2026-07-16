# P21 Signing Path Decision

Date: 2026-07-17
Phase: P21 Signing Path Unblock Decision Or Pause Gate
Status: rebaseline complete; decision pending Round 2

P21 decides whether signing is unblocked for a later rehearsal phase or paused
until a human supplies missing safe-path inputs. P21 does not run signing
commands, create/import/purchase/invent/use certificates, call timestamp
services, or create signed artifacts.

## Accepted Baseline Revalidated

P20 remains the accepted baseline for P21:

- accepted P20 commit:
  `0821a109c683e763997ca116c74ffbe2fddfbde9`;
- planner P21 guide commit:
  `ca7a23a3eba01de2e7e43ee1020df6ff323209bc`;
- current P21 dispatch HEAD:
  `6e5b728c8e3a9d7c744e7156624977afc89b2a9e`;
- `main` is aligned with `origin/main`;
- P20 recorded signing path approval as BLOCKED/SKIPPED because no explicit
  safe throwaway/test signing path approval was supplied;
- P20 did not run signing commands, create/import/purchase/invent/use
  certificates, call timestamp services, create signed artifacts, or approve
  public release;
- `signtool.exe` was not discoverable on PATH in P20;
- `Get-AuthenticodeSignature`, `Set-AuthenticodeSignature`, and `Get-FileHash`
  were discoverable in P20;
- `base` remains the deterministic, keyring-free package lane;
- `credentials` remains explicit and private-trial only.

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
present at the start of P21 editing.

## Decision Inputs

P21 may record `UNBLOCKED FOR FUTURE REHEARSAL` only if explicit safe-path
approval and all required inputs are supplied before the decision is made.
Those inputs include:

- approval owner and date;
- signing path type;
- signer identity label;
- proof that no production certificate is used unless separately approved;
- certificate metadata when present;
- private-key custody and cleanup rule;
- ignored local artifact path;
- command shape;
- timestamp policy;
- verification commands;
- evidence retention rule;
- cleanup and boundary scan rule.

Current evidence does not include these inputs. Round 2 will record the formal
P21 decision.

## Round 1 Self-Checks

Debug self-check:

- The result is explained by the smallest P21 starting workflow: accept P20,
  confirm HEAD, confirm deterministic validation, confirm package dry-runs, and
  list decision inputs.
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
