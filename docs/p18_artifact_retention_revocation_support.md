# P18 Artifact Retention, Revocation, And Support Policy

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Status: artifact naming, transfer, retention, revocation, and support recorded

P18 keeps SnapLex distribution in a private-trial archive lane. This policy
defines how package candidates are named, transferred, retained, revoked, and
supported without committing artifacts or secret-bearing evidence.

## Artifact Naming

Use this label shape for any P18 or later private-trial archive candidate:

```text
SnapLex-<version-or-commit>-<variant>-<yyyymmdd>-<signed-status>-private-trial
```

Allowed `variant` values for the current lanes:

- `base`
- `credentials`

Allowed `signed-status` values:

- `unsigned`
- `signed`
- `test-signed`

Rules:

- `credentials` must remain visible in the artifact name when keyring support
  is included.
- `base` must not include keyring support.
- `signed` may be used only after production signing and verification pass.
- `test-signed` may be used only for isolated rehearsal artifacts that are not
  shared as production trust evidence.
- `unsigned` private-trial artifacts must not be described as public release,
  installer-ready, or auto-update-ready.

## Transfer Policy

Private-trial transfer requirements:

- use an access-controlled private link or direct controlled handoff;
- include artifact label, source commit, variant, SHA256 hash, and status;
- include no-secret feedback rules and cleanup instructions;
- never place package outputs, signed artifacts, hashes tied to secret-bearing
  paths, screenshots, logs, local app data, keyring exports, `.env` files,
  tester personal data, or provider secrets in git;
- disable access when the candidate is withdrawn, expired, or superseded.

Transfer is not approved for public download pages, unauthenticated mirrors,
package registries, app stores, or automatic update feeds in P18.

## Retention Policy

Source and policy docs are retained in git.

Generated artifacts are not retained in git. If an artifact is produced for a
private trial, retain it only in an approved ignored local or private transfer
location long enough to complete the pilot, support window, or revocation
decision.

Recommended default retention:

- unsigned private-trial candidate: expire or delete within 14 days after the
  pilot window closes;
- superseded candidate: disable transfer access as soon as replacement is
  announced;
- revoked candidate: disable transfer access immediately and keep only the
  non-secret manifest needed for audit;
- signing rehearsal candidate: delete after evidence is recorded unless a later
  gate approves a private ignored evidence store.

Retained evidence may include source commit, variant, label, hash, verification
status, and support outcome. It must not include binaries, private keys,
certificate passwords, token PINs, screenshots, logs with secrets, raw provider
responses, tester personal data, or keyring exports.

## Revocation Policy

Revoke or withdraw a candidate when:

- signing key or certificate custody is suspected to be compromised;
- artifact hash or variant label does not match evidence;
- signed identity is wrong, missing, expired, or unverifiable;
- base package imports keyring or credential-only dependencies;
- credentials package cleanup fails without a safe environment explanation;
- tester feedback includes secrets or personal data that cannot be safely
  triaged;
- malware, trust prompt, enterprise policy, or tampering reports cannot be
  reconciled with verification evidence.

Revocation actions:

- disable private transfer access;
- mark the artifact label withdrawn in the report;
- notify testers not to run or redistribute the candidate;
- document affected label, source commit, variant, and SHA256 hash;
- notify the certificate authority or managed signing provider when signing key
  compromise is suspected;
- fall back to the last accepted deterministic base lane or a clean replacement
  candidate after validation.

## Support Escalation

Use these support buckets for private-trial reports:

- S0 security/privacy: exposed credential, private key, `.env`, keyring export,
  personal data, malicious artifact suspicion, or wrong publisher identity.
- S1 release blocker: package fails to start, verification mismatch, cleanup
  unsafe, base imports keyring, credentials lane cannot save/delete safely, or
  trust prompt blocks selected tester lane.
- S2 pilot issue: confusing setup, expected missing-provider rejection, benign
  trust prompt, device-specific keyring availability, or documentation gap.

S0 handling:

- stop distribution for affected candidate;
- ask tester not to send more secret-bearing material;
- preserve only non-secret metadata;
- rotate or revoke affected credential or certificate material outside git;
- record sanitized outcome in the phase report.

S1 handling:

- reproduce only with deterministic fake or throwaway credential paths;
- keep logs and screenshots out of git;
- file a follow-up with affected variant, command, and non-secret error
  summary;
- block wider sharing until fixed or explicitly deferred.

S2 handling:

- update tester instructions or docs when appropriate;
- keep private-trial limits visible;
- do not expand P18 scope into installer, updater, account, cloud, or public
  release work.

## Round 7 Self-Checks

Debug self-check:

- The policy is explained by the smallest artifact workflow: name, transfer,
  retain, revoke, support, and fall back.
- Success, expected rejection, cleanup, revocation, support escalation,
  unsigned/signed/test-signed status, and no-secret states are covered.

Architecture self-check:

- Artifact handling does not move provider, credential, settings, history,
  capture, OCR, UI, or trial readiness rules into packaging.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, installer, updater, cloud, OAuth, browser extension, AI
  summary, global hotkey, provider rewrite, OCR/capture rewrite, or full
  localization is introduced.
