# P18 Signing Identity And Certificate Custody

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Status: signing identity and certificate custody policy recorded

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

## Signing Identity Policy

P18 does not create, request, require, or invent a production code-signing
certificate. A later signed distribution gate may proceed only after the
signing identity is approved outside the build scripts and recorded in release
planning.

Required identity decisions before signed distribution:

- The signed artifact publisher must be the approved SnapLex release owner,
  not an executor machine, tester, CI worker name, or informal local alias.
- The public publisher display name must be recorded before any signed
  external artifact is shared.
- The release owner must approve which package lane may be signed:
  deterministic `base`, explicit `credentials`, or both as separate artifacts.
- A signing operator may run the signing command only for a clean source commit
  that has passed the package gate for the same variant.
- A verifier distinct from the signing action must record verification output
  before transfer. For a one-person project, this can be a separate manual
  verification step with command output recorded, but it must not be skipped.

Signed artifacts must keep variant clarity in the file name and release notes.
Signing does not merge the `credentials` lane into `base`, imply public
release, or approve installer/updater runtime.

## Certificate Custody Policy

Production certificate custody requirements:

- Private keys must never be committed, copied into package resources, pasted
  into docs, exported into logs, attached to feedback, or captured in
  screenshots.
- The private key must be held by a non-exportable local certificate store,
  hardware token, or managed signing service approved for release use.
- Plain `.pfx`, `.p12`, `.pem`, `.key`, `.crt`, `.cer`, `.spc`, `.pvk`, and
  similar signing material files are forbidden in the repository, build
  outputs committed to git, issue attachments, and tester feedback.
- CI signing is not approved in P18. A later phase must define secure runner,
  secret storage, audit, and revocation behavior before any automated signing.
- Test certificates are allowed only for an isolated rehearsal when they are
  locally generated or already available as throwaway material, never shared as
  production trust evidence, and never committed.
- Certificate passwords, hardware-token PINs, and account recovery material
  must not appear in command history, docs, logs, screenshots, package
  metadata, or chat handoff text.

Release evidence may record certificate subject, issuer, thumbprint, signing
time, timestamp server result, and verification status, but it must not include
private-key material or credential secrets.

## Custody Stop Conditions

Stop signing or distribution work immediately if any of these occur:

- private key or certificate password appears in git, package resources, docs,
  logs, screenshots, tester feedback, or chat;
- the signing identity cannot be matched to an approved release owner;
- the signing operator cannot prove the source commit and variant that were
  signed;
- verification output is missing, ambiguous, or for a different artifact;
- the credential-capable package is presented as base, public, installer-ready,
  or auto-update-ready without a later gate.

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

## Round 2 Self-Checks

Debug self-check:

- The current policy is explained by the smallest custody workflow: approved
  release owner, explicit signer, separate verifier, non-exportable key
  storage, and stop conditions.
- Success, no certificate, skipped signing, revocation precursor, and
  no-secret states are represented.

Architecture self-check:

- Certificate custody does not move provider, credential, settings, history,
  capture, OCR, UI, or trial readiness rules into packaging.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No production certificate, signed binary, installer, updater, cloud account
  system, OAuth, browser extension, AI summary, global hotkey, provider
  rewrite, OCR/capture rewrite, or full localization is introduced.
