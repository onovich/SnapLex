# P18 Signing Identity And Certificate Custody

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Status: round 1 baseline recorded; custody policy pending round 2

P18 decides whether SnapLex is ready to move from an unsigned private-trial
credential package lane toward signed distribution. This document starts with
the accepted P17 baseline and the signing readiness questions that P18 must
answer before any broader distribution decision.

## Accepted Baseline Revalidated

P17 remains the accepted baseline for P18:

- accepted P17 commit:
  `6c7061ad21cbd7b384806a3466f7c31adf8399db`;
- planner P18 guide commit:
  `c8eb59f4b647d905089ff60634d243c01ea408be`;
- current dispatch commit:
  `739ab6a`;
- working tree was clean before P18 round 1 edits;
- `main` was aligned with `origin/main`;
- the deterministic `base` package lane remains keyring-free;
- the explicit `credentials` package lane remains private-trial only;
- no public release, signed installer, updater runtime, cloud account system,
  browser extension runtime, AI summary runtime, global hotkeys, provider
  rewrites, OCR/capture rewrites, or full localization is approved.

Round 1 revalidation results:

- `Validate.cmd` passed with 264 tests.
- `git diff --check` passed.
- `python -m snaplex --version` passed and reported `SnapLex 0.1.0`.
- `python -m snaplex --no-gui` passed.
- `python -m snaplex --check-real-provider` rejected missing real provider
  setup as expected.
- `python scripts\package_windows.py --dry-run --variant base` passed.
- `python scripts\package_windows.py --dry-run --variant credentials` passed.

## Signing Readiness Questions

P18 must answer these questions before SnapLex can move beyond the unsigned
private-trial lane:

- What legal or organizational identity owns signed SnapLex artifacts?
- Who is allowed to request, approve, perform, and verify signing?
- Where is the certificate stored, and what private-key custody rule prevents
  export, screenshots, logs, package resources, or git history exposure?
- Which artifacts are eligible for signing: archive only, installer only, or
  both?
- What exact signing command and timestamp policy will be used once a real
  certificate is approved?
- What verification command must pass before an artifact can be shared?
- What revocation trigger stops distribution after a suspected signing or
  package compromise?
- How is the credential-capable package labelled so testers can distinguish
  unsigned, signed, private-trial, and future release candidates?
- What rollback path exists if a signed package fails smoke, verification,
  trust prompt review, or credential cleanup?
- What support escalation path exists when testers report Windows trust
  prompts, keyring failures, cleanup failures, or accidental secret exposure?
- What evidence is required before P19 may consider a signed distribution
  readiness gate?

## Round 1 Self-Checks

Debug self-check:

- The current result is explained by the smallest baseline workflow: preserve
  P17, confirm source validation, confirm deterministic package dry-runs, and
  list the signing decisions P18 must close.
- Success, expected rejection, no certificate, skipped network, and no-secret
  states are represented.

Architecture self-check:

- Signing policy remains outside provider, credential, settings, history,
  capture, OCR, and UI business rules.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No cloud, OAuth, billing, token broker, browser extension, AI summary,
  global hotkey, provider rewrite, OCR/capture rewrite, full localization,
  signed artifact, installer, updater, certificate, or private key is added.
