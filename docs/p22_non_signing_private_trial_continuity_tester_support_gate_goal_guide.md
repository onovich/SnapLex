# P22 Non-Signing Private Trial Continuity And Tester Support Gate Goal Guide

Date: 2026-07-17

Role: executor

Round budget: 10 conversation rounds

## Direct Goal Prompt For Executor

Use `$donextgoal` to execute this P22 guide in goal mode. Work only from the
accepted P21 baseline. P22 continues unsigned/private-trial readiness while
signing remains paused. Improve tester-facing continuity, support, feedback,
trust-label, transfer, and package-lane evidence without introducing new runtime
features and without running signing commands.

Do not run signing commands. Do not create, import, purchase, invent, or use
certificates. Do not commit certificates, private keys, signed binaries, package
outputs, timestamp responses, screenshots, logs, `.env` files, keyring exports,
tester personal data, local app data, smoke data, OCR caches, or provider
secrets.

## Goal

P22 keeps the project useful while signing is paused. It should make the
unsigned/private-trial package lane easier to support by producing current,
tester-facing operational docs and a clear triage loop, while preserving all
package, credential, provider, and no-secret boundaries.

P22 is not a signing, installer, updater, public release, or runtime feature
phase.

## Required Reading

Read these before editing:

- `Role.md`
- `README.md`
- `AGENTS.md`
- `TRY.md`
- `docs/phase_plan.md`
- `docs/windows_smoke_checklist.md`
- `docs/p21_signing_path_unblock_decision_pause_gate_goal_guide.md`
- `docs/p21_final_validation_report.md`
- `docs/p21_to_p22_handoff.md`
- `docs/p21_signing_path_decision.md`
- `docs/p21_signing_unblock_requirements.md`
- `docs/p21_next_phase_recommendation.md`
- `docs/p21_boundary_scan_evidence.md`
- `docs/p12_private_trial_release_notes.md`
- `docs/p12_feedback_intake_template.md`
- `docs/p12_trial_pass_fail_criteria.md`
- `docs/p12_trial_triage_workflow.md`
- `docs/p16_tester_setup_cleanup_guide.md`
- `docs/p17_artifact_transfer_retention_support.md`

## Scope

- Revalidate the accepted P21 baseline.
- Keep signing explicitly paused and document that private-trial artifacts are
  unsigned.
- Refresh tester-facing unsigned/private-trial instructions.
- Refresh support intake and escalation flow for unsigned private trials.
- Refresh feedback triage criteria for current package lanes.
- Revalidate deterministic base package behavior.
- Revalidate explicit credentials package behavior.
- Record artifact transfer, retention, trust-label, and privacy guidance for
  unsigned/private-trial testers.
- Preserve no-secret and no-artifact repository hygiene.

## Non-Scope

- Signing command execution.
- Certificate creation, import, purchase, invention, or use.
- Timestamp service calls.
- Signed binary or signed archive candidate creation.
- Public release.
- Production signing.
- Installer runtime, updater runtime, release feed, auto-update behavior, or
  public support channel.
- Silent keyring support in the base package.
- SnapLex Cloud, OAuth, billing, hosted token broker, browser extension runtime,
  AI summary runtime, global hotkeys, broad provider/OCR/capture rewrites, or
  full localization.
- Real-provider network smoke unless local credentials exist and the human
  explicitly approves network use.

## Architecture Boundaries

- Providers remain behind `TranslationProvider`, provider registry contracts,
  and `TranslationPipeline`.
- Credentials remain behind `CredentialService`/stores, `SettingsService`,
  `SettingsPresenter`, provider setup, and trial readiness.
- Tester/support docs may describe flows, but must not move provider,
  credential, UI, capture, OCR, or storage rules into packaging docs.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit and private-trial only.
- Signing remains paused until a later planner-approved signing phase receives
  every input listed in `docs/p21_signing_unblock_requirements.md`.

## Per-Round Gate

Every round must report:

- round goal;
- completed work;
- Debug self-check;
- architecture self-check;
- validation commands and results;
- commit hash and push result;
- next round goal;
- whether a buffer round was consumed.

Progression rules:

- If validation fails, do not commit, do not push, and do not proceed.
- If commit or push fails, do not proceed.
- Only proceed after validation, commit, and push succeed.
- Do not stage unrelated untracked files.

## Round Plan

1. Rebaseline P21, current HEAD, package lanes, and signing pause state.
2. Refresh unsigned/private-trial tester instructions and trust-label language.
3. Refresh support intake, privacy guidance, and escalation rules.
4. Refresh feedback triage criteria and pass/fail language.
5. Revalidate deterministic base package lane.
6. Revalidate explicit credentials package lane.
7. Record artifact transfer, retention, cleanup, and no-secret evidence.
8. Run boundary, secret, private-key, certificate, package-output, screenshot,
   log, and signing-material scans.
9. Buffer: repair docs, links, package evidence, or support clarity only.
10. Final validation, report, handoff, commit, and push.

## Required Deliverables

- `docs/p22_unsigned_private_trial_release_notes.md`
- `docs/p22_tester_support_intake.md`
- `docs/p22_feedback_triage_criteria.md`
- `docs/p22_artifact_transfer_retention.md`
- `docs/p22_base_package_continuity_evidence.md`
- `docs/p22_credentials_package_continuity_evidence.md`
- `docs/p22_boundary_scan_evidence.md`
- `docs/p22_final_validation_report.md`
- `docs/p22_to_p23_handoff.md`

## Validation Matrix

Run and record:

- `Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python -m snaplex --check-real-provider` with expected rejection when no real
  provider is configured.
- `python scripts\package_windows.py --dry-run --variant base`
- `python scripts\package_windows.py --dry-run --variant credentials`
- `cmd /c StartTrial.cmd --no-gui` expected rejection when no real provider is
  configured.
- `cmd /c StartFakeTrial.cmd --no-gui`
- `cmd /c SmokeTrial.cmd`
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`
- `cmd /c StartPackagedTrial.cmd --no-gui` expected rejection when no real
  provider is configured.
- Base package credential smoke expected rejection.
- Credentials package build and `--smoke-credentials` import/cycle/save/check-delete.
- Final base package restore and base credential smoke expected rejection.
- P22 docs link/index check.
- Artifact boundary scan.
- Secret, private-key, certificate, package-output, screenshot, log, and
  signing-material scans.

## Pass Criteria

P22 can pass when:

- P21 baseline remains intact.
- Signing remains PAUSED and no signing command runs.
- Tester-facing unsigned/private-trial instructions are current.
- Support intake, privacy guidance, escalation, and feedback triage are current.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit and private-trial only.
- No generated artifacts, certificates, private keys, signed binaries, timestamp
  responses, screenshots, logs, `.env`, keyring exports, tester personal data,
  local app data, smoke data, OCR caches, or provider secrets are committed.
- Final report and P23 handoff are written.
- Validation matrix passes.
- Git status is clean and pushed to `origin/main`.

