# P20 Signature Verification Evidence Policy

Date: 2026-07-17
Phase: P20 Approved Signing Path Acquisition And Rehearsal Setup Gate
Status: policy recorded; verification NOT RUN because signing is
BLOCKED/SKIPPED

P20 records how a future approved signing rehearsal must verify signatures,
trust, timestamp, revocation, and evidence retention. Because P20 has no
approved safe throwaway/test signing path, no signed artifact exists and no
signature verification command is run against signed output.

## Current Verification State

Current state: NO SIGNED ARTIFACT.

P20 records verification policy only:

- no certificate was generated, imported, purchased, invented, or used;
- no signing command was run;
- no timestamp service was called;
- no signed binary or archive exists;
- no signature verification output exists;
- no timestamp response, screenshot, log, certificate, private key, signed
  artifact, or package output is committed.

This absence is expected because P20 lacks explicit safe signing-path approval.

## Future Verification Preconditions

A future approved signing rehearsal must satisfy all of these before
verification is considered meaningful:

- source commit is clean and pushed;
- package variant is explicit: `base` or `credentials`;
- package smoke for the same variant passed before signing;
- signing path approval is recorded as APPROVED before signing;
- signing material is throwaway/test-only unless a later gate explicitly
  approves a production certificate;
- signed output lives only under ignored local artifact paths recorded in
  `docs/p20_rehearsal_artifact_directory_policy.md`;
- signing command output is summarized as text without secrets, PINs,
  passwords, private-key paths, timestamp response bodies, logs, screenshots,
  or binary payloads.

## Verification Commands

For a future signed Windows artifact, run:

```powershell
Get-AuthenticodeSignature -FilePath <artifact-path>
Get-FileHash -Algorithm SHA256 -Path <artifact-path>
signtool verify /pa /all /v <artifact-path>
```

`signtool verify` may be replaced only when a later gate records an approved
equivalent verification path. The current P20 command discovery found
`Get-AuthenticodeSignature` and `Get-FileHash`, but did not find `signtool.exe`
on PATH.

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
was BLOCKED/SKIPPED.

## Trust Labels

Trust labels must be explicit:

- `unsigned-private-trial`: no signing trust is claimed;
- `test-signed-private-trial`: signing used throwaway/test material and must
  not be represented as production trust;
- `signed-private-trial`: signing used an approved production or release-owner
  path but still does not imply public release;
- `signed-release-candidate`: requires a later release gate, not P20.

P20 currently supports only `unsigned-private-trial` evidence because signing
is BLOCKED/SKIPPED.

## Timestamp Policy

Timestamp policy for future work:

- production-signed artifacts require an approved RFC 3161 timestamp policy;
- test-signed rehearsal artifacts may skip timestamp only when the rehearsal
  approval says timestamp is intentionally out of scope;
- timestamp service output must be summarized, not committed as raw response
  logs or screenshots;
- timestamp failure blocks signed candidate transfer unless a later gate
  records an explicit test-only exception;
- absence of timestamp policy blocks signing command execution.

P20 does not call a timestamp service.

## Revocation And Withdrawal Policy

Future signed artifacts must be withdrawn or quarantined if:

- the signer identity does not match the approved record;
- certificate or key custody is unclear;
- verification fails or cannot be reproduced;
- timestamp policy is violated;
- signing material, logs, screenshots, timestamp responses, signed binaries, or
  secrets are staged;
- tester feedback reports trust, malware, publisher mismatch, or enterprise
  policy warnings that cannot be explained by the recorded trust label.

For throwaway/test signing, "revocation" means local artifact withdrawal,
cleanup, transfer halt, and evidence update unless a later production signing
gate defines certificate-level revocation.

## Evidence Policy

Allowed text evidence:

- source commit;
- package variant;
- artifact label;
- signing path status;
- signer subject, issuer, and thumbprint when approved and non-secret;
- timestamp status when present;
- SHA256 hash when present;
- verification command names and PASS/FAIL/NOT RUN result;
- package smoke command names and PASS/FAIL result;
- cleanup and boundary scan result.

Forbidden evidence:

- certificates;
- private keys;
- token PINs;
- passwords;
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

- The policy is explained by the smallest verification workflow: signing is
  BLOCKED/SKIPPED, no signed artifact exists, verification is NOT RUN, and
  future verification commands and evidence rules are recorded.
- Success, expected rejection, missing approval, skipped signing, no signed
  artifact, skipped timestamp, verification NOT RUN, withdrawal, revocation,
  and no-secret states are covered.

Architecture self-check:

- Verification policy does not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- Base and credentials package lanes remain separate.
- No production signing, installer, updater, public release, cloud/OAuth,
  browser extension, AI summary, global hotkey, broad provider/OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, signing log, or verification screenshot is introduced.
