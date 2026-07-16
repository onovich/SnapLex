# P14 To P15 Handoff

Date: 2026-07-16
Status: P14 planner-accepted; P15 ready for execution

Selected P15: isolated credential-capable package spike design gate.

P15 execution guide:
`docs/p15_isolated_credential_package_spike_design_gate_goal_guide.md`
P15 TODO: `docs/p15_todo.md`

## P14 Baseline

P14 completed manual environment and source keyring validation while preserving
the accepted P10/P11/P12/P13 boundaries. No external tester report was supplied,
so the executor recorded no external feedback rather than fabricating pilot
results.

Final P14 executor artifacts:

- `docs/p14_tester_feedback_intake_log.md`
- `docs/p14_manual_at_dpi_multimonitor_results.md`
- `docs/p14_source_keyring_smoke_evidence.md`
- `docs/p14_real_provider_smoke_record.md`
- `docs/p14_credential_package_spike_decision.md`
- `docs/p14_boundary_scan_evidence.md`
- `docs/p14_final_validation_report.md`

## Validation To Preserve

- `Validate.cmd` PASS with 255 tests.
- `git diff --check` PASS.
- `python -m snaplex --version` PASS.
- `python -m snaplex --no-gui` PASS.
- `python -m snaplex --check-real-provider` expected rejection PASS.
- `python scripts\package_windows.py --dry-run --variant base` PASS.
- `StartTrial.cmd --no-gui` expected rejection PASS.
- `StartFakeTrial.cmd --no-gui` PASS.
- `SmokeTrial.cmd` PASS.
- `StartPackagedFakeTrial.cmd --no-gui` PASS.
- `StartPackagedTrial.cmd --no-gui` expected rejection PASS.
- `python scripts\p9_gui_smoke.py` PASS.
- `python scripts\p11_visible_gui_smoke.py` PASS.
- P14 docs index, artifact scan, and secret scan PASS.

## Evidence Summary

- External tester feedback: none supplied.
- Assistive technology: manual check BLOCKED / NOT RUN.
- DPI scaling: manual check BLOCKED / NOT RUN.
- Multi-monitor: manual check BLOCKED / NOT RUN.
- Source credential dependency: optional `keyring` support installed locally.
- Source keyring backend: `keyring.backends.Windows.WinVaultKeyring`.
- Source keyring smoke: save/read/delete/cleanup PASS with a throwaway fake
  value through SnapLex credential service boundaries.
- Real provider network smoke: skipped without local credentials and explicit
  human network approval.
- Real trial paths: fail closed when no real provider is configured.
- Credential package decision: later isolated spike is justified, but no
  package credential implementation was added or promised in P14.

## Known Trial Gaps

- No external tester feedback has been ingested.
- Assistive technology has not been tested by a human screen-reader session.
- DPI scaling has not been manually tested at target scaling values.
- Multi-monitor behavior has not been manually tested on multiple displays.
- Real-provider network smoke remains opt-in and skipped in this environment.
- Packaged keyring behavior is not implemented, shipped, or promised.

## Selected P15 Scope

P15 should be a narrow, architect-approved spike if accepted:

- keep the existing base package and fake package smoke unchanged;
- prototype credential-capable packaging only as an isolated variant or spike
  entry point;
- prove packaged keyring backend inclusion and import discovery;
- prove packaged save/read/delete with a throwaway fake value;
- prove packaged restart readiness without displaying or printing the fake
  value;
- preserve fail-closed real trial behavior when no real provider is configured;
- add cleanup guidance for local throwaway/manual credentials;
- keep automated validation deterministic and no-network.

P15 should not become production SnapLex Cloud, account OAuth, billing, hosted
token broker, broad provider rewrites, OCR/capture rewrites, browser extension
runtime, AI summary runtime, global hotkeys, full localization, or a packaged
credential release promise without explicit later approval.

## Manual Environment Follow-Up

AT/DPI/multi-monitor checks remain useful, but they need a target Windows
device or human review session. If P15 gets real device access, record those
results in a privacy-safe report without screenshots containing sensitive
content, provider keys, private documents, tester personal data, logs, or
keyring exports.

## Explicit Non-Scope To Preserve

- SnapLex Cloud, account OAuth, billing, hosted token broker, remote accounts,
  or cloud sync.
- Raw API-key persistence in app config.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to accepted pilot blockers.
- OCR/capture rewrites unrelated to accepted pilot blockers.
- Full localization implementation.
- Network-required automated tests.
- Committed screenshots, package outputs, local app data, `.env`, keyring
  exports, logs, OCR caches, smoke data, tester personal data, or provider
  secrets.
