# P20 Approved Signing Path Acquisition And Rehearsal Setup Gate Goal Guide

Date: 2026-07-17

Role: executor

Round budget: 12 conversation rounds

## Direct Goal Prompt For Executor

Use `$donextgoal` to execute this P20 guide in goal mode. Work only from the
accepted P19 baseline. P20 must decide whether SnapLex has an explicitly
approved safe throwaway/test signing path for an isolated local signing
rehearsal. If approval and all safety inputs exist, prepare and run only the
approved local rehearsal in ignored artifact paths. If approval is missing,
record BLOCKED or SKIPPED honestly and do not run signing commands.

Do not create, import, purchase, invent, or use production certificates. Do not
commit certificates, private keys, signed binaries, package outputs, timestamp
responses, screenshots, logs, `.env` files, keyring exports, tester personal
data, local app data, smoke data, OCR caches, or provider secrets.

## Goal

P20 is the acquisition/setup gate for a safe signing rehearsal path. It should
turn P19's "no approved signing path" limitation into one of two clear states:

- APPROVED: a safe throwaway/test signing path, ignored local artifact
  directory, command shape, evidence policy, cleanup policy, and stop conditions
  are explicitly documented and validated; or
- BLOCKED/SKIPPED: signing remains blocked because safe-path approval or
  required inputs are missing.

P20 is not a public release and not a production signing phase.

## Required Reading

Read these before editing:

- `Role.md`
- `README.md`
- `AGENTS.md`
- `docs/phase_plan.md`
- `docs/windows_smoke_checklist.md`
- `docs/p19_signing_rehearsal_signed_archive_candidate_gate_goal_guide.md`
- `docs/p19_final_validation_report.md`
- `docs/p19_to_p20_handoff.md`
- `docs/p19_signing_path_decision.md`
- `docs/p19_signing_rehearsal_evidence.md`
- `docs/p19_signature_verification_policy.md`
- `docs/p19_signed_archive_stop_conditions.md`
- `docs/p19_signed_archive_candidate_decision.md`
- `scripts/package_windows.py`
- `packaging/snaplex.spec`

## Scope

- Revalidate the accepted P19 baseline.
- Decide whether safe signing-path approval exists.
- Define the exact approval record required for any local signing rehearsal.
- If approval exists, restrict all rehearsal outputs to ignored local artifact
  paths and record non-secret evidence only.
- If approval is missing, record BLOCKED/SKIPPED and preserve package lanes.
- Revalidate deterministic base package behavior.
- Revalidate explicit credentials package behavior.
- Define cleanup, revocation, timestamp, trust, and verification handling for a
  future signed archive candidate.
- Preserve no-secret and no-artifact repository hygiene.

## Non-Scope

- Public release.
- Production signing, production certificate purchase/import/use, or certificate
  custody execution unless separately approved outside this phase.
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
- Signing work wraps local package artifacts only; it must not move provider,
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

## Debug Self-Check

Each round must answer:

- Can the current result be explained by the smallest signing-path or package
  lane workflow?
- Are success, expected rejection, missing approval, cleanup, no-secret, and
  no-artifact states covered?
- If a signing rehearsal runs, can failure be localized to command discovery,
  certificate availability, artifact path, timestamp policy, verification, or
  cleanup?
- If signing is blocked, is the missing approval or input precise enough for a
  planner or human owner to resolve later?

## Architecture Self-Check

Each round must confirm:

- Provider execution remains behind the provider registry and
  `TranslationPipeline`.
- Credential behavior remains behind credential services/stores and settings
  presenters.
- Base and credentials package lanes remain separate.
- No production signing, installer, updater, public release, cloud/OAuth,
  browser extension, AI summary, global hotkey, broad provider/OCR/capture
  rewrite, or full localization scope is pulled into P20.
- Generated outputs and signing material remain ignored and untracked.

## Round Plan

1. Rebaseline P19, current HEAD, package lanes, and ignored artifact state.
2. Record signing-path approval decision and required safety inputs.
3. Define ignored local artifact directories, cleanup rules, and evidence
   retention rules.
4. Define command discovery and signing rehearsal command shape without running
   signing unless approval exists.
5. If approval exists, run the isolated rehearsal; otherwise record
   BLOCKED/SKIPPED and continue validation.
6. Define signature verification, trust prompt, timestamp, and revocation
   evidence handling.
7. Revalidate deterministic base package lane.
8. Revalidate explicit credentials package lane.
9. Buffer: repair docs, package lane evidence, or blocked-state clarity only.
10. Buffer: optional approved rehearsal cleanup/hygiene only.
11. Buffer: final scan and evidence hardening only.
12. Final validation, report, handoff, commit, and push.

## Required Deliverables

- `docs/p20_signing_path_approval_record.md`
- `docs/p20_rehearsal_artifact_directory_policy.md`
- `docs/p20_signing_command_discovery.md`
- `docs/p20_isolated_rehearsal_evidence.md`
- `docs/p20_signature_verification_evidence_policy.md`
- `docs/p20_base_package_control_evidence.md`
- `docs/p20_credentials_package_control_evidence.md`
- `docs/p20_boundary_scan_evidence.md`
- `docs/p20_final_validation_report.md`
- `docs/p20_to_p21_handoff.md`

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
- `python scripts\p9_gui_smoke.py`
- `python scripts\p11_visible_gui_smoke.py`
- P20 docs link/index check.
- Artifact boundary scan.
- Secret, private-key, certificate, package-output, screenshot, log, and
  signing-material scans.
- Approved signing rehearsal verification only when safe-path approval exists.

## Pass Criteria

P20 can pass when:

- P19 baseline remains intact.
- Signing-path state is explicit: APPROVED with all required safety inputs, or
  BLOCKED/SKIPPED with a precise missing input list.
- No signing command runs without explicit safe-path approval.
- Any approved rehearsal uses only ignored local artifact paths and non-secret
  evidence.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit and private-trial only.
- No generated artifacts, certificates, private keys, signed binaries, timestamp
  responses, screenshots, logs, `.env`, keyring exports, tester personal data,
  local app data, smoke data, OCR caches, or provider secrets are committed.
- Final report and P21 handoff are written.
- Validation matrix passes or records an accepted, bounded skip/block for
  signing only.
- Git status is clean and pushed to `origin/main`.

