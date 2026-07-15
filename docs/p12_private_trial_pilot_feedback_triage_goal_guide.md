# P12 Private Trial Pilot And Feedback Triage Goal Mode Guide

Date: 2026-07-16
Status: execution guide for P12 after planner-accepted P11
Estimated budget: 12 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P12 in goal mode:

```text
Execute SnapLex P12 - Private Trial Pilot And Feedback Triage in 12 conversation
rounds.

Required reading before changes:
- AGENTS.md
- Role.md
- README.md
- TRY.md
- .env.example
- pyproject.toml
- docs/development_plan.md
- docs/phase_plan.md
- docs/p11_final_validation_report.md
- docs/p11_to_p12_handoff.md
- docs/p11_private_trial_release_checklist.md
- docs/p11_visible_windows_smoke_evidence.md
- docs/p11_keyring_smoke_evidence.md
- docs/p11_keyring_packaging_decision.md
- docs/p11_packaged_trial_evidence.md
- docs/p11_provider_onboarding_notes.md
- docs/p11_key_rotation_least_privilege.md
- docs/p11_boundary_scan_evidence.md
- docs/p12_todo.md
- docs/p12_private_trial_pilot_feedback_triage_goal_guide.md
- docs/windows_smoke_checklist.md
- packaging/README.md
- RequireRealProvider.cmd
- StartTrial.cmd
- StartFakeTrial.cmd
- StartPackagedTrial.cmd
- StartPackagedFakeTrial.cmd
- SmokeTrial.cmd
- scripts/p11_visible_gui_smoke.py
- snaplex/app.py
- snaplex/trial_readiness.py
- snaplex/credentials.py
- tests/test_trial_readiness.py
- tests/test_release_smoke.py
- tests/test_credentials.py

P11 is planner-accepted. SnapLex has enough release-hardening evidence for a
controlled private trial, but the project still needs a repeatable pilot
operation plan, tester-facing materials, feedback triage rules, and explicit
go/no-go criteria before distributing builds more broadly.

Goal:
Prepare and validate the first controlled private-trial pilot. Produce
tester-facing release notes, feedback intake templates, pass/fail criteria,
manual environment-check instructions, optional real-provider smoke decision
rules, and credential-capable package variant decision notes. Preserve all P11
release-hardening and P10 credential boundaries.

Round budget:
- Rounds 1-8: main private-trial planning and evidence work.
- Rounds 9-11: buffer fixes for docs, smoke, packaging, or triage gaps.
- Round 12: final validation, report, and P13 handoff.

Rules:
- P12 is trial operations and feedback triage, not feature expansion.
- Do not implement production SnapLex Cloud, account OAuth, billing, hosted
  token broker, browser extension runtime, AI summary runtime, global hotkeys,
  provider rewrites, OCR/capture rewrites, or full localization.
- Do not require real provider credentials, real network calls, real OS keyring
  state, screen permissions, or model downloads in automated validation.
- Optional real-provider smoke may run only when local credentials already exist
  and a human intentionally approves using the network in that round. If not,
  document it as intentionally skipped.
- Do not collect or commit real tester personal data, provider secrets, `.env`
  files, screenshots with sensitive content, package outputs, logs, keyring
  exports, OCR caches, or smoke app data.
- Feedback templates must ask testers not to paste provider keys, secrets,
  private documents, or personal data.
- Keep base fake smoke deterministic and no-network.
- Every round must include Debug self-check, architecture self-check,
  validation commands and results, commit hash, push result, next-round target,
  and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to
  the next round.
```

## 1. Required Context

P11 accepted baseline:

- P11 final commit: `66d3cef11db492b6c6170c26b69e483528186767`.
- P11 validation passed with 255 tests.
- P11 added automated visible Windows GUI smoke, packaged trial evidence,
  keyring blocker evidence, provider onboarding polish, key rotation guidance,
  private-trial checklist, and boundary scan evidence.
- Manual Windows Credential Locker smoke remains blocked until optional
  `keyring` support is installed in a credential-capable environment.
- Real provider network smoke remains optional/manual only.
- Assistive technology, DPI scaling, and multi-monitor checks remain manual
  private-trial checks.

P12 planning decision:

- The next safest step is to run the project as a controlled private pilot,
  not to add new runtime scope.
- P12 should create durable trial materials and triage rules that a human tester
  can use without leaking secrets.
- P12 should decide whether a credential-capable package variant is worth a
  later implementation phase; it should not build or promise that variant unless
  explicitly approved.

## 2. Scope

P12 must complete:

- Revalidate the accepted P11 baseline.
- Create tester-facing private-trial release notes.
- Create feedback intake template and triage taxonomy.
- Define pass/fail criteria for the first private trial.
- Record manual environment check instructions and results/blockers for:
  assistive technology, DPI scaling, multi-monitor behavior, visible GUI,
  packaged fake smoke, and real/fake trial paths.
- Decide optional real-provider smoke policy for P12, including explicit
  approval and no-secret handling.
- Decide whether a credential-capable package variant should be built in a
  later phase, deferred, or rejected for the private pilot.
- Update private-trial checklist and onboarding docs.
- Preserve deterministic validation, package dry-run, fake smoke, and no-secret
  boundaries.
- Create preferred P12 docs:
  - `docs/p12_private_trial_release_notes.md`
  - `docs/p12_feedback_intake_template.md`
  - `docs/p12_trial_pass_fail_criteria.md`
  - `docs/p12_manual_environment_checks.md`
  - `docs/p12_real_provider_smoke_decision.md`
  - `docs/p12_credential_package_variant_decision.md`
  - `docs/p12_final_validation_report.md`
  - `docs/p12_to_p13_handoff.md`
- Update README, phase plan, development plan, smoke checklist, TODO, and
  planning entry points.

## 3. Non-Scope

Do not implement in P12:

- Production SnapLex Cloud.
- Production account OAuth, billing, hosted token broker, remote accounts, or
  cloud sync.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to trial feedback classification.
- OCR/capture rewrites.
- Full localization implementation.
- A credential-capable package variant unless the architect explicitly expands
  scope after the P12 decision.
- Automated tests that require real provider credentials, network calls, real
  OS keyring state, screen permissions, model downloads, or tester devices.
- Collection or storage of real tester personal data inside the repo.
- Committed screenshots, package outputs, local app data, `.env`, provider
  secrets, keyring exports, logs, OCR model caches, or smoke data.

## 4. Planner Decisions And Assumptions

- P12 uses a 12-round budget because it is operational hardening and triage
  setup, not a broad feature phase.
- Feedback intake should be local Markdown templates and checklists unless the
  user explicitly chooses an external issue tracker.
- Private-trial materials should support both source checkout and deterministic
  base package smoke.
- Real-provider smoke is opt-in only. If credentials are unavailable or the user
  does not explicitly approve network use, P12 should document a skipped result.
- P13 should be chosen after P12 based on feedback readiness; likely candidates
  are credential-capable package variant, localization foundation, or global
  hotkey feasibility.

## 5. Architecture Boundaries

Hard constraints:

- P10 credential boundaries remain intact.
- Provider setup and Test Connection remain behind services/presenters.
- Translation execution remains behind `TranslationPipeline`.
- Trial scripts keep fake and real paths separate.
- Feedback and release docs must not create new runtime truth that contradicts
  service/provider/config boundaries.
- Any user-facing copy must state current product reality: account OAuth,
  cloud accounts, hosted token broker, and packaged keyring support are not
  shipped.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P12 Private Trial Pilot And Feedback Triage
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

- Can the current change be explained by private-trial release notes, feedback
  intake, pass/fail criteria, manual environment checks, real-provider smoke
  decision, credential package decision, or docs?
- Can failures be localized to docs, package smoke, visible GUI smoke, trial
  readiness, credential readiness, feedback taxonomy, or boundary scan?
- Are fake smoke, real-trial fail-closed, skipped real-provider smoke,
  unavailable keyring, tester privacy, and no-secret states covered?
- If tester-facing material changed, does it tell testers not to paste secrets
  or personal data?
- If generated outputs were created, are they ignored and uncommitted?

Architecture self-check:

- Did P12 avoid adding runtime features outside private-trial operations?
- Did credential/provider/trial boundaries stay in their existing services?
- Did docs avoid promising account OAuth, cloud accounts, packaged keyring, or
  real network support beyond validated scope?
- Are feedback artifacts privacy-preserving and repo-safe?
- Are unrelated files, generated outputs, and user changes left alone?

## 7. Round Plan

Round 1 - Rebaseline and pilot scope:

- Revalidate P11 with the core validation matrix.
- Audit P11 limitations and private-trial checklist.
- Create or update `docs/p12_private_trial_release_notes.md` outline.

Round 2 - Tester-facing release notes:

- Finish private-trial release notes with install/run paths, fake versus real
  provider explanation, known limitations, and no-secret warnings.
- Keep copy consistent with README, TRY, and packaging docs.

Round 3 - Feedback intake template:

- Create `docs/p12_feedback_intake_template.md`.
- Include bug, usability, translation quality, credential setup, packaging,
  accessibility, DPI, multi-monitor, and provider onboarding categories.
- Add privacy instructions: no API keys, private documents, or personal data.

Round 4 - Pass/fail criteria:

- Create `docs/p12_trial_pass_fail_criteria.md`.
- Define pilot go/no-go gates, blocker severity, must-fix versus defer, and
  accepted known limitations.

Round 5 - Manual environment checks:

- Create `docs/p12_manual_environment_checks.md`.
- Run or document blockers for assistive technology, DPI scaling,
  multi-monitor behavior, visible GUI, packaged fake smoke, and trial scripts.

Round 6 - Optional real-provider smoke decision:

- Create `docs/p12_real_provider_smoke_decision.md`.
- If local credentials and explicit approval exist, run one narrow smoke and
  record no-secret evidence.
- Otherwise document an intentional skip and the exact future runbook.

Round 7 - Credential package variant decision:

- Create `docs/p12_credential_package_variant_decision.md`.
- Decide whether to build a credential-capable package in P13, defer it, or
  keep source checkout plus `.[credentials]`.

Round 8 - Trial triage workflow:

- Update private-trial checklist and docs index.
- Add a local triage workflow for classifying feedback into fix-now,
  investigate, defer, or reject.

Rounds 9-11 - Buffer hardening:

- Fix docs, smoke, package, privacy, or boundary issues found during pilot
  setup.
- Repeat relevant validation after each fix.
- Keep scope narrow.

Round 12 - Final validation, report, and P13 handoff:

- Create `docs/p12_final_validation_report.md`.
- Create `docs/p12_to_p13_handoff.md`.
- Mark `docs/p12_todo.md` complete.
- Update README, phase plan, development plan, smoke checklist, and AGENTS entry
  points to reflect P12 completion.
- Run final validation, boundary scans, commit, push, and report back to the
  planner/checker session for P12 acceptance.
- Recommend P13 based on private-trial readiness and remaining risks.

## 8. Validation Matrix

Required P12 validation:

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
- Docs link/index check for P12 docs.
- Artifact and secret boundary scan showing no committed `build/`, `dist/`,
  packaged binaries, generated config/history, `.env`, provider keys,
  screenshots, smoke data, local app data, logs, keyring exports, OCR caches,
  tester personal data, or API response captures.

Optional manual validation:

- Assistive technology checks.
- DPI and multi-monitor checks.
- Real-provider smoke only with existing local credentials and explicit human
  approval.
- Windows Credential Locker smoke only with installed optional credentials
  support and a throwaway fake value.

No P12 validation may require:

- Real provider credentials by default.
- Network calls in automated tests.
- Real OS keyring state.
- Production SnapLex Cloud or account OAuth.
- Committed screenshots, local secret stores, package outputs, or tester
  personal data.

## 9. PASS Criteria

P12 passes when:

- Tester-facing release notes exist and are privacy-safe.
- Feedback intake template and triage taxonomy exist.
- Pass/fail criteria for the first private trial exist.
- Manual environment checks are completed or blockers are explicitly recorded.
- Optional real-provider smoke has a clear run/skip decision.
- Credential-capable package variant has a clear build/defer/reject decision.
- P11/P10 credential, package, trial, and no-secret boundaries remain intact.
- Required validation and boundary scans pass.
- P12 final validation report and P12 to P13 handoff exist.
- Final P12 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P12 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Release notes:
- Feedback intake and triage:
- Trial pass/fail criteria:
- Manual environment checks:
- Optional real-provider smoke decision:
- Credential package variant decision:
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
P12 to P13 handoff:
- Accepted P12 baseline:
- Private-trial materials:
- Feedback triage model:
- Manual validation results/blockers:
- Credential package decision:
- Known trial gaps:
- Recommended P13 scope:
- Validation to preserve:
- Explicit non-scope:
```
