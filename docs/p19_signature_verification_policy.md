# P19 Signature Verification, Trust, Timestamp, And Evidence Policy

Date: 2026-07-17
Phase: P19 Signing Rehearsal And Signed Archive Candidate Gate
Status: verification policy recorded; no signed artifact exists in P19

P19 records how a future signed archive rehearsal or candidate must be verified.
Because the P19 signing path is SKIPPED, no signed artifact exists and no
signature verification command is run against a signed output.

## Current P19 Verification State

Current state: NO SIGNED ARTIFACT.

P19 records verification policy only:

- no certificate was generated, imported, purchased, or used;
- no signing command was run;
- no timestamp service was called;
- no signed binary or archive exists;
- no signature verification output exists;
- no timestamp response, screenshot, log, certificate, private key, signed
  artifact, or package output is committed.

This absence is expected because P19 lacks an approved safe throwaway/test
signing path.

## Future Verification Preconditions

A later approved signing rehearsal or signed archive candidate must satisfy all
of these before verification is considered meaningful:

- the artifact was built from a clean pushed source commit;
- package variant is explicit: `base` or `credentials`;
- package smoke for the same variant passed before signing;
- signing path approval is recorded before signing;
- signing material is throwaway/test-only unless a later gate explicitly
  approves a production certificate;
- signed output lives only in an ignored local artifact path;
- signing command output is summarized in text without secrets, PINs,
  passwords, private-key paths, or binary payloads.

## Verification Commands

For a future signed Windows artifact, run:

```powershell
signtool verify /pa /all /v <artifact-path>
Get-AuthenticodeSignature -FilePath <artifact-path>
Get-FileHash -Algorithm SHA256 -Path <artifact-path>
```

Expected PASS criteria:

- signature status is valid for the intended trust scope;
- signer subject matches the approved rehearsal or release identity;
- issuer and thumbprint match the approved signing-path record;
- SHA256 hash matches the evidence manifest;
- artifact label matches source commit, package variant, and signed/test-signed
  status;
- package smoke still passes after signing;
- no certificate, private key, signed artifact, timestamp response, screenshot,
  log, `.env`, keyring export, tester data, local app data, smoke data, OCR
  cache, or provider secret is staged.

If no signed artifact exists, record verification as NOT RUN because signing
was SKIPPED.

## Trust Policy

Trust labels must be explicit:

- `unsigned-private-trial`: no signing trust is claimed;
- `test-signed-private-trial`: signing used throwaway/test material and must
  not be represented as production trust;
- `signed-private-trial`: signing used an approved production or release-owner
  path but still does not imply public release;
- `signed-release-candidate`: requires a later release gate, not P19.

P19 only supports `unsigned-private-trial` evidence because signing is SKIPPED.

## Timestamp Policy

Timestamp policy for future work:

- production-signed artifacts require an approved RFC 3161 timestamp policy;
- test-signed rehearsal artifacts may skip timestamp only when the rehearsal
  approval says timestamp is intentionally out of scope;
- timestamp service output must be summarized, not committed as raw response
  logs or screenshots;
- timestamp failure blocks signed candidate transfer unless a later gate
  records an explicit test-only exception.

P19 does not call a timestamp service.

## Evidence Policy

Allowed text evidence:

- source commit;
- package variant;
- artifact label;
- signing path status;
- signer subject, issuer, and thumbprint when present;
- timestamp status when present;
- SHA256 hash when present;
- verification command names and PASS/FAIL/NOT RUN result;
- package smoke command names and PASS/FAIL result;
- cleanup and boundary scan result.

Forbidden evidence:

- certificates;
- private keys;
- signed binaries;
- signed archives;
- timestamp responses;
- screenshots;
- logs;
- `.env` files;
- keyring exports;
- tester personal data;
- local app data;
- smoke data;
- OCR caches;
- provider secrets.

## Round 6 Self-Checks

Debug self-check:

- The policy is explained by the smallest verification workflow: no signed
  artifact exists, so verification is NOT RUN, while future commands and
  evidence rules are recorded.
- Success, expected rejection, skipped signing, no signed artifact, skipped
  timestamp, verification NOT RUN, and no-secret states are covered.

Architecture self-check:

- Verification policy does not change provider, credential, settings, history,
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
