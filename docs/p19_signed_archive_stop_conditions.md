# P19 Signed Archive Stop Conditions

Date: 2026-07-17
Phase: P19 Signing Rehearsal And Signed Archive Candidate Gate
Status: stop conditions, cleanup, rollback, and support implications recorded

P19 defines the conditions that stop a signed archive rehearsal or candidate
from proceeding. Because P19 signing is SKIPPED, these conditions govern future
work and the decision for any later signed archive gate.

## Immediate Stop Conditions

Stop signing, transfer, or candidate promotion immediately if any of these
occur:

- signing path approval is missing, ambiguous, or contradicted;
- production certificate material is introduced without separate approval;
- certificate, private key, token PIN, password, timestamp response, signing
  log, screenshot, signed binary, signed archive, `.env`, keyring export,
  local app data, smoke data, tester data, OCR cache, or provider secret is
  staged;
- artifact is built from an unpushed or dirty source commit;
- package variant label is missing or wrong;
- `base` package imports keyring or credential-only dependencies;
- `credentials` package smoke prints raw credential values;
- credential cleanup fails or cannot prove cleanup safely;
- signature verification fails, is missing, or refers to the wrong artifact;
- timestamp policy is missing or timestamp result is invalid when timestamp is
  required;
- `StartPackagedTrial.cmd --no-gui` no longer fails closed without real
  provider setup;
- Windows trust, malware, or enterprise policy warnings cannot be explained by
  the accepted trust label;
- tester feedback includes secrets or personal data that cannot be sanitized.

## Cleanup Expectations

After any future signing rehearsal:

- delete or quarantine local signed outputs according to the approved rehearsal
  record;
- preserve only non-secret text evidence in git;
- confirm `git status --short --ignored` shows generated artifacts only in
  ignored local paths;
- confirm signing-material file scans find no tracked `.pfx`, `.p12`, `.pem`,
  `.pvk`, `.spc`, `.cer`, `.crt`, or `.key` files;
- confirm private-key and certificate marker scans find no tracked secret
  material;
- rerun base package credential smoke expected rejection after restoring base;
- rerun credentials package cleanup smoke if the credentials lane is exercised;
- never ask testers to send logs, screenshots, keyring exports, or provider
  secrets.

## Rollback Implications

Rollback is manual archive withdrawal.

If a signed archive candidate is stopped:

- withdraw or disable transfer access;
- notify testers not to run or redistribute the candidate;
- record source commit, artifact label, variant, and non-secret hash when
  available;
- fall back to the last accepted base package lane or an unsigned/private-trial
  archive candidate;
- rebuild only from a clean pushed source commit after validation passes;
- keep local config, history, credential references, and keyring data outside
  package resources;
- do not delete tester user data automatically.

Rollback does not approve an installer, updater, release feed, cloud account,
or automatic repair behavior.

## Support Implications

Support severity for signed archive gates:

- S0 security/privacy: exposed signing material, provider secret, `.env`,
  keyring export, personal data, wrong publisher identity, or malicious
  artifact suspicion.
- S1 release blocker: signing verification mismatch, timestamp failure when
  required, package smoke failure, base imports keyring, credentials cleanup
  uncertain, or trust prompt blocks selected tester lane.
- S2 pilot issue: expected missing-provider rejection, benign trust prompt,
  unclear instructions, device-specific keyring behavior, or documentation gap.

S0 response stops distribution immediately and records only sanitized
non-secret metadata. S1 blocks promotion until fixed or explicitly deferred.
S2 may be documented for follow-up without expanding P19 scope.

## Round 7 Self-Checks

Debug self-check:

- The policy is explained by the smallest stop workflow: missing approval,
  bad artifact, bad signature/timestamp, bad package lane, unsafe cleanup, or
  unsafe feedback stops promotion.
- Success, expected rejection, cleanup, rollback, revocation, support
  escalation, skipped signing, and no-secret states are covered.

Architecture self-check:

- Stop conditions do not change provider, credential, settings, history,
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
