# P25 Non-Signing Private Trial Feedback Watch Pause Closeout Gate Goal Guide

Date: 2026-07-17
Status: ready for executor use
Role: executor / implementation programmer
Round budget: 8 conversation rounds

## 0. Direct Goal Prompt For The Executor

You are executing P25 for SnapLex in `D:\ToolProjects\SnapLex`.

Goal: run a short non-signing private-trial feedback watch and pause/closeout
gate after accepted P24. Decide whether the unsigned/private-trial lane remains
watch-active, should pause awaiting real feedback, or needs a later planner
decision. Do not resume signing or public release work.

Every round must end with validation, commit, push, and a round report. Do not
advance to the next round if validation, commit, or push fails.

## 1. Required Reading

- `Role.md`
- `AGENTS.md`
- `README.md`
- `docs/phase_plan.md`
- `docs/development_plan.md`
- `docs/windows_smoke_checklist.md`
- `docs/p24_non_signing_private_trial_candidate_readiness_feedback_watch_goal_guide.md`
- `docs/p24_final_validation_report.md`
- `docs/p24_to_p25_handoff.md`
- `docs/p24_unsigned_candidate_readiness.md`
- `docs/p24_feedback_watch_register.md`
- `docs/p24_support_watch_runbook.md`
- `docs/p24_release_hold_decision.md`
- `docs/p24_boundary_scan_evidence.md`
- `docs/p21_signing_unblock_requirements.md`

## 2. Scope

- Revalidate the accepted P24 baseline and current signing pause state.
- Keep a privacy-safe feedback watch record.
- If external feedback is supplied, screen and classify it without committing
  private payloads.
- If no feedback is supplied, record no-feedback honestly and decide whether to
  pause the lane.
- Refresh the non-signing candidate support/readiness status.
- Run lightweight deterministic source/package validation.
- Preserve package-lane separation, no-secret hygiene, and release-hold state.
- Produce a P25 final report and P25 to P26 handoff or closeout recommendation.

## 3. Non-Scope

- Signing commands.
- Certificate creation, import, purchase, invention, or use.
- Timestamp service calls.
- Signed binaries, signed archives, installers, updaters, release feeds, public
  release artifacts, or broader distribution approval.
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

- Is the watch/pause decision grounded in supplied evidence rather than assumed
  tester feedback?
- Are expected rejections, no-feedback, late-feedback, cleanup, and unsupported
  states covered?
- Are generated artifacts ignored and excluded from git?
- Is any real network, credential, tester payload, or signing action explicitly
  gated?

Architecture self-check:

- Did provider, credential, settings, packaging, and trial-readiness boundaries
  stay separated?
- Did the phase avoid pulling signing, public release, cloud/account, browser,
  AI summary, hotkey, or broad runtime feature scope into P25?
- Did the base package remain deterministic and keyring-free?
- Did the credentials package remain explicit/private-trial?
- Were unrelated files and generated outputs left alone?

## 6. Round Plan

Round 1: Rebaseline P24 and signing pause state.

- Confirm HEAD, `origin/main`, P24 report, and handoff.
- Record accepted P24 commit and P25 assumptions.

Round 2: Feedback watch disposition.

- Create `docs/p25_feedback_watch_disposition.md`.
- Record supplied feedback or no-feedback honestly.
- Screen any supplied feedback before recording summaries.

Round 3: Pause/continue decision.

- Create `docs/p25_private_trial_pause_continue_decision.md`.
- Decide whether the non-signing private-trial lane remains watch-active, pauses
  awaiting real feedback, or needs a later planner decision.

Round 4: Support/readiness closeout refresh.

- Create `docs/p25_support_readiness_closeout.md`.
- Summarize candidate state, tester support status, privacy rules, and release
  hold.

Round 5: Lightweight package/source revalidation.

- Create `docs/p25_package_revalidation_evidence.md`.
- Run deterministic source and packaged smoke checks appropriate to a pause gate.
- Keep base/credentials lane separation explicit.

Round 6: Boundary scans.

- Create `docs/p25_boundary_scan_evidence.md`.
- Check docs index, generated outputs, package artifacts, screenshots, logs,
  certificates, private keys, signing materials, and common token patterns.

Round 7: Buffer.

- Use only for fixing docs, links, package evidence, support clarity, or
  validation drift.
- If unused, record that no buffer was consumed.

Round 8: Final validation and handoff.

- Create `docs/p25_final_validation_report.md`.
- Create `docs/p25_to_p26_handoff.md`.
- Run final validation matrix and push before reporting READY_FOR_CHECK.

## 7. Required Deliverables

- `docs/p25_feedback_watch_disposition.md`
- `docs/p25_private_trial_pause_continue_decision.md`
- `docs/p25_support_readiness_closeout.md`
- `docs/p25_package_revalidation_evidence.md`
- `docs/p25_boundary_scan_evidence.md`
- `docs/p25_final_validation_report.md`
- `docs/p25_to_p26_handoff.md`

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
- Credentials package smoke only if the pause/continue decision needs another
  explicit credentials package check
- Final base package restore and base credential-smoke expected rejection if a
  credentials package build was run
- P25 docs link/index check
- Artifact/generated-output scan
- Certificate/private-key/signing-material extension scan
- Non-documentation secret/private-key content scan

## 9. PASS Criteria

- P24 baseline and final commit are correctly recorded.
- Feedback is recorded honestly: supplied feedback is privacy-screened, or
  no-feedback is recorded without fabrication.
- Pause/continue decision is explicit and does not approve signing or public
  release.
- Support/readiness closeout and package revalidation evidence are documented.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit and private-trial only.
- Signing remains paused and no signing artifacts or commands appear.
- Validation matrix passes or has documented, acceptable expected rejections.
- No generated artifacts, package outputs, screenshots, logs, local app data,
  `.env`, keyring exports, OCR caches, tester personal data, certificates,
  private keys, signed binaries, timestamp responses, or provider secrets are
  committed.
- Final report and P26 handoff or closeout recommendation are present.

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
- recommended next phase or pause/closeout recommendation
