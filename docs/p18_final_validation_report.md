# P18 Final Validation Report

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Status: PASS
Final commit: recorded in READY_FOR_CHECK planner notification after final
report commit
Push: PASS, `origin/main`
Rounds used: 12
Buffer consumed: 3 rounds, rounds 9-11

## Main Deliverables

- `docs/p18_signing_identity_certificate_custody.md`
- `docs/p18_signing_verification_policy.md`
- `docs/p18_signing_rehearsal_record.md`
- `docs/p18_archive_installer_readiness_decision.md`
- `docs/p18_rollback_update_policy.md`
- `docs/p18_artifact_retention_revocation_support.md`
- `docs/p18_distribution_readiness_decision.md`
- `docs/p18_boundary_scan_evidence.md`
- `docs/p18_package_validation_evidence.md`
- `docs/p18_final_validation_report.md`
- `docs/p18_to_p19_handoff.md`

## Signing Identity And Certificate Custody

P18 records the signing identity and certificate custody policy without
requesting, requiring, inventing, importing, or committing a production
certificate.

The future signed artifact publisher must be the approved SnapLex release
owner. Private keys must remain in a non-exportable local certificate store,
hardware token, or managed signing service approved by a later gate. CI signing
is not approved in P18.

## Signing Verification

P18 records the future Windows signing command shape, timestamp requirement,
verification commands, verification evidence, and revocation triggers.

No signing command was run for production artifacts in P18.

## Signing Rehearsal

Status: SKIPPED.

Reason: no approved safe throwaway/test signing path was supplied, and P18 must
not require or invent a real code-signing certificate. No signed binary,
certificate, private key, signing log, timestamp response, or verification
screenshot was created or committed.

## Archive Versus Installer

Decision: archive lane only.

P18 does not approve a Windows installer, updater runtime, public release, or
automatic update feed. Archive candidates must keep variant labels explicit and
must remain private-trial unless a later gate approves broader distribution.

## Rollback And Update Policy

P18 records manual archive replacement as the only current update path.

Rollback triggers include package smoke failure, signing verification mismatch,
base package keyring import, credential cleanup uncertainty, secret-bearing
feedback, and unexplained trust or policy blocks.

## Artifact Retention, Revocation, And Support

P18 records artifact naming, private transfer, finite retention, revocation,
and support escalation policy.

Support buckets:

- S0 security/privacy;
- S1 release blocker;
- S2 pilot issue.

Generated package outputs, signed artifacts, screenshots, logs, keyring
exports, local app data, tester data, and provider secrets remain out of git.

## Distribution Readiness Decision

Decision: conditionally ready for a later signing gate, not ready for public
release.

Allowed after P18:

- continue controlled private-trial archive handling;
- proceed to a later isolated signing/distribution gate if a safe signing path
  is approved;
- preserve base and credentials package validation lanes.

Not allowed after P18:

- public release;
- production signing with an unapproved certificate;
- installer or updater runtime;
- silent keyring support in the base package;
- SnapLex Cloud, account OAuth, billing, hosted token broker, remote accounts,
  cloud sync, browser extension runtime, AI summary runtime, global hotkeys,
  broad provider rewrites, OCR/capture rewrites, or full localization.

## Validation Commands And Results

- `Validate.cmd`: PASS, 264 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS.
- `python -m snaplex --check-real-provider`: PASS as expected rejection;
  missing real provider setup rejected.
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `python scripts\package_windows.py --dry-run --variant credentials`: PASS.
- Base package build: PASS.
- `cmd /c SmokeTrial.cmd`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: PASS as expected rejection.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`: PASS.
- `cmd /c StartPackagedTrial.cmd --no-gui`: PASS as expected rejection.
- Base package credential smoke: PASS as expected rejection,
  `keyring is not available in this runtime`.
- Credentials package build: PASS.
- Credentials package `import`: PASS, WinVault keyring backend discovered.
- Credentials package `cycle`: PASS, save/read/delete and cleanup passed.
- Credentials package `save`: PASS.
- Credentials package `check-delete`: PASS, restart readiness and cleanup
  passed.
- Final base package restore: PASS.
- Final restored base credential smoke: PASS as expected rejection.
- `python scripts\p9_gui_smoke.py`: PASS, screenshots saved under ignored
  smoke data.
- `python scripts\p11_visible_gui_smoke.py`: PASS, screenshots saved under
  ignored smoke data.
- P18 docs link/index check: PASS.

## Boundary And Secret Scan

P18 boundary scan: PASS.

Evidence:

- ignored local outputs only: caches, `build/`, `dist/`, `snaplex-smoke-data/`,
  and `tmp/`;
- no tracked signing-material file matches for `.pfx`, `.p12`, `.pem`, `.pvk`,
  `.spc`, `.cer`, `.crt`, or `.key`;
- no tracked package/log/screenshot artifact matches for `.exe`, `.msi`,
  `.zip`, `.7z`, `.log`, `.png`, `.jpg`, or `.jpeg`;
- no private-key blocks, certificate blocks, or raw OpenAI-style secret token
  markers found outside documentation allowlists;
- broad policy keyword matches were documentation/source references only.

## Known Limitations

- No production signing identity or certificate custody execution path exists.
- Signing rehearsal was skipped because no approved safe throwaway/test signing
  path was supplied.
- No signed artifact verification evidence exists.
- No installer, updater, release feed, public support channel, or public
  release path exists.
- No external P18 tester feedback was supplied.
- No real-provider network smoke was run because credentials and explicit human
  network approval were not supplied.
- Locked Credential Locker, enterprise-managed keyring policy, unsupported
  backend, remote-session behavior, and broader tester device matrix evidence
  remain limited.

## Recommended Next Phase

Recommended P19: signing rehearsal and signed archive candidate gate.

P19 should remain isolated, no-secret, no-artifact-in-git, and deterministic by
default. It should approve a safe throwaway/test signing path before any
signing rehearsal, keep `base` deterministic and keyring-free, keep
`credentials` explicit and private-trial, and avoid public release unless a
later release gate approves it.

## Round 12 Self-Checks

Debug self-check:

- The final result is explained by the smallest P18 workflow: policy decisions,
  skipped signing rehearsal, package lane validation, boundary scans, final
  report, and handoff.
- Success, expected rejection, no certificate, skipped signing, skipped
  network, cleanup, rollback, revocation, support, and no-secret states are
  covered.

Architecture self-check:

- Signing and distribution policy wraps artifacts and does not move provider,
  credential, settings, history, capture, OCR, UI, package specification, or
  trial readiness business rules.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, or full localization is introduced.
