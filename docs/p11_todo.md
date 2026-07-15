# P11 TODO

P11 goal: harden SnapLex for private Windows trial release by validating visible
desktop behavior, manual credential/keyring behavior, packaged trial behavior,
and provider onboarding clarity while preserving P10 credential boundaries.

Status: complete, planner-accepted.

Executable guide: `docs/p11_trial_release_hardening_goal_guide.md`

Estimated budget: 12 conversation rounds.

## Tasks

- [x] Revalidate the accepted P10 baseline.
- [x] Audit release risks from P10 handoff, package docs, and smoke checklist.
- [x] Run visible Windows GUI smoke or document the exact blocker.
- [x] Run Windows Credential Locker/keyring smoke with a throwaway fake secret
  or document the exact blocker.
- [x] Decide and document packaged keyring/credential support.
- [x] Recheck packaged fake smoke and real-trial fail-closed behavior.
- [x] Polish provider onboarding and credential setup copy.
- [x] Add key rotation and least-privilege notes.
- [x] Consolidate release smoke and private trial checklist docs.
- [x] Preserve P10 no-secret boundaries and deterministic no-network tests.
- [x] Produce P11 final validation report.
- [x] Produce P11 to P12 handoff.

## Deferred Outside P11

- Production SnapLex Cloud, account OAuth, billing, hosted token broker, or
  remote accounts.
- Raw API-key persistence in app config.
- Production browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to release-hardening validation or onboarding
  copy.
- OCR/capture rewrites.
- Full localization implementation.
- Real network validation in automated tests.
- Committed screenshots, package outputs, local app data, `.env`, keyring
  exports, logs, OCR model caches, or secrets.
