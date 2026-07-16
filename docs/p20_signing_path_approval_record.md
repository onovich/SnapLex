# P20 Signing Path Approval Record

Date: 2026-07-17
Phase: P20 Approved Signing Path Acquisition And Rehearsal Setup Gate
Status: BLOCKED/SKIPPED - no explicit safe throwaway/test signing path
approval supplied

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

## P20 Signing Path Approval Decision

Decision: BLOCKED/SKIPPED.

P20 does not have explicit approval for a safe throwaway/test signing path.
Therefore P20 will not run signing commands, generate a self-signed
certificate, import certificate material, call a timestamp service, create
signed artifacts, or verify signatures against signed output.

Reasons:

- P19 was accepted with signing rehearsal SKIPPED because no approved safe
  throwaway/test signing path was supplied.
- The P20 planner dispatch asks the executor not to run signing commands unless
  explicit safe signing path approval and all required safety inputs are
  recorded first.
- The P20 dispatch does not supply a safe signing path type, signer identity,
  certificate source, private-key custody rule, ignored artifact path, command
  shape, timestamp policy, verification evidence policy, or cleanup policy
  sufficient to authorize signing.
- No production certificate is approved, required, or in scope.
- No explicit approval was supplied to generate a local throwaway certificate.
- Committing certificates, private keys, signed binaries, timestamp responses,
  screenshots, logs, package outputs, `.env`, keyring exports, tester data,
  local app data, smoke data, OCR caches, or provider secrets remains
  forbidden.

This BLOCKED/SKIPPED decision is acceptable for P20 as long as approval
requirements, artifact policy, command discovery shape, verification policy,
package lanes, validation, and hygiene gates pass. P20 is an acquisition/setup
gate, not a mandate to invent signing material.

## Future Inputs To Change This Decision

A later round or phase may change this decision only with explicit safe-path
approval that includes:

- approval owner and date;
- signing path type: local throwaway certificate, hardware token test
  certificate, managed signing sandbox, or other safe non-production path;
- signer identity label and proof that it is not a production release
  certificate unless separately approved;
- certificate subject, issuer, and non-secret thumbprint or test identifier
  when present;
- private-key custody rule and cleanup rule;
- ignored local artifact directory for unsigned and signed rehearsal files;
- exact signing and verification commands;
- timestamp policy, including whether timestamp is skipped for local test
  rehearsal or uses an approved test-safe endpoint;
- evidence retention rule that records only non-secret text and hashes;
- post-rehearsal cleanup and boundary scan commands.

Without these inputs, signing remains BLOCKED/SKIPPED.

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

## Round 2 Self-Checks

Debug self-check:

- The decision is explained by the smallest signing-path workflow: required
  approval inputs are missing, so signing is blocked/skipped and package lane
  validation continues.
- Success, expected rejection, missing approval, no certificate, no signing
  command, skipped timestamp, skipped network, cleanup requirement, and
  no-secret states are covered.

Architecture self-check:

- The BLOCKED/SKIPPED decision does not change provider, credential, settings,
  history, capture, OCR, UI, package specification, or trial readiness
  behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
