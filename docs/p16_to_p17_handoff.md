# P16 To P17 Handoff

Date: 2026-07-17
Status: P16 planner-accepted; ready for P17 execution

Recommended P17: Limited Credential Package Pilot And Signing Decision.

P17 execution guide:
`docs/p17_limited_credential_package_pilot_signing_decision_goal_guide.md`

P17 TODO: `docs/p17_todo.md`

## P16 Baseline

P16 hardened the explicit credential-capable package path while preserving the
deterministic base package. The `credentials` variant now has phase-neutral
smoke identifiers, deterministic failure wrapping, tester-facing setup and
cleanup guidance, keyring failure-mode policy, release gates, artifact policy,
and a production-hardening decision.

Final P16 executor artifacts:

- `docs/p16_base_package_preservation_evidence.md`
- `docs/p16_credentials_variant_hardening.md`
- `docs/p16_credential_smoke_hardening.md`
- `docs/p16_tester_setup_cleanup_guide.md`
- `docs/p16_keyring_failure_modes.md`
- `docs/p16_release_gate_artifact_policy.md`
- `docs/p16_production_hardening_decision.md`
- `docs/p16_boundary_scan_evidence.md`
- `docs/p16_final_validation_report.md`

## Validation To Preserve

- `Validate.cmd` PASS with 264 tests.
- `git diff --check` PASS.
- `python -m snaplex --version` PASS.
- `python -m snaplex --no-gui` PASS.
- `python -m snaplex --check-real-provider` expected rejection PASS.
- Base and credentials package dry-runs PASS.
- Base package fake smoke PASS.
- Base package real trial expected rejection PASS.
- Base package credential smoke expected rejection PASS.
- Credentials package import/cycle/save/check-delete PASS.
- Credentials smoke cleanup status PASS, `missing`.
- P9 and P11 GUI smoke PASS with ignored local screenshots.
- P16 docs index, artifact scan, and secret scan PASS after final docs.

## Decision Summary

P16 approves limited private tester distribution of the explicit unsigned
`credentials` package candidate under the P16 release gate.

P16 does not approve public release, signed installer or updater, default/base
package keyring support, SnapLex Cloud, OAuth, billing, token broker, remote
accounts, cloud sync, browser extension runtime, AI summary runtime, global
hotkeys, broad provider rewrites, OCR/capture rewrites, full localization, or
network-required automated tests.

## Suggested P17 Scope

P17 should execute the first limited credential package pilot:

- choose a small controlled private tester lane;
- build the explicit `credentials` variant from a clean source commit;
- label the package as unsigned private-trial only;
- run P16 source, base lane, and credential lane gates before sharing;
- collect no-secret tester feedback using P16 setup and failure-mode guidance;
- record optional real-provider smoke only when local credentials already exist
  and the human explicitly approves network use;
- decide whether credentials stay a separate variant;
- define signing/installer/updater requirements or defer them with evidence;
- preserve deterministic base package validation.

## Known Gaps For P17

- No signed installer/updater exists.
- No tester device matrix has exercised locked Credential Locker or enterprise
  keyring policy behavior.
- No real-provider network smoke was run in P16.
- Artifact transfer, retention, and support escalation policy still need a real
  pilot loop.
- The package candidate remains explicit and unsigned.

## Explicit Non-Scope To Preserve

- Raw API-key persistence in app config, history, docs, tests, logs,
  screenshots, package resources, or git.
- Keyring exports or screenshots of credential fields.
- Network-required automated tests.
- Committed package outputs, screenshots, local app data, `.env`, keyring
  exports, logs, OCR caches, smoke data, tester personal data, or provider
  secrets.
