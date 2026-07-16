# P17 To P18 Handoff

Date: 2026-07-17
Status: P17 planner-accepted; ready for P18 execution

Recommended P18: Signing And Distribution Readiness Gate.

P18 execution guide: `docs/p18_signing_distribution_readiness_gate_goal_guide.md`

P18 TODO: `docs/p18_todo.md`

## P17 Baseline

P17 ran the limited credential package pilot and signing-decision phase without
expanding runtime product scope. The explicit `credentials` package candidate
passed pre-share gate rehearsal, credential smoke, restart readiness, cleanup,
and final validation. The deterministic `base` package remains keyring-free and
was restored locally after credential package smoke.

Final P17 executor artifacts:

- `docs/p17_pilot_lane_plan.md`
- `docs/p17_package_candidate_gate_evidence.md`
- `docs/p17_tester_feedback_intake.md`
- `docs/p17_real_provider_smoke_record.md`
- `docs/p17_artifact_transfer_retention_support.md`
- `docs/p17_signing_installer_updater_decision.md`
- `docs/p17_credential_package_lane_decision.md`
- `docs/p17_boundary_scan_evidence.md`
- `docs/p17_final_validation_report.md`
- `docs/p17_to_p18_handoff.md`

## Validation To Preserve

- `Validate.cmd` PASS with 264 tests.
- `git diff --check` PASS.
- `python -m snaplex --version` PASS.
- `python -m snaplex --no-gui` PASS.
- `python -m snaplex --check-real-provider` expected rejection PASS.
- Base and credentials package dry-runs PASS.
- Credentials package build/import/cycle/save/check-delete PASS.
- Credentials cleanup status PASS, `missing`.
- Final base package restore PASS.
- Base package credential smoke expected rejection PASS.
- `StartTrial.cmd --no-gui` expected rejection PASS.
- `StartFakeTrial.cmd --no-gui` PASS.
- `SmokeTrial.cmd` PASS.
- `StartPackagedFakeTrial.cmd --no-gui` PASS.
- `StartPackagedTrial.cmd --no-gui` expected rejection PASS.
- P9 and P11 GUI smoke PASS with ignored local screenshots.
- P17 docs index, artifact scan, and secret scan PASS.

## Decision Summary

P17 keeps the `credentials` package as a separate explicit private-trial
variant. The base package remains deterministic and keyring-free.

P17 does not approve public release, signed installer, updater, silent
base-package keyring support, SnapLex Cloud, OAuth, billing, hosted token
broker, remote accounts, cloud sync, browser extension runtime, AI summary
runtime, global hotkeys, broad provider rewrites, OCR/capture rewrites, full
localization, or network-required automated tests.

## Known Gaps For P18

- No signed installer or updater exists.
- No code-signing identity, certificate custody, signing verification, or
  revocation workflow is defined.
- No external tester feedback was supplied in P17.
- No real-provider network smoke was run in P17.
- Locked Credential Locker, enterprise-managed keyring policy, unsupported
  backend, and remote-session behavior need real tester matrix evidence.
- Artifact transfer was defined as policy, not executed with external testers.

## Suggested P18 Scope

P18 should decide signing and distribution readiness before any broader
credential package sharing:

- define signing identity and certificate handling policy;
- decide archive versus installer and rollback/update expectations;
- define signed artifact verification and support escalation;
- optionally run an isolated signing rehearsal only if the architect approves;
- keep `base` deterministic and keyring-free;
- keep `credentials` explicit and private-trial until signing/support gates
  pass;
- preserve no-secret, no-artifact, no-network automated validation boundaries.

## Explicit Non-Scope To Preserve

- Public release without a later approval gate.
- Silent keyring inclusion in the base package.
- Production SnapLex Cloud, account OAuth, billing, hosted token broker, remote
  accounts, or cloud sync.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Broad provider rewrites.
- OCR/capture rewrites.
- Full localization.
- Network-required automated tests.
- Raw provider secrets in config, history, docs, tests, logs, screenshots,
  package resources, chat, or git.
- Committed package outputs, screenshots, local app data, `.env`, keyring
  exports, logs, OCR caches, smoke data, tester personal data, or provider
  secrets.
