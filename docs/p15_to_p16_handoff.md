# P15 To P16 Handoff

Date: 2026-07-16
Status: P15 executor-complete; ready for planner acceptance

Recommended P16: Credential-Capable Package Production Hardening.

## P15 Baseline

P15 completed an isolated credential-capable package spike while preserving the
deterministic base package path. It added an explicit `credentials` package
variant and an explicit `--smoke-credentials` CLI, proved packaged keyring
import/backend discovery, proved packaged save/read/delete/cleanup, proved
packaged restart readiness, documented cleanup, and made a promote/defer/reject
decision.

Final P15 executor artifacts:

- `docs/p15_packaging_spike_design.md`
- `docs/p15_packaged_keyring_import_evidence.md`
- `docs/p15_packaged_credential_smoke_evidence.md`
- `docs/p15_packaged_restart_readiness.md`
- `docs/p15_credential_cleanup_guidance.md`
- `docs/p15_package_spike_decision.md`
- `docs/p15_boundary_scan_evidence.md`
- `docs/p15_final_validation_report.md`

## Validation To Preserve

- `Validate.cmd` PASS with 261 tests.
- `git diff --check` PASS.
- `python -m snaplex --version` PASS.
- `python -m snaplex --no-gui` PASS.
- `python -m snaplex --check-real-provider` expected rejection PASS.
- `python scripts\package_windows.py --dry-run --variant base` PASS.
- `python scripts\package_windows.py --dry-run --variant credentials` PASS.
- `StartTrial.cmd --no-gui` expected rejection PASS.
- `StartFakeTrial.cmd --no-gui` PASS.
- `SmokeTrial.cmd` PASS.
- `StartPackagedFakeTrial.cmd --no-gui` PASS.
- `StartPackagedTrial.cmd --no-gui` expected rejection PASS.
- `python scripts\p9_gui_smoke.py` PASS.
- `python scripts\p11_visible_gui_smoke.py` PASS.
- P15 docs index, artifact scan, and secret scan PASS.

## Evidence Summary

- Explicit package variant: `credentials`.
- Base package: deterministic and still excludes keyring.
- Credentials variant import/backend: PASS,
  `keyring.backends.Windows.WinVaultKeyring`.
- Packaged save/read/delete/cleanup: PASS with runtime-generated throwaway
  value.
- Packaged restart readiness: PASS across two packaged processes.
- Cleanup guidance: recorded in `docs/p15_credential_cleanup_guidance.md`.
- Decision: promote to later production hardening phase, not production release
  promise.

## Suggested P16 Scope

P16 should harden the credential-capable package path for production decision:

- keep the base package deterministic and unchanged;
- harden the explicit `credentials` variant build and smoke path;
- define tester-facing credential package setup, failure, and cleanup docs;
- polish failure messages for missing, unavailable, or locked keyring backends;
- decide whether the credential-capable package remains a separate variant or
  becomes a clearly labeled trial artifact;
- define release gates for signed builds, packaging outputs, and manual smoke;
- preserve no-network automated validation and no-secret repository hygiene;
- run optional real-provider smoke only with existing local credentials and
  explicit human network approval.

## Known Gaps For P16

- P15 did not ship or promise a production credential-capable package.
- P15 did not test locked Windows Credential Locker, enterprise keyring policy,
  signed installer behavior, or updater behavior.
- P15 did not run real-provider network smoke.
- P15 cleanup guidance is maintainer-oriented and should be polished before
  broad tester distribution.

## Explicit Non-Scope To Preserve

- SnapLex Cloud, account OAuth, billing, hosted token broker, remote accounts,
  or cloud sync.
- Raw API-key persistence in app config.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Broad provider rewrites.
- OCR/capture rewrites.
- Full localization implementation.
- Network-required automated tests.
- Committed screenshots, package outputs, local app data, `.env`, keyring
  exports, logs, OCR caches, smoke data, tester personal data, or provider
  secrets.
