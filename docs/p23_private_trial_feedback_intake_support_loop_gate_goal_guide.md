# P23 Private Trial Feedback Intake And Support Loop Gate Goal Guide

Date: 2026-07-17

Role: executor

Round budget: 10 conversation rounds

## Direct Goal Prompt For Executor

Use `$donextgoal` to execute this P23 guide in goal mode. Work only from the
accepted P22 baseline. P23 runs a non-signing private-trial feedback intake and
support loop using P22's tester support and triage docs. If no external tester
feedback is supplied, record that honestly and keep package-lane validation
green. If feedback is supplied, triage it with privacy-safe evidence only.

Do not run signing commands. Do not create, import, purchase, invent, or use
certificates. Do not commit certificates, private keys, signed binaries, package
outputs, timestamp responses, screenshots, logs, `.env` files, keyring exports,
tester personal data, local app data, smoke data, OCR caches, or provider
secrets.

## Goal

P23 turns the P22 support materials into one real private-trial support loop:
intake, privacy screen, severity triage, response decision, package-lane
revalidation, and handoff. It should not fabricate tester feedback. It should
either process supplied feedback or record that none was supplied.

P23 is not a signing, installer, updater, public release, cloud/account, or
runtime feature phase.

## Required Reading

Read these before editing:

- `Role.md`
- `README.md`
- `AGENTS.md`
- `TRY.md`
- `docs/phase_plan.md`
- `docs/windows_smoke_checklist.md`
- `docs/p22_non_signing_private_trial_continuity_tester_support_gate_goal_guide.md`
- `docs/p22_final_validation_report.md`
- `docs/p22_to_p23_handoff.md`
- `docs/p22_unsigned_private_trial_release_notes.md`
- `docs/p22_tester_support_intake.md`
- `docs/p22_feedback_triage_criteria.md`
- `docs/p22_artifact_transfer_retention.md`
- `docs/p22_boundary_scan_evidence.md`
- `docs/p21_signing_unblock_requirements.md`

## Scope

- Revalidate the accepted P22 baseline.
- Keep signing paused and preserve the `unsigned-private-trial` trust label.
- Run one privacy-safe feedback intake pass.
- Record no external feedback honestly when none is supplied.
- If feedback is supplied, classify it with P22 severity/pass-fail rules.
- Produce support response decisions and a next-action register.
- Revalidate deterministic base package behavior.
- Revalidate explicit credentials package behavior.
- Preserve artifact transfer, retention, cleanup, and no-secret rules.
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
- Fabricated tester feedback.

## Architecture Boundaries

- Providers remain behind `TranslationProvider`, provider registry contracts,
  and `TranslationPipeline`.
- Credentials remain behind `CredentialService`/stores, `SettingsService`,
  `SettingsPresenter`, provider setup, and trial readiness.
- Feedback/support docs may describe flows, but must not move provider,
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

1. Rebaseline P22, current HEAD, package lanes, and signing pause state.
2. Run feedback intake inventory and privacy screen.
3. Record no-feedback state or triage supplied feedback.
4. Record support response decisions and next-action register.
5. Revalidate deterministic base package lane.
6. Revalidate explicit credentials package lane.
7. Refresh artifact transfer, retention, cleanup, and no-secret support loop
   evidence.
8. Run boundary, secret, private-key, certificate, package-output, screenshot,
   log, and signing-material scans.
9. Buffer: repair docs, links, package evidence, or triage clarity only.
10. Final validation, report, handoff, commit, and push.

## Required Deliverables

- `docs/p23_feedback_intake_log.md`
- `docs/p23_privacy_screen_and_triage.md`
- `docs/p23_support_response_decisions.md`
- `docs/p23_next_action_register.md`
- `docs/p23_base_package_continuity_evidence.md`
- `docs/p23_credentials_package_continuity_evidence.md`
- `docs/p23_artifact_retention_support_evidence.md`
- `docs/p23_boundary_scan_evidence.md`
- `docs/p23_final_validation_report.md`
- `docs/p23_to_p24_handoff.md`

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
- P23 docs link/index check.
- Artifact boundary scan.
- Secret, private-key, certificate, package-output, screenshot, log, and
  signing-material scans.

## Pass Criteria

P23 can pass when:

- P22 baseline remains intact.
- Signing remains PAUSED and no signing command runs.
- Feedback intake is recorded honestly without fabricated tester reports.
- Privacy screen and triage decisions are recorded for any supplied feedback.
- Support response decisions and next actions are current.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit and private-trial only.
- No generated artifacts, certificates, private keys, signed binaries, timestamp
  responses, screenshots, logs, `.env`, keyring exports, tester personal data,
  local app data, smoke data, OCR caches, or provider secrets are committed.
- Final report and P24 handoff are written.
- Validation matrix passes.
- Git status is clean and pushed to `origin/main`.

