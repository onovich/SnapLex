# P13 Private Trial Feedback Response And Credential Package Feasibility Goal Mode Guide

Date: 2026-07-16
Status: execution guide for P13 after planner-accepted P12
Estimated budget: 12 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P13 in goal mode:

```text
Execute SnapLex P13 - Private Trial Feedback Response And Credential Package
Feasibility in 12 conversation rounds.

Required reading before changes:
- AGENTS.md
- Role.md
- README.md
- TRY.md
- .env.example
- pyproject.toml
- docs/development_plan.md
- docs/phase_plan.md
- docs/p12_private_trial_pilot_feedback_triage_goal_guide.md
- docs/p12_final_validation_report.md
- docs/p12_to_p13_handoff.md
- docs/p12_private_trial_release_notes.md
- docs/p12_feedback_intake_template.md
- docs/p12_trial_pass_fail_criteria.md
- docs/p12_manual_environment_checks.md
- docs/p12_real_provider_smoke_decision.md
- docs/p12_credential_package_variant_decision.md
- docs/p12_trial_triage_workflow.md
- docs/p12_boundary_scan_evidence.md
- docs/p13_todo.md
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

P12 is planner-accepted. SnapLex has privacy-safe pilot materials and triage
rules. P13 should run the first feedback response loop, close any S0/S1 pilot
blockers that can be reproduced safely, capture remaining manual environment
results or blockers, and decide whether a credential-capable package variant is
feasible after manual keyring validation.

Goal:
Respond to the first private-trial feedback loop while preserving all existing
release, credential, provider, and no-secret boundaries. Produce a feedback
response log, S0/S1 blocker closure evidence, manual AT/DPI/multi-monitor
results or blockers, optional real-provider smoke evidence only when explicitly
approved, manual keyring/source credential evidence when available, and a
credential-capable package feasibility decision. Prepare a P13 final report and
P13-to-P14 handoff.

Round budget:
- Rounds 1-8: main feedback response and feasibility work.
- Rounds 9-11: buffer fixes for accepted S0/S1 blockers, docs, smoke, package,
  keyring, or boundary issues.
- Round 12: final validation, report, and P14 handoff.

Rules:
- P13 is private-trial response and feasibility assessment, not broad feature
  expansion.
- If no external tester feedback is available, do not fabricate reports. Use
  P12 known gaps as internally tracked pilot blockers and record that no
  external tester report was supplied.
- S0/S1 fixes are allowed only when they are directly tied to accepted pilot
  blockers and can be validated deterministically.
- Do not implement production SnapLex Cloud, account OAuth, billing, hosted
  token broker, browser extension runtime, AI summary runtime, global hotkeys,
  provider rewrites, OCR/capture rewrites, or full localization.
- Do not require real provider credentials, real network calls, real OS keyring
  state, screen permissions, model downloads, or tester devices in automated
  validation.
- Optional real-provider smoke may run only when local credentials already
  exist and a human intentionally approves using the network in that round. If
  not, document it as intentionally skipped.
- Manual keyring smoke must use only a throwaway fake value and must not export
  or commit keyring data.
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

P12 accepted baseline:

- P12 final commit: `1b5c690b4c974c254b9d45d63a78ec4b11a4d583`.
- P12 validation passed with 255 tests and deterministic no-network smoke.
- P12 produced private-trial release notes, feedback intake, pass/fail gates,
  manual environment check runbooks, real-provider smoke policy, credential
  package variant decision notes, triage workflow, and boundary evidence.
- Real provider network smoke was intentionally skipped.
- Optional `keyring` was missing in the executor environment, so Windows
  Credential Locker smoke remains blocked.
- Assistive technology, DPI scaling, and multi-monitor checks remain manual
  tester/device checks.

P13 planning decision:

- The next safest step is to respond to the first pilot feedback loop instead
  of adding unrelated product features.
- The credential-capable package variant remains a feasibility question until
  source keyring behavior and package implications are validated with throwaway
  credentials.
- Feedback may arrive as real tester notes or as documented P12 pilot blockers.
  The executor must label the evidence source honestly.

## 2. Scope

P13 must complete:

- Revalidate the accepted P12 baseline.
- Create a private-trial feedback response log using the P12 template and
  triage taxonomy.
- Triage supplied tester feedback, or explicitly record that no external
  feedback was supplied and use P12 known gaps as internal pilot blockers.
- Close any accepted S0/S1 pilot blockers that can be safely reproduced and
  fixed inside existing boundaries.
- Capture assistive-technology, DPI, and multi-monitor manual results or
  blockers.
- Record optional real-provider smoke run/skip evidence using the P12 policy.
- Attempt manual source keyring smoke only if optional credential dependencies
  are available and only with a throwaway fake value; otherwise record the
  blocker.
- Decide whether a credential-capable package variant should be implemented,
  deferred, rejected, or prototyped in a later explicit phase.
- Preserve deterministic validation, package dry-run, fake smoke, fail-closed
  real trial paths, and no-secret boundaries.
- Create preferred P13 docs:
  - `docs/p13_feedback_response_log.md`
  - `docs/p13_s0_s1_blocker_resolution.md`
  - `docs/p13_manual_environment_results.md`
  - `docs/p13_real_provider_smoke_record.md`
  - `docs/p13_keyring_source_smoke_record.md`
  - `docs/p13_credential_package_feasibility.md`
  - `docs/p13_boundary_scan_evidence.md`
  - `docs/p13_final_validation_report.md`
  - `docs/p13_to_p14_handoff.md`
- Update README, phase plan, development plan, smoke checklist, TODO, and
  planning entry points.

## 3. Non-Scope

Do not implement in P13:

- Production SnapLex Cloud.
- Production account OAuth, billing, hosted token broker, remote accounts, or
  cloud sync.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to accepted S0/S1 pilot blockers.
- OCR/capture rewrites unrelated to accepted S0/S1 pilot blockers.
- Full localization implementation.
- A credential-capable package variant unless the architect explicitly expands
  scope after the P13 feasibility decision.
- Automated tests that require real provider credentials, network calls, real
  OS keyring state, screen permissions, model downloads, or tester devices.
- Collection or storage of real tester personal data inside the repo.
- Committed screenshots, package outputs, local app data, `.env`, provider
  secrets, keyring exports, logs, OCR model caches, or smoke data.

## 4. Planner Decisions And Assumptions

- P13 uses a 12-round budget because it may include small accepted blocker
  fixes, but should not become a broad feature phase.
- Feedback intake remains local Markdown unless the user explicitly chooses an
  external issue tracker.
- If no tester reports are available, the executor should not block the phase;
  it should record "no external feedback supplied" and process P12 known gaps as
  internal pilot blockers.
- Credential-capable packaging must remain a decision artifact unless manual
  keyring validation and package constraints justify a later implementation
  phase.
- Real-provider smoke remains opt-in only and must never run as an automated
  default.

## 5. Architecture Boundaries

Hard constraints:

- P10/P11/P12 credential boundaries remain intact.
- Provider setup and Test Connection remain behind services/presenters.
- Translation execution remains behind `TranslationPipeline`.
- Trial scripts keep fake and real paths separate.
- Feedback response docs must not create new runtime truth that contradicts
  service/provider/config boundaries.
- Any user-facing copy must state current product reality: account OAuth,
  cloud accounts, hosted token broker, and packaged keyring support are not
  shipped.
- S0/S1 fixes must be narrow, test-backed, and tied to accepted pilot evidence.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P13 Private Trial Feedback Response And Credential Package Feasibility
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

- Can the current change be explained by feedback response, S0/S1 blocker
  closure, manual environment evidence, real-provider smoke record, source
  keyring smoke, credential package feasibility, or boundary scan?
- Can failures be localized to docs, package smoke, GUI smoke, trial readiness,
  credential readiness, keyring availability, provider setup, or a specific
  accepted pilot blocker?
- Are fake smoke, real-trial fail-closed, skipped real-provider smoke,
  unavailable keyring, tester privacy, and no-secret states covered?
- If tester-facing material changed, does it tell testers not to paste secrets
  or personal data?
- If generated outputs were created, are they ignored and uncommitted?

Architecture self-check:

- Did P13 avoid adding runtime features outside accepted pilot blockers?
- Did credential/provider/trial boundaries stay in their existing services?
- Did docs avoid promising account OAuth, cloud accounts, packaged keyring, or
  real network support beyond validated scope?
- Are feedback artifacts privacy-preserving and repo-safe?
- Are unrelated files, generated outputs, and user changes left alone?

## 7. Round Plan

Round 1 - Rebaseline and feedback source inventory:

- Revalidate P12 with the core validation matrix.
- Create `docs/p13_feedback_response_log.md`.
- Record whether external tester feedback exists. If not, explicitly state that
  the phase is processing P12 known gaps as internal pilot blockers.

Round 2 - Triage and S0/S1 decision:

- Classify feedback or known gaps using P12 severity and disposition rules.
- Create `docs/p13_s0_s1_blocker_resolution.md` with accepted, rejected,
  deferred, and investigated items.
- Decide which S0/S1 items are safe to fix in P13.

Round 3 - First accepted blocker fix or closure:

- Implement the smallest accepted S0/S1 fix if one exists.
- If no accepted fix exists, close the round with evidence that P13 remains
  documentation/validation-only.
- Add focused deterministic tests when code changes.

Round 4 - Manual AT/DPI/multi-monitor evidence:

- Create `docs/p13_manual_environment_results.md`.
- Run or document blockers for assistive technology, DPI scaling, and
  multi-monitor behavior.
- Keep screenshots local and ignored if any are created.

Round 5 - Optional real-provider smoke record:

- Create `docs/p13_real_provider_smoke_record.md`.
- Run one narrow real-provider smoke only if credentials exist and human network
  approval is explicit.
- Otherwise document a skipped result and the exact blocker.

Round 6 - Source keyring smoke record:

- Create `docs/p13_keyring_source_smoke_record.md`.
- If optional `keyring` support is available, run source checkout credential
  save/read/delete smoke with a throwaway fake value.
- If unavailable, record the blocker and do not fake a pass.

Round 7 - Credential package feasibility:

- Create `docs/p13_credential_package_feasibility.md`.
- Decide whether a credential-capable package variant should be implemented,
  deferred, rejected, or prototyped in a later explicit phase.
- Do not build or promise the variant unless the architect expands scope.

Round 8 - Feedback response closure:

- Update release/trial docs based on accepted feedback without broadening scope.
- Confirm all accepted S0/S1 items have closure evidence or a documented
  blocker.
- Update docs indexes.

Rounds 9-11 - Buffer hardening:

- Fix docs, accepted S0/S1 regressions, smoke, package, keyring, or boundary
  issues found during P13.
- Repeat relevant validation after each fix.
- Keep scope narrow.

Round 12 - Final validation, report, and P14 handoff:

- Create `docs/p13_boundary_scan_evidence.md`.
- Create `docs/p13_final_validation_report.md`.
- Create `docs/p13_to_p14_handoff.md`.
- Mark `docs/p13_todo.md` complete.
- Update README, phase plan, development plan, smoke checklist, and AGENTS entry
  points to reflect P13 completion.
- Run final validation, boundary scans, commit, push, and report back to the
  planner/checker session for P13 acceptance.
- Recommend P14 based on actual feedback, not preference.

## 8. Validation Matrix

Required P13 validation:

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
- Docs link/index check for P13 docs.
- Artifact and secret boundary scan showing no committed `build/`, `dist/`,
  packaged binaries, generated config/history, `.env`, provider keys,
  screenshots, smoke data, local app data, logs, keyring exports, OCR caches,
  tester personal data, or API response captures.

Optional manual validation:

- Assistive technology checks.
- DPI and multi-monitor checks.
- Real-provider smoke only with existing local credentials and explicit human
  approval.
- Source keyring smoke only with installed optional credentials support and a
  throwaway fake value.
- Packaged credential behavior only as feasibility evidence, not a shipped
  promise.

No P13 validation may require:

- Real provider credentials by default.
- Network calls in automated tests.
- Real OS keyring state.
- Production SnapLex Cloud or account OAuth.
- Committed screenshots, local secret stores, package outputs, or tester
  personal data.

## 9. PASS Criteria

P13 passes when:

- Feedback response log exists and clearly labels whether external tester
  feedback was supplied.
- S0/S1 pilot blockers are fixed, closed with evidence, or explicitly blocked.
- Assistive-technology, DPI, and multi-monitor results or blockers are recorded.
- Optional real-provider smoke has a clear run/skip record.
- Source keyring smoke has a clear pass/blocker record.
- Credential-capable package feasibility has a clear implement/defer/reject or
  prototype-next decision.
- P12/P11/P10 credential, package, trial, and no-secret boundaries remain
  intact.
- Required validation and boundary scans pass.
- P13 final validation report and P13 to P14 handoff exist.
- Final P13 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P13 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Feedback response log:
- S0/S1 blocker resolution:
- Manual environment results:
- Optional real-provider smoke:
- Source keyring smoke:
- Credential package feasibility:
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
P13 to P14 handoff:
- Accepted P13 baseline:
- Feedback response summary:
- S0/S1 closure evidence:
- Manual validation results/blockers:
- Real-provider and keyring smoke status:
- Credential package feasibility decision:
- Known trial gaps:
- Recommended P14 scope:
- Validation to preserve:
- Explicit non-scope:
```
