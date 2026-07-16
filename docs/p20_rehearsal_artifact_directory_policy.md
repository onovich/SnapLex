# P20 Rehearsal Artifact Directory Policy

Date: 2026-07-17
Phase: P20 Approved Signing Path Acquisition And Rehearsal Setup Gate
Status: policy recorded; signing remains BLOCKED/SKIPPED

P20 defines where future signing rehearsal outputs may live if a safe
throwaway/test signing path is approved later. Because P20 currently has no
explicit safe signing-path approval, this document is policy only and no
signing artifact is created.

## Approved Local-Only Directories

Future signing rehearsal outputs may use only ignored local directories:

- `tmp\p20-signing-rehearsal\`
- `tmp\p20-signing-rehearsal\unsigned\`
- `tmp\p20-signing-rehearsal\signed\`
- `tmp\p20-signing-rehearsal\evidence-local\`

These paths are covered by the repository's existing `tmp/` ignore rule.

Package build outputs remain limited to already ignored packaging paths:

- `build\`
- `dist\`
- `snaplex-smoke-data\`

No rehearsal output may be copied into tracked docs, source directories,
package resources, screenshots folders, or release/archive folders.

## Directory Preconditions

Before any future approved rehearsal runs:

- `git status --short --branch` must show no tracked edits except current
  intended docs;
- the source commit must be pushed;
- the package variant must be explicit: `base` or `credentials`;
- the package smoke for that variant must pass before signing;
- the artifact path must be under `tmp\p20-signing-rehearsal\`;
- the signing path approval record must list signer identity, custody,
  timestamp policy, command shape, verification commands, and cleanup rules.

If any precondition is missing, signing remains BLOCKED/SKIPPED.

## Evidence Retention

Allowed tracked evidence:

- source commit;
- package variant;
- artifact label;
- signing path status;
- command names and PASS/FAIL/SKIPPED results;
- non-secret signer subject, issuer, and thumbprint when explicitly approved;
- SHA256 hash of a future local-only rehearsal artifact;
- verification result summary;
- cleanup and boundary scan result.

Forbidden tracked evidence:

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
- local app data;
- smoke data;
- tester personal data;
- OCR caches;
- provider secrets;
- raw command transcripts containing paths or values that expose signing
  material.

## Cleanup Policy

After any future approved local rehearsal:

- delete local unsigned and signed rehearsal outputs from
  `tmp\p20-signing-rehearsal\`, or explicitly quarantine them outside the repo;
- retain only sanitized Markdown evidence in git;
- rerun `git status --short --ignored`;
- run signing-material scans for `.pfx`, `.p12`, `.pem`, `.pvk`, `.spc`,
  `.cer`, `.crt`, and `.key`;
- run private-key and certificate marker scans;
- restore the local `dist\SnapLex` output to the deterministic `base` package;
- rerun base package credential smoke expected rejection.

Cleanup failure blocks any signed archive candidate and must be recorded as
S1 or S0 depending on whether signing material, secrets, or personal data are
involved.

## Stop Conditions

Stop immediately if:

- artifact output resolves outside `tmp\p20-signing-rehearsal\`;
- signing material appears in tracked files;
- a production certificate is used without separate approval;
- a timestamp response, screenshot, log, signed binary, or signed archive is
  staged;
- package smoke fails;
- base package credential smoke imports keyring;
- credential cleanup fails;
- the evidence policy cannot be followed without exposing secret material.

## Round 3 Self-Checks

Debug self-check:

- The policy is explained by the smallest artifact workflow: future local
  outputs stay under ignored `tmp`, generated package outputs stay under
  ignored package paths, and tracked evidence stays sanitized text only.
- Success, expected rejection, missing approval, cleanup, no-secret,
  no-artifact, and boundary scan states are covered.

Architecture self-check:

- Artifact directory policy does not change provider, credential, settings,
  history, capture, OCR, UI, package specification, or trial readiness
  behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- Base and credentials package lanes remain separate.
- No production signing, installer, updater, public release, cloud/OAuth,
  browser extension, AI summary, global hotkey, broad provider/OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
