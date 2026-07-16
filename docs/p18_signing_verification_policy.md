# P18 Signing Verification Policy

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Status: signing command, verification, and revocation expectations recorded

P18 defines the command shape and evidence expected for a later signed
distribution gate. P18 does not sign production artifacts, require a real
certificate, store signing material, or approve public release.

## Signing Preconditions

Signing may be attempted in a later gate only when all of these are true:

- source commit is clean, pushed, and recorded;
- package variant is explicit: `base` or `credentials`;
- package validation for the same commit and variant has passed;
- artifact label includes product, version or commit, variant, date, and
  distribution status;
- release owner and signing identity are approved;
- certificate custody policy in
  `docs/p18_signing_identity_certificate_custody.md` is satisfied;
- no certificates, private keys, package outputs, logs, screenshots, `.env`
  files, local app data, keyring exports, tester data, or provider secrets are
  staged.

## Signing Command Shape

The expected Windows signing command shape for a future production path is:

```powershell
signtool sign /fd SHA256 /tr <timestamp-url> /td SHA256 `
  /sha1 <approved-certificate-thumbprint> <artifact-path>
```

Allowed future variations:

- `/n <approved-publisher-name>` may replace `/sha1` only if it resolves to one
  approved certificate in the signer environment.
- A hardware token, managed signing service, or non-exportable certificate
  store may provide the key. The private key must not be exported to the repo
  or build tree.
- Timestamp URL must be an approved RFC 3161 timestamp service. A signed
  artifact without timestamp evidence is not ready for broader distribution.

The command must run only against an ignored local artifact path. It must not
write signed binaries, installer files, or command logs into tracked
directories.

## Verification Commands

The verifier must run these checks before any signed artifact is transferred:

```powershell
signtool verify /pa /all /v <artifact-path>
Get-AuthenticodeSignature -FilePath <artifact-path>
Get-FileHash -Algorithm SHA256 -Path <artifact-path>
```

Required verification result:

- signature status is valid;
- signer subject matches the approved SnapLex release owner;
- issuer and thumbprint match the approved certificate record;
- timestamp is present and valid;
- file hash matches the transfer manifest;
- artifact label matches the source commit and package variant;
- package smoke for that artifact lane passes after signing.

If any verification command fails or reports an unknown, mismatched, or
unsigned status, the artifact must not be shared.

## Evidence Record

A later signed distribution gate must record this evidence in a text report:

- source commit hash;
- package variant and artifact label;
- package command used to build the unsigned artifact;
- signing command shape without secrets, PINs, passwords, or private-key
  locations;
- signer subject, issuer, and certificate thumbprint;
- timestamp result;
- SHA256 hash;
- verification command names and PASS/FAIL result;
- package smoke command names and PASS/FAIL result;
- transfer destination class, such as private link or internal archive, without
  public credentials or secret-bearing URLs.

Evidence must not include package binaries, signed binaries, screenshots,
private keys, certificate passwords, token PINs, `.env` files, provider
secrets, tester personal data, or logs with secret-bearing content.

## Revocation Expectations

Distribution must stop and revocation must be considered if:

- certificate private key, token PIN, account recovery path, or certificate
  password is exposed;
- signed artifact hash differs from the approved manifest;
- artifact is signed with the wrong identity or wrong variant label;
- tester or user reports malware warning, tampering, or unexpected publisher
  identity that verification cannot explain;
- credential package smoke reveals secret printing, unsafe cleanup, or keyring
  behavior outside the accepted service boundary.

Revocation response for a later gate:

- pull or disable private transfer links;
- notify testers not to run the affected artifact;
- record affected artifact labels, hashes, and variants;
- contact the certificate authority or managed signing provider when key
  compromise is suspected;
- rebuild from a clean source commit only after custody and verification pass;
- keep the base package deterministic and keyring-free during rollback.

## Round 3 Self-Checks

Debug self-check:

- The policy is explained by the smallest signing workflow: preconditions,
  command shape, verification commands, evidence, and revocation triggers.
- Success, expected rejection, no certificate, skipped signing, verification
  failure, revocation, rollback precursor, and no-secret states are covered.

Architecture self-check:

- Signing and verification wrap artifacts; they do not own provider,
  credential, settings, history, capture, OCR, UI, or trial readiness rules.
- Provider execution remains behind the provider registry and
  `TranslationPipeline`.
- Credential behavior remains behind credential services, stores, provider
  setup, settings, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No production signing, public release, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, or full localization is introduced.
