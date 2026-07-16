# P14 Final Validation Report

Date: 2026-07-16
Phase: P14 Manual Environment And Source Keyring Validation
Status: PASS - planner-accepted

P14 completed manual-environment and source-keyring validation without
expanding SnapLex runtime scope. No external tester feedback was supplied to
the executor, so P14 recorded that honestly and did not fabricate pilot
reports. Assistive-technology, DPI scaling, and multi-monitor checks remain
target-device manual blockers. Source keyring save/read/delete passed with a
throwaway fake value through SnapLex credential service boundaries. Optional
real-provider network smoke was skipped without credentials and explicit human
network approval, while real trial paths continued to fail closed. P14
recommends a later isolated credential-capable package spike, but did not
implement, ship, or promise one.

## Rounds Used

- Round 1: rebaseline and tester feedback intake.
- Round 2: assistive-technology validation blocker record.
- Round 3: DPI scaling validation blocker record.
- Round 4: multi-monitor validation blocker record.
- Round 5: optional source credential dependency and backend status.
- Round 6: source keyring save/read/delete smoke.
- Round 7: optional real-provider smoke skip and fail-closed record.
- Round 8: credential package spike decision.
- Round 9: boundary scan evidence.
- Round 10: final validation matrix.
- Round 11: final report, docs index updates, and P15 handoff.
- Round 12: final commit, push, and planner notification.

Buffer consumed: 0 repair buffer rounds. No accepted S0/S1 runtime repair was
identified.

## Main Deliverables

- `docs/p14_tester_feedback_intake_log.md`
- `docs/p14_manual_at_dpi_multimonitor_results.md`
- `docs/p14_source_keyring_smoke_evidence.md`
- `docs/p14_real_provider_smoke_record.md`
- `docs/p14_credential_package_spike_decision.md`
- `docs/p14_boundary_scan_evidence.md`
- `docs/p14_final_validation_report.md`
- `docs/p14_to_p15_handoff.md`

## Feedback And Manual Environment

- External tester feedback: none supplied.
- Assistive technology: BLOCKED / NOT RUN because no human screen-reader
  session or target AT tool was supplied.
- DPI scaling: BLOCKED / NOT RUN because no target display scaling change or
  manual review evidence was supplied.
- Multi-monitor: BLOCKED / NOT RUN because no multi-monitor hardware,
  configured equivalent, or manual overlay/capture review was supplied.
- P9 and P11 GUI smoke remain supporting regression evidence, not substitutes
  for the target-device manual checks.

## Source Keyring Evidence

P14 installed optional credential support locally with
`python -m pip install -e ".[credentials]"`, confirmed
`keyring.backends.Windows.WinVaultKeyring`, and ran source save/read/delete
smoke through `CredentialService` and `KeyringCredentialStore` using only a
throwaway fake value.

Observed source keyring smoke output:

```text
source_keyring_save_read_delete=PASS
source_keyring_cleanup=PASS
source_keyring_backend=Windows WinVaultKeyring
```

The temporary helper stayed under ignored `tmp\`, the fake value was not
printed in command output or committed docs, and the smoke deleted the
credential before exit.

## Credential Package Decision

P14 recommends a later isolated credential-capable package spike because source
keyring save/read/delete now passes. P14 does not implement or promise package
credential support. The base package remains the deterministic fake/private
trial smoke path.

Required future spike constraints are recorded in
`docs/p14_credential_package_spike_decision.md`.

## Validation Commands And Results

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`:
  PASS with ruff, format check, mypy, compileall, and 255 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS, PySide6 bootstrap OK.
- `python -m snaplex --check-real-provider`: expected rejection PASS,
  `Real translation provider is not configured.`
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: expected rejection PASS.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS with visible fake smoke label.
- `cmd /c SmokeTrial.cmd`: PASS, including packaged workflow smoke from local
  `dist\SnapLex\SnapLex.exe`.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`: PASS with visible fake smoke
  label.
- `cmd /c StartPackagedTrial.cmd --no-gui`: expected rejection PASS.
- `python scripts\p9_gui_smoke.py`: PASS with seven ignored local screenshots.
- `python scripts\p11_visible_gui_smoke.py`: PASS with six ignored local
  screenshots.
- P14 docs link/index check: PASS.
- Artifact scan: PASS; no tracked `build`, `dist`, `snaplex-smoke-data`, `tmp`,
  `.pytest_cache`, `.env`, logs, caches, screenshots, OCR model caches, or
  smoke data.
- Secret pattern scan: PASS; no real provider keys, bearer tokens, `.env`,
  keyring exports, logs, screenshots, package resources, tester data, or API
  response captures found in tracked content.

## Credential And Privacy Handling

- Raw provider key values were not stored in config, history, docs, tests,
  logs, screenshots, package resources, or git.
- Fake mode remains deterministic and visibly labeled as fake smoke mode.
- Real trial paths remain fail-closed when no real provider is configured.
- Optional real-provider network smoke remains skipped without local
  credentials and explicit human network approval.
- Source keyring evidence uses only a throwaway fake value and source checkout
  behavior.
- Packaged keyring behavior is not implemented, tested, or promised.

## Known Limitations

- No external tester feedback was supplied to this executor.
- Assistive-technology, DPI scaling, and multi-monitor checks remain manual
  NOT RUN blockers.
- Optional real-provider network smoke was skipped because no local credentials
  and no explicit human network approval were present.
- P14 installed optional credential support into the local Python environment;
  this is environment state only and not a repository artifact.
- Packaged keyring/credential-capable package behavior is not implemented or
  promised.

## Architecture Notes

P14 did not move provider, credential, settings, history, OCR, capture,
translation, or package rules into UI widgets or scripts. Providers remain
behind provider contracts, provider registry, and `TranslationPipeline`.
Credential behavior remains behind credential services/stores, settings
services/presenters, provider setup, and trial readiness.

## Commit Hashes

- `000d67c` docs: record P14 dispatch
- `018e911` p14: log tester feedback intake
- `85827c9` p14: record assistive tech blocker
- `a1440f7` p14: record dpi scaling blocker
- `7316466` p14: record multi-monitor blocker
- `3de7e54` p14: record keyring dependency status
- `62da2ff` p14: record source keyring smoke
- `0578650` p14: record real provider smoke skip
- `b4f8684` p14: decide credential package spike
- `f861c81` p14: record boundary scan evidence

## Request For Acceptance

P14 is accepted by planner/architect review.

## Planner Acceptance

Planner recheck on 2026-07-16: PASS.

Re-run validation evidence:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`:
  PASS with 255 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, prints `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS, PySide6 bootstrap OK.
- `python -m snaplex --check-real-provider`: expected rejection PASS when no
  real provider is configured.
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: expected rejection PASS.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS.
- `cmd /c SmokeTrial.cmd`: PASS.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`: PASS.
- `cmd /c StartPackagedTrial.cmd --no-gui`: expected rejection PASS.
- `python scripts\p9_gui_smoke.py`: PASS with ignored local screenshots.
- `python scripts\p11_visible_gui_smoke.py`: PASS with ignored local
  screenshots.
- P14 docs link/index check: PASS.
- Artifact boundary scan: PASS.
- Secret pattern scan: PASS.

Selected P15: an isolated credential-capable package spike design gate, limited
to proving packaged keyring behavior with throwaway fake values while
preserving the deterministic base package path and all no-secret/no-network
boundaries.
