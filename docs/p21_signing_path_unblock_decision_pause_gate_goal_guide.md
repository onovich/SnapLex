# P21 Signing Path Unblock Decision Or Pause Gate Goal Guide

Date: 2026-07-17

Role: executor

Round budget: 8 conversation rounds

## Direct Goal Prompt For Executor

Use `$donextgoal` to execute this P21 guide in goal mode. Work only from the
accepted P20 baseline. P21 must make one explicit decision: either a safe
throwaway/test signing path is supplied and can be handed to a later isolated
rehearsal phase, or signing work is paused because approval and tooling remain
missing.

Do not run signing commands in P21. Do not create, import, purchase, invent, or
use certificates. Do not commit certificates, private keys, signed binaries,
package outputs, timestamp responses, screenshots, logs, `.env` files, keyring
exports, tester personal data, local app data, smoke data, OCR caches, or
provider secrets.

## Goal

P21 turns the P20 BLOCKED/SKIPPED signing state into an explicit project
decision:

- UNBLOCKED FOR FUTURE REHEARSAL: all safe-path approval inputs are supplied,
  and a later phase may run a signing rehearsal under those conditions; or
- PAUSED: signing remains blocked and should stop consuming phase cycles until
  a human supplies the missing safe-path inputs.

P21 is a decision/pause gate. It is not a signing rehearsal, signed archive,
installer, updater, or public release phase.

## Required Reading

Read these before editing:

- `Role.md`
- `README.md`
- `AGENTS.md`
- `docs/phase_plan.md`
- `docs/windows_smoke_checklist.md`
- `docs/p20_approved_signing_path_acquisition_rehearsal_setup_gate_goal_guide.md`
- `docs/p20_final_validation_report.md`
- `docs/p20_to_p21_handoff.md`
- `docs/p20_signing_path_approval_record.md`
- `docs/p20_signing_command_discovery.md`
- `docs/p20_isolated_rehearsal_evidence.md`
- `docs/p20_signature_verification_evidence_policy.md`
- `docs/p20_boundary_scan_evidence.md`

## Scope

- Revalidate the accepted P20 baseline.
- Decide whether safe signing-path approval has been supplied after P20.
- If approval exists, record all approval inputs and prepare a later-phase
  handoff without running signing.
- If approval is still missing, record signing as PAUSED and list exact unblock
  inputs.
- Preserve deterministic base package validation.
- Preserve explicit credentials package validation.
- Recommend the next non-signing or signing-rehearsal phase based on the
  decision.
- Preserve no-secret and no-artifact repository hygiene.

## Non-Scope

- Running signing commands.
- Public release.
- Production signing, production certificate purchase/import/use, or certificate
  custody execution.
- Committed certificates, private keys, signed binaries, package outputs,
  timestamp responses, screenshots, logs, `.env`, keyring exports, tester
  personal data, local app data, smoke data, OCR caches, or provider secrets.
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
- Signing policy wraps package artifacts only; it must not move provider,
  credential, UI, capture, OCR, or storage rules into packaging code.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit and private-trial only.

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

1. Rebaseline P20, current HEAD, package lanes, and ignored artifact state.
2. Decide whether safe signing-path approval exists and record APPROVED or
   PAUSED.
3. If PAUSED, write unblock requirements and next non-signing recommendation.
   If APPROVED, write later-rehearsal handoff without running signing.
4. Revalidate deterministic base package lane.
5. Revalidate explicit credentials package lane.
6. Run boundary, secret, private-key, certificate, package-output, screenshot,
   log, and signing-material scans.
7. Buffer: repair docs, links, or decision clarity only.
8. Final validation, report, handoff, commit, and push.

## Required Deliverables

- `docs/p21_signing_path_decision.md`
- `docs/p21_signing_unblock_requirements.md`
- `docs/p21_next_phase_recommendation.md`
- `docs/p21_base_package_control_evidence.md`
- `docs/p21_credentials_package_control_evidence.md`
- `docs/p21_boundary_scan_evidence.md`
- `docs/p21_final_validation_report.md`
- `docs/p21_to_p22_handoff.md`

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
- P21 docs link/index check.
- Artifact boundary scan.
- Secret, private-key, certificate, package-output, screenshot, log, and
  signing-material scans.

## Pass Criteria

P21 can pass when:

- P20 baseline remains intact.
- Signing-path state is explicit: APPROVED for later rehearsal, or PAUSED with
  exact unblock requirements.
- No signing command runs.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit and private-trial only.
- No generated artifacts, certificates, private keys, signed binaries, timestamp
  responses, screenshots, logs, `.env`, keyring exports, tester personal data,
  local app data, smoke data, OCR caches, or provider secrets are committed.
- Final report and P22 handoff are written.
- Validation matrix passes.
- Git status is clean and pushed to `origin/main`.

