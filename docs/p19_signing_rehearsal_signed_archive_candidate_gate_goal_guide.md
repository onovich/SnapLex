# P19 Signing Rehearsal And Signed Archive Candidate Gate Goal Mode Guide

Date: 2026-07-17

Role: executor

Round budget: 12 conversation rounds

## Goal

P19 must decide whether SnapLex has an approved safe throwaway/test signing path
for an isolated signing rehearsal. If such a path is available, run the
rehearsal only in ignored local artifact paths and record verification evidence
without committing certificates, private keys, signed binaries, package outputs,
timestamp responses, screenshots, logs, or secrets.

If no safe path is supplied, P19 must record a precise SKIPPED or BLOCKED
decision and still preserve the base and credentials package validation lanes.

P19 is a signing rehearsal and signed archive candidate gate. It is not a public
release.

## Required Reading

Read these before editing:

- `Role.md`
- `README.md`
- `AGENTS.md`
- `docs/phase_plan.md`
- `docs/windows_smoke_checklist.md`
- `docs/p18_signing_distribution_readiness_gate_goal_guide.md`
- `docs/p18_final_validation_report.md`
- `docs/p18_to_p19_handoff.md`
- `docs/p18_signing_identity_certificate_custody.md`
- `docs/p18_signing_verification_policy.md`
- `docs/p18_signing_rehearsal_record.md`
- `docs/p18_distribution_readiness_decision.md`
- `docs/p18_package_validation_evidence.md`
- `scripts/package_windows.py`
- `packaging/snaplex.spec`

## Scope

- Reconfirm P18 signing and distribution decisions.
- Decide whether an approved safe throwaway/test signing path exists.
- If approved, run only an isolated local signing rehearsal with non-production
  test material.
- If not approved, record SKIPPED or BLOCKED honestly.
- Revalidate base package behavior as deterministic and keyring-free.
- Revalidate credentials package behavior as explicit and private-trial only.
- Define signed archive candidate stop conditions, cleanup expectations,
  verification policy, timestamp policy, and support/revocation notes.
- Preserve no-secret and no-artifact repository hygiene.

## Non-Scope

- Public release.
- Production certificate purchase, import, custody execution, or use unless
  explicitly approved outside this goal.
- Committing certificates, private keys, signed binaries, package outputs,
  timestamp responses, screenshots, logs, `.env`, keyring exports, tester
  personal data, local app data, smoke data, OCR caches, or provider secrets.
- Installer runtime, updater runtime, release feed, or auto-update behavior.
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
- Signing/distribution work wraps local package artifacts only; it must not move
  provider, credential, UI, capture, OCR, or storage rules into packaging code.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit as the credentials variant and
  private-trial until a later gate approves a broader release.

## Round Plan

1. Rebaseline P18 reports, current HEAD, and local ignored artifact state.
2. Record P19 signing path decision: approved safe rehearsal, SKIPPED, or
   BLOCKED.
3. Revalidate base package control lane.
4. Revalidate credentials package candidate lane.
5. Run approved signing rehearsal or record why it was not run.
6. Record signature verification, trust, timestamp, and evidence policy.
7. Define signed archive stop conditions, cleanup, and rollback implications.
8. Decide whether a signed archive candidate can proceed to a later release
   gate.
9. Buffer: repair docs, links, or validation only.
10. Buffer: package-lane or hygiene rehearsal only.
11. Buffer: final scan and evidence hardening only.
12. Final validation, report, handoff, commit, and push.

## Required Deliverables

- `docs/p19_signing_path_decision.md`
- `docs/p19_base_package_control_evidence.md`
- `docs/p19_credentials_package_candidate_evidence.md`
- `docs/p19_signing_rehearsal_evidence.md`
- `docs/p19_signature_verification_policy.md`
- `docs/p19_signed_archive_stop_conditions.md`
- `docs/p19_signed_archive_candidate_decision.md`
- `docs/p19_boundary_scan_evidence.md`
- `docs/p19_final_validation_report.md`
- `docs/p19_to_p20_handoff.md`

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
- Base package build and smoke.
- Credentials package build and `--smoke-credentials` import/cycle/save/check-delete.
- Restored base package credential smoke expected rejection.
- `cmd /c StartTrial.cmd --no-gui` expected rejection when no real provider is
  configured.
- `cmd /c StartFakeTrial.cmd --no-gui`
- `cmd /c SmokeTrial.cmd`
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`
- `cmd /c StartPackagedTrial.cmd --no-gui` expected rejection when no real
  provider is configured.
- `python scripts\p9_gui_smoke.py`
- `python scripts\p11_visible_gui_smoke.py`
- P19 docs link/index check.
- Artifact boundary scan.
- Secret, private-key, certificate, and signing-material scan.
- Signing rehearsal verification only when an approved safe throwaway/test
  signing path exists.

## Pass Criteria

P19 can pass when:

- P18 baseline remains intact.
- Signing path decision is recorded without inventing certificates or approval.
- Any signing rehearsal uses only approved throwaway/test material in ignored
  local artifact paths.
- If signing is skipped or blocked, the reason is precise and actionable.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit and private-trial only.
- No generated artifacts, certificates, private keys, signed binaries, timestamp
  responses, screenshots, logs, `.env`, keyring exports, tester personal data,
  local app data, smoke data, OCR caches, or provider secrets are committed.
- Final report and P20 handoff are written.
- Validation matrix passes or records an accepted, bounded skip/block.
- Git status is clean and pushed to `origin/main`.

