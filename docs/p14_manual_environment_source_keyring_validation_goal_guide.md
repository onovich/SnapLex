# P14 Manual Environment And Source Keyring Validation Goal Mode Guide

Date: 2026-07-16
Status: execution guide for P14 after planner-accepted P13
Estimated budget: 12 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P14 in goal mode:

```text
Execute SnapLex P14 - Manual Environment And Source Keyring Validation in 12
conversation rounds.

Required reading before changes:
- AGENTS.md
- Role.md
- README.md
- TRY.md
- .env.example
- pyproject.toml
- docs/development_plan.md
- docs/phase_plan.md
- docs/p13_private_trial_feedback_response_credential_package_feasibility_goal_guide.md
- docs/p13_final_validation_report.md
- docs/p13_to_p14_handoff.md
- docs/p13_feedback_response_log.md
- docs/p13_s0_s1_blocker_resolution.md
- docs/p13_manual_environment_results.md
- docs/p13_real_provider_smoke_record.md
- docs/p13_keyring_source_smoke_record.md
- docs/p13_credential_package_feasibility.md
- docs/p13_boundary_scan_evidence.md
- docs/p14_todo.md
- docs/windows_smoke_checklist.md
- packaging/README.md
- RequireRealProvider.cmd
- StartTrial.cmd
- StartFakeTrial.cmd
- StartPackagedTrial.cmd
- StartPackagedFakeTrial.cmd
- SmokeTrial.cmd
- scripts/p9_gui_smoke.py
- scripts/p11_visible_gui_smoke.py
- snaplex/app.py
- snaplex/trial_readiness.py
- snaplex/credentials.py
- tests/test_trial_readiness.py
- tests/test_release_smoke.py
- tests/test_credentials.py

P13 is planner-accepted. P13 did not fabricate external tester feedback, found
no accepted S0/S1 runtime repair, and left the next evidence gaps as manual
AT/DPI/multi-monitor validation, optional source keyring smoke, optional
real-provider smoke, and a later decision about whether to authorize an
isolated credential-capable package spike.

Goal:
Collect privacy-safe tester feedback if available, run manual
assistive-technology, DPI scaling, and multi-monitor checks on target Windows
devices when available, install optional source credential support and run
save/read/delete keyring smoke with a throwaway fake value when feasible, keep
real-provider network smoke optional and human-approved only, and decide
whether the evidence justifies a later isolated credential-capable package
spike. Preserve all P10-P13 credential, provider, privacy, packaging, and
no-secret boundaries.

Round budget:
- Rounds 1-8: main manual validation and evidence work.
- Rounds 9-11: buffer fixes for accepted validation blockers, docs, smoke,
  keyring, or hygiene gaps.
- Round 12: final validation, report, and P15 handoff.

Rules:
- P14 is manual validation and feasibility evidence, not broad feature
  expansion.
- Do not fabricate external tester feedback. If no tester feedback is supplied,
  record that explicitly.
- Manual AT/DPI/multi-monitor checks may pass, fail, or be blocked by missing
  devices. Record the evidence honestly.
- Source keyring smoke must use only a throwaway fake value and must not export
  or commit keyring data.
- Installing optional credential support is allowed only as an explicit local
  environment step; if dependency install or keyring backend availability is
  blocked, document the blocker instead of faking a pass.
- Optional real-provider smoke may run only when local credentials already
  exist and a human intentionally approves network use in that round. If not,
  document it as skipped.
- Do not implement a credential-capable package variant in P14. Decide whether
  a later isolated spike is justified.
- Do not implement production SnapLex Cloud, account OAuth, billing, hosted
  token broker, browser extension runtime, AI summary runtime, global hotkeys,
  provider rewrites, OCR/capture rewrites, or full localization.
- Do not require real provider credentials, real network calls, real OS keyring
  state, screen permissions, model downloads, or tester devices in automated
  validation.
- Do not collect or commit real tester personal data, provider secrets, `.env`
  files, screenshots with sensitive content, package outputs, logs, keyring
  exports, OCR caches, or smoke app data.
- Keep base fake smoke deterministic and no-network.
- Every round must include Debug self-check, architecture self-check,
  validation commands and results, commit hash, push result, next-round target,
  and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to
  the next round.
```

## 1. Required Context

P13 accepted baseline:

- P13 final commit: `9ec029c9d72354fac768a558ddb70881622475ca`.
- P13 validation passed with 255 tests and deterministic no-network smoke.
- P13 recorded no external tester feedback supplied, no accepted S0/S1 runtime
  repair, manual AT/DPI/multi-monitor blockers, real-provider smoke skip,
  source keyring blocker, and credential-package defer decision.
- Credential-capable package behavior is not implemented, shipped, or promised.
- Real-provider network smoke remains optional and human-approved only.

P14 planning decision:

- The next safest step is to collect actual manual environment evidence and
  source keyring evidence before authorizing any package-variant spike.
- P14 should produce evidence and decisions, not a credential-capable package.
- If devices, credentials, keyring support, or tester feedback are unavailable,
  P14 should record precise blockers and preserve deterministic validation.

## 2. Scope

P14 must complete:

- Revalidate the accepted P13 baseline.
- Ingest privacy-safe tester feedback if supplied; otherwise record that no
  external tester feedback was supplied.
- Run or document blockers for assistive-technology validation.
- Run or document blockers for DPI scaling validation.
- Run or document blockers for multi-monitor validation.
- Install optional source credential support and run source keyring
  save/read/delete smoke with a throwaway fake value when feasible; otherwise
  record dependency/backend blockers.
- Record optional real-provider smoke run/skip evidence using the P12/P13
  policy.
- Decide whether evidence justifies a later isolated credential-capable package
  spike, or whether to defer/reject that spike.
- Preserve deterministic validation, package dry-run, fake smoke, fail-closed
  real trial paths, and no-secret boundaries.
- Create preferred P14 docs:
  - `docs/p14_tester_feedback_intake_log.md`
  - `docs/p14_manual_at_dpi_multimonitor_results.md`
  - `docs/p14_source_keyring_smoke_evidence.md`
  - `docs/p14_real_provider_smoke_record.md`
  - `docs/p14_credential_package_spike_decision.md`
  - `docs/p14_boundary_scan_evidence.md`
  - `docs/p14_final_validation_report.md`
  - `docs/p14_to_p15_handoff.md`
- Update README, phase plan, development plan, smoke checklist, TODO, and
  planning entry points.

## 3. Non-Scope

Do not implement in P14:

- Credential-capable package variant.
- Production SnapLex Cloud.
- Production account OAuth, billing, hosted token broker, remote accounts, or
  cloud sync.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to accepted validation blockers.
- OCR/capture rewrites unrelated to accepted validation blockers.
- Full localization implementation.
- Automated tests that require real provider credentials, network calls, real
  OS keyring state, screen permissions, model downloads, or tester devices.
- Collection or storage of real tester personal data inside the repo.
- Committed screenshots, package outputs, local app data, `.env`, provider
  secrets, keyring exports, logs, OCR model caches, or smoke data.

## 4. Planner Decisions And Assumptions

- P14 uses a 12-round budget because it is manual validation and feasibility
  evidence, with room for narrow docs or validation fixes.
- P14 should not block forever when a manual device or optional dependency is
  unavailable. It should record blockers and decide whether that evidence is
  enough for P15.
- Keyring smoke is source-checkout validation only. Packaged keyring behavior
  remains a later explicit spike decision.
- Real-provider smoke remains opt-in only and must never run as an automated
  default.

## 5. Architecture Boundaries

Hard constraints:

- P10-P13 credential boundaries remain intact.
- Provider setup and Test Connection remain behind services/presenters.
- Translation execution remains behind `TranslationPipeline`.
- Trial scripts keep fake and real paths separate.
- Manual validation docs must not promise package behavior that has not been
  validated.
- Any user-facing copy must state current product reality: account OAuth,
  cloud accounts, hosted token broker, and packaged keyring support are not
  shipped.
- Any accepted blocker fix must be narrow, test-backed, and tied to validation
  evidence.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P14 Manual Environment And Source Keyring Validation
Round goal:
Completed changes:
Debug self-check:
Architecture self-check:
Validation commands and results:
Commit hash:
Push result:
Buffer consumed:
Risks or blockers:
Next-round target:
```

Progression rules:

- Validation fails: do not commit, do not push, do not move to the next round.
- Validation passes but commit fails: do not move to the next round.
- Commit succeeds but push fails: do not move to the next round.
- Push succeeds: record commit hash and remote branch, then move to the next
  round.
- Any scope expansion beyond this guide must be explicitly approved by the
  architect/PM before implementation.

Debug self-check:

- Can the current change be explained by tester feedback intake, AT/DPI/
  multi-monitor validation, source keyring smoke, real-provider smoke record,
  package-spike decision, or boundary scan?
- Can failures be localized to docs, device availability, keyring dependency,
  keyring backend, provider readiness, trial scripts, package dry-run, GUI
  smoke, or boundary scan?
- Are pass, fail, skipped, blocked, unavailable, no-feedback, and no-secret
  states covered?
- If tester-facing material changed, does it tell testers not to paste secrets
  or personal data?
- If generated outputs were created, are they ignored and uncommitted?

Architecture self-check:

- Did P14 avoid implementing the credential-capable package?
- Did credential/provider/trial boundaries stay in their existing services?
- Did docs avoid promising account OAuth, cloud accounts, packaged keyring, or
  real network support beyond validated scope?
- Are manual validation artifacts privacy-preserving and repo-safe?
- Are unrelated files, generated outputs, and user changes left alone?

## 7. Round Plan

Round 1 - Rebaseline and tester feedback inventory:

- Revalidate P13 with the core validation matrix.
- Create `docs/p14_tester_feedback_intake_log.md`.
- Record whether external tester feedback exists. If none, state that clearly.

Round 2 - Assistive-technology validation:

- Start `docs/p14_manual_at_dpi_multimonitor_results.md`.
- Run or document blocker for screen-reader or assistive-technology checks on
  a target Windows device.
- Record environment, result, and privacy-safe evidence.

Round 3 - DPI scaling validation:

- Run or document blocker for target DPI scaling values.
- Record visible GUI, Settings, History, result states, and long-text behavior.
- Keep screenshots local and ignored if any are created.

Round 4 - Multi-monitor validation:

- Run or document blocker for multi-monitor behavior.
- Include screen translation overlay/capture coordinate notes when feasible.
- Record whether any accepted blocker needs later implementation.

Round 5 - Optional credential dependency setup:

- Attempt local source environment credential extra setup only when appropriate.
- Record installed/missing optional `keyring` status without committing
  environment artifacts.

Round 6 - Source keyring smoke:

- Create `docs/p14_source_keyring_smoke_evidence.md`.
- If keyring is available, run save/read/readiness/delete smoke with a
  throwaway fake value.
- If unavailable, record exact dependency/backend blocker.

Round 7 - Optional real-provider smoke record:

- Create `docs/p14_real_provider_smoke_record.md`.
- Run one narrow real-provider smoke only if credentials exist and human
  network approval is explicit.
- Otherwise document skipped result and blocker.

Round 8 - Credential package spike decision:

- Create `docs/p14_credential_package_spike_decision.md`.
- Decide whether to authorize, defer, or reject a later isolated
  credential-capable package spike.
- Do not implement the spike in P14.

Rounds 9-11 - Buffer hardening:

- Fix docs, accepted validation blockers, smoke, keyring, package dry-run, or
  boundary issues found during P14.
- Repeat relevant validation after each fix.
- Keep scope narrow.

Round 12 - Final validation, report, and P15 handoff:

- Create `docs/p14_boundary_scan_evidence.md`.
- Create `docs/p14_final_validation_report.md`.
- Create `docs/p14_to_p15_handoff.md`.
- Mark `docs/p14_todo.md` complete.
- Update README, phase plan, development plan, smoke checklist, and AGENTS entry
  points to reflect P14 completion.
- Run final validation, boundary scans, commit, push, and report back to the
  planner/checker session for P14 acceptance.
- Recommend P15 based on actual validation evidence.

## 8. Validation Matrix

Required P14 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python -m snaplex --check-real-provider` expected rejection without real
  provider setup.
- `python scripts\package_windows.py --dry-run --variant base`
- `cmd /c StartTrial.cmd --no-gui` expected rejection without real provider
  setup.
- `cmd /c StartFakeTrial.cmd --no-gui`
- `cmd /c SmokeTrial.cmd`
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`
- `cmd /c StartPackagedTrial.cmd --no-gui` expected rejection without real
  provider setup.
- `python scripts\p9_gui_smoke.py`
- `python scripts\p11_visible_gui_smoke.py`
- Docs link/index check for P14 docs.
- Artifact and secret boundary scan showing no committed `build/`, `dist/`,
  packaged binaries, generated config/history, `.env`, provider keys,
  screenshots, smoke data, local app data, logs, keyring exports, OCR caches,
  tester personal data, or API response captures.

Optional manual validation:

- Assistive technology checks.
- DPI scaling checks.
- Multi-monitor checks.
- Real-provider smoke only with existing local credentials and explicit human
  approval.
- Source keyring smoke only with installed optional credentials support and a
  throwaway fake value.

No P14 validation may require:

- Real provider credentials by default.
- Network calls in automated tests.
- Real OS keyring state in automated tests.
- Production SnapLex Cloud or account OAuth.
- Committed screenshots, local secret stores, package outputs, or tester
  personal data.

## 9. PASS Criteria

P14 passes when:

- Tester feedback intake log exists and clearly labels whether external tester
  feedback was supplied.
- Assistive-technology, DPI, and multi-monitor results or blockers are recorded.
- Source keyring smoke has a clear pass/blocker record using only a throwaway
  fake value.
- Optional real-provider smoke has a clear run/skip record.
- Credential-capable package spike decision is explicit and does not ship a
  package variant.
- P13/P12/P11/P10 credential, package, trial, and no-secret boundaries remain
  intact.
- Required validation and boundary scans pass.
- P14 final validation report and P14 to P15 handoff exist.
- Final P14 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P14 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Tester feedback intake:
- Manual AT/DPI/multi-monitor results:
- Source keyring smoke:
- Optional real-provider smoke:
- Credential package spike decision:
- Credential/privacy handling:
- Deferred scope:
- Architecture notes:
- Artifact and secret exclusion evidence:
- Commit hashes:
- Push result:
- Request for architect/PM acceptance:
- Recommended next goal:
```

```text
P14 to P15 handoff:
- Accepted P14 baseline:
- Tester feedback summary:
- Manual AT/DPI/multi-monitor results/blockers:
- Source keyring smoke status:
- Real-provider smoke status:
- Credential package spike decision:
- Known trial gaps:
- Recommended P15 scope:
- Validation to preserve:
- Explicit non-scope:
```
