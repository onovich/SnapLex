# P20 Final Validation Report

Date: 2026-07-17
Phase: P20 Approved Signing Path Acquisition And Rehearsal Setup Gate
Status: PASS - ready for planner check
Final commit: recorded in READY_FOR_CHECK planner notification after final
report commit
Push: PASS, `origin/main`
Rounds used: 12
Buffer consumed: 3 rounds, rounds 9-11

## Main Deliverables

- `docs/p20_signing_path_approval_record.md`
- `docs/p20_rehearsal_artifact_directory_policy.md`
- `docs/p20_signing_command_discovery.md`
- `docs/p20_isolated_rehearsal_evidence.md`
- `docs/p20_signature_verification_evidence_policy.md`
- `docs/p20_base_package_control_evidence.md`
- `docs/p20_credentials_package_control_evidence.md`
- `docs/p20_boundary_scan_evidence.md`
- `docs/p20_validation_precheck_evidence.md`
- `docs/p20_final_validation_report.md`
- `docs/p20_to_p21_handoff.md`

## Signing Path Approval

Decision: BLOCKED/SKIPPED.

P20 does not have explicit approval for a safe throwaway/test signing path.
Therefore no signing command was run. No self-signed certificate was generated,
no certificate was imported, no production certificate was used, no timestamp
service was called, no signed artifact was created, and no signature
verification command was run against signed output.

P20 records the future approval inputs required before signing can proceed:
approval owner and date, signing path type, signer identity, certificate
metadata, private-key custody, ignored local artifact path, command shape,
timestamp policy, verification commands, evidence retention, cleanup, and
boundary scan rules.

## Artifact And Evidence Policy

P20 records future local-only artifact directories under ignored
`tmp\p20-signing-rehearsal\` paths. Because signing is BLOCKED/SKIPPED, no
rehearsal artifact directory or signing output was created for this phase.

Tracked evidence is limited to sanitized Markdown policy and validation
results. Certificates, private keys, signed binaries, package outputs,
timestamp responses, screenshots, logs, `.env`, keyring exports, tester data,
local app data, smoke data, OCR caches, and provider secrets remain forbidden.

## Command Discovery

P20 command discovery found:

- `signtool.exe`: not discoverable on PATH;
- `Get-AuthenticodeSignature`: available;
- `Set-AuthenticodeSignature`: available;
- `Get-FileHash`: available.

This does not fail P20 because signing remains BLOCKED/SKIPPED. Future signing
still requires explicit safe-path approval before command execution.

## Rehearsal And Verification

Signing rehearsal status: BLOCKED/SKIPPED.

Signature verification status: NOT RUN because no signed artifact exists.

P20 records future verification, trust label, timestamp, revocation, withdrawal,
and evidence policy in
`docs/p20_signature_verification_evidence_policy.md`.

Current trust label: `unsigned-private-trial`.

## Base Package Control

Decision: PASS.

The deterministic `base` package lane remains fake-smoke capable,
real-provider fail-closed, and keyring-free. Base package credential smoke
continues to reject keyring with `keyring is not available in this runtime`.

## Credentials Package Control

Decision: PASS for explicit private-trial package lane.

The `credentials` variant was built explicitly and passed credential smoke for
import, cycle, save, and check-delete. Smoke output records only the non-secret
reference identifier `snaplex/package-credential-smoke`; cleanup passed. The
local package output was restored to `base` afterward, and restored base
credential smoke rejected keyring as expected.

## Validation Commands And Results

- `Validate.cmd`: PASS, 264 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS.
- `python -m snaplex --check-real-provider`: PASS as expected rejection;
  missing real provider setup was rejected.
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `python scripts\package_windows.py --dry-run --variant credentials`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: PASS as expected rejection; missing real
  provider setup was rejected.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS.
- `cmd /c SmokeTrial.cmd`: PASS, including base package dry-run/build path and
  packaged workflow smoke.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`: PASS.
- `cmd /c StartPackagedTrial.cmd --no-gui`: PASS as expected rejection;
  missing real provider setup was rejected.
- Base package credential smoke: PASS as expected rejection,
  `keyring is not available in this runtime`.
- Credentials package build: PASS, recorded in
  `docs/p20_credentials_package_control_evidence.md`.
- Credentials package `import`: PASS, WinVault keyring backend discovered,
  recorded in `docs/p20_credentials_package_control_evidence.md`.
- Credentials package `cycle`: PASS, save/read/delete and cleanup passed,
  recorded in `docs/p20_credentials_package_control_evidence.md`.
- Credentials package `save`: PASS, recorded in
  `docs/p20_credentials_package_control_evidence.md`.
- Credentials package `check-delete`: PASS, restart readiness and cleanup
  passed, recorded in `docs/p20_credentials_package_control_evidence.md`.
- Final base package restore: PASS, recorded in
  `docs/p20_credentials_package_control_evidence.md`.
- Final restored base credential smoke: PASS as expected rejection.
- `python scripts\p9_gui_smoke.py`: PASS, screenshots saved under ignored
  smoke data.
- `python scripts\p11_visible_gui_smoke.py`: PASS, screenshots saved under
  ignored smoke data.
- P20 docs link/index check: PASS.
- Signing rehearsal verification: BLOCKED/SKIPPED/NOT RUN because no approved
  safe signing path or signed artifact exists.

## Boundary And Secret Scan

P20 boundary scan: PASS.

Evidence:

- ignored local outputs only: `.codex/Role.md`, caches, `build/`, `dist/`,
  `snaplex-smoke-data/`, `snaplex.egg-info/`, and `tmp/`;
- no unignored signing-material file matches for `.pfx`, `.p12`, `.pem`,
  `.pvk`, `.spc`, `.cer`, `.crt`, or `.key`;
- no unignored package/log/screenshot artifact matches for `.exe`, `.msi`,
  `.zip`, `.7z`, `.log`, `.png`, `.jpg`, or `.jpeg`;
- no private-key blocks, certificate blocks, or raw OpenAI-style secret token
  markers found outside documentation allowlists;
- broad policy keyword matches were documentation/source references only;
- no certificate, private key, signed binary, timestamp response, screenshot,
  log, `.env`, keyring export, tester personal data, local app data, smoke
  data, OCR cache, provider secret, or package output was committed.

## Known Limitations

- No approved safe throwaway/test signing path exists.
- No production signing identity, certificate custody execution path, or
  production certificate exists.
- `signtool.exe` is not currently discoverable on PATH.
- Signing rehearsal and signature verification were BLOCKED/SKIPPED/NOT RUN;
  no signed artifact, timestamp response, trust prompt evidence, or verification
  output exists.
- No signed archive candidate is approved for production, transfer, or public
  release.
- No installer, updater, release feed, public support channel, or public release
  path exists.
- No external P20 tester feedback was supplied.
- No real-provider network smoke was run because credentials and explicit human
  network approval were not supplied.
- Broader Credential Locker/keyring device matrix evidence remains limited.

## Recommended Next Phase

Recommended P21: signing path unblock decision or pause signing work.

If an explicit safe throwaway/test signing path is approved, P21 should run a
narrow local-only rehearsal setup using ignored artifact paths, then verify
signature, timestamp policy, trust label, cleanup, and boundary scans without
committing binaries or secrets.

If no signing path is approved, P21 should keep signing blocked and continue
private-trial archive operations without producing signed artifacts.

## Round 12 Self-Checks

Debug self-check:

- The final result is explained by the smallest P20 workflow: rebaseline,
  signing approval decision, artifact policy, command discovery, blocked
  rehearsal evidence, verification policy, base package evidence, credentials
  package evidence, boundary scans, validation precheck, final report, and
  handoff.
- Success, expected rejection, missing approval, skipped signing, no
  certificate, no signed artifact, no timestamp response, cleanup, rollback,
  support, no-secret, and no-public-release states are covered.

Architecture self-check:

- Signing and distribution policy wraps package artifacts and does not move
  provider, credential, settings, history, capture, OCR, UI, package
  specification, or trial readiness business rules.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, or full localization is introduced.
