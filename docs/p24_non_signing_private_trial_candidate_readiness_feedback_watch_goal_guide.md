# P24 Non-Signing Private Trial Candidate Readiness And Feedback Watch Gate Goal Guide

Date: 2026-07-17
Status: ready for executor use
Role: executor / implementation programmer
Round budget: 10 conversation rounds

## 0. Direct Goal Prompt For The Executor

You are executing P24 for SnapLex in `D:\ToolProjects\SnapLex`.

Goal: prepare a non-signing private-trial candidate readiness package and
feedback watch gate after accepted P23, while signing remains paused.

Use this guide as the source of truth. Do not run signing commands. Do not
create, import, purchase, invent, or use certificates. Do not fabricate tester
feedback. If no external feedback arrives, record that honestly and focus on
candidate-readiness, support watch, package-lane validation, and no-secret /
no-artifact hygiene.

Every round must end with validation, commit, push, and a round report. Do not
advance to the next round if validation, commit, or push fails.

## 1. Required Reading

- `Role.md`
- `AGENTS.md`
- `README.md`
- `docs/phase_plan.md`
- `docs/development_plan.md`
- `docs/windows_smoke_checklist.md`
- `docs/p23_private_trial_feedback_intake_support_loop_gate_goal_guide.md`
- `docs/p23_final_validation_report.md`
- `docs/p23_to_p24_handoff.md`
- `docs/p23_feedback_intake_log.md`
- `docs/p23_privacy_screen_and_triage.md`
- `docs/p23_support_response_decisions.md`
- `docs/p23_next_action_register.md`
- `docs/p23_boundary_scan_evidence.md`
- `docs/p21_signing_unblock_requirements.md`

## 2. Scope

- Revalidate the accepted P23 baseline and current signing pause state.
- Create a non-signing private-trial candidate readiness record.
- Create a feedback watch register that can accept late external feedback
  without storing private payloads.
- Refresh tester support runbook language for unsigned/private-trial use.
- Revalidate deterministic base package candidate behavior.
- Revalidate explicit credentials package candidate behavior with throwaway
  values only.
- Record a release-hold decision that keeps public release, installer, updater,
  release feed, signed archive, and signing out of scope.
- Preserve no-secret, no-artifact, no-screenshot, no-log, no-package-output, and
  no-signing-material repository hygiene.

## 3. Non-Scope

- Signing commands.
- Certificate creation, import, purchase, invention, or use.
- Timestamp service calls.
- Signed binaries, signed archives, installers, updaters, release feeds, public
  release artifacts, or public support channel launch.
- SnapLex Cloud, OAuth, billing, hosted token broker, browser extension runtime,
  AI summary runtime, global hotkeys, broad provider/OCR/capture rewrites, or
  full localization.
- Real-provider network smoke unless existing local credentials and explicit
  human network approval are supplied.
- Fabricated tester feedback or invented tester devices.
- Silent keyring support in the base package.

## 4. Architecture And Privacy Boundaries

- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The credentials package remains explicit and private-trial only.
- No raw provider secrets, keyring exports, `.env` files, logs, screenshots,
  local app data, package outputs, OCR caches, tester personal data,
  certificates, private keys, signed binaries, timestamp responses, or signing
  materials may be committed.
- Signing remains PAUSED until a later planner-approved signing phase supplies
  every required unblock input.

## 5. Per-Round Gate

Every round summary must include:

- Round goal.
- Completed work.
- Debug self-check.
- Architecture self-check.
- Validation commands and results.
- Commit hash and push result.
- Next round goal.
- Whether a buffer round was consumed.

Progression rules:

- If validation fails, do not commit, do not push, and do not advance.
- If validation passes but commit fails, do not advance.
- If commit succeeds but push fails, do not advance.
- Only after push succeeds may the executor continue to the next round.

Debug self-check:

- Can the current evidence be traced to a concrete private-trial support or
  package candidate workflow?
- Are success, expected rejection, no-feedback, late-feedback, cleanup, and
  unsupported states covered where relevant?
- Are generated artifacts ignored and excluded from git?
- Is any real network, real credential, tester payload, or signing action
  explicitly gated?

Architecture self-check:

- Did provider, credential, settings, packaging, and trial-readiness boundaries
  stay separated?
- Did the phase avoid pulling signing, public release, cloud/account, browser,
  AI summary, hotkey, or broad runtime feature scope into P24?
- Did the base package remain deterministic and keyring-free?
- Did the credentials package remain explicit/private-trial?
- Were unrelated files and generated outputs left alone?

## 6. Round Plan

Round 1: Rebaseline P23 and signing pause state.

- Confirm HEAD, `origin/main`, P23 report, and handoff.
- Record accepted P23 commit and P24 assumptions.

Round 2: Candidate readiness record.

- Create `docs/p24_unsigned_candidate_readiness.md`.
- Include candidate trust label, supported package lanes, setup expectations,
  trial blockers, and release-hold boundaries.

Round 3: Feedback watch register.

- Create `docs/p24_feedback_watch_register.md`.
- Record whether external feedback arrived.
- If feedback arrives, screen it for privacy before storing any summary.
- If none arrives, record no-feedback honestly.

Round 4: Tester support runbook refresh.

- Create `docs/p24_support_watch_runbook.md`.
- Cover intake, escalation, privacy screen, real-provider support gate,
  credential package support gate, and unsigned trust prompt handling.

Round 5: Base package candidate lane.

- Create `docs/p24_base_package_candidate_evidence.md`.
- Validate source fake smoke, packaged fake smoke, real-provider expected
  rejection, dry-run/build as needed, and base credential-smoke expected
  rejection.

Round 6: Credentials package candidate lane.

- Create `docs/p24_credentials_package_candidate_evidence.md`.
- Validate credentials dry-run/build and packaged import/cycle/save/check-delete
  smoke using generated throwaway values only.
- Restore base package behavior after credentials smoke.

Round 7: Release-hold and support decision.

- Create `docs/p24_release_hold_decision.md`.
- Decide whether the non-signing private-trial candidate remains support-ready,
  stays held, or needs repair before more testers.
- Do not approve public release or signing.

Round 8: Boundary scans.

- Create `docs/p24_boundary_scan_evidence.md`.
- Check docs index, generated outputs, package artifacts, screenshots, logs,
  certificates, private keys, signing materials, and common token patterns.

Round 9: Buffer.

- Use only for fixing docs, links, package evidence, support runbook clarity, or
  validation drift.
- If unused, record that no buffer was consumed.

Round 10: Final validation and handoff.

- Create `docs/p24_final_validation_report.md`.
- Create `docs/p24_to_p25_handoff.md`.
- Run final validation matrix and push before reporting READY_FOR_CHECK.

## 7. Required Deliverables

- `docs/p24_unsigned_candidate_readiness.md`
- `docs/p24_feedback_watch_register.md`
- `docs/p24_support_watch_runbook.md`
- `docs/p24_base_package_candidate_evidence.md`
- `docs/p24_credentials_package_candidate_evidence.md`
- `docs/p24_release_hold_decision.md`
- `docs/p24_boundary_scan_evidence.md`
- `docs/p24_final_validation_report.md`
- `docs/p24_to_p25_handoff.md`

## 8. Validation Matrix

Run when feasible and record results:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python -m snaplex --check-real-provider` as expected rejection when no real
  provider is configured
- `python scripts\package_windows.py --dry-run --variant base`
- `python scripts\package_windows.py --dry-run --variant credentials`
- `cmd /c StartTrial.cmd --no-gui` as expected rejection when no real provider
  is configured
- `cmd /c StartFakeTrial.cmd --no-gui`
- `cmd /c SmokeTrial.cmd`
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`
- `cmd /c StartPackagedTrial.cmd --no-gui` as expected rejection when no real
  provider is configured
- Base package credential smoke as expected rejection
- Credentials package build/import/cycle/save/check-delete smoke
- Final base package restore and base credential-smoke expected rejection
- P24 docs link/index check
- Artifact/generated-output scan
- Certificate/private-key/signing-material extension scan
- Non-documentation secret/private-key content scan

## 9. PASS Criteria

- P23 baseline and final commit are correctly recorded.
- P24 records no-feedback honestly unless real external feedback is supplied.
- Late-feedback handling is privacy-safe.
- Candidate readiness, support watch, package lanes, release hold, and boundary
  evidence are documented.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit and private-trial only.
- Signing remains paused and no signing artifacts or commands appear.
- Full validation matrix passes or has documented, acceptable expected
  rejections.
- No generated artifacts, package outputs, screenshots, logs, local app data,
  `.env`, keyring exports, OCR caches, tester personal data, certificates,
  private keys, signed binaries, timestamp responses, or provider secrets are
  committed.
- Final report and P25 handoff are present.

## 10. Final Report Template

The READY_FOR_CHECK report back to planner must include:

- phase name
- final commit
- push result
- rounds used and buffer consumed
- pass report path
- handoff path
- deliverables
- validation evidence
- key boundaries preserved
- known limitations
- recommended next phase
