# P13 TODO

Date: 2026-07-16
Phase: P13 Private Trial Feedback Response And Credential Package Feasibility
Guide: `docs/p13_private_trial_feedback_response_credential_package_feasibility_goal_guide.md`
Status: ready for executor.
Estimated budget: 12 conversation rounds.

## Tasks

- [x] Revalidate the accepted P12 baseline.
- [x] Create a private-trial feedback response log.
- [x] Record whether external tester feedback exists; do not fabricate reports.
- [x] Triage supplied feedback or P12 known gaps using P12 severity rules.
- [x] Close any accepted S0/S1 pilot blockers with deterministic validation, or
      document blockers.
- [x] Capture assistive-technology, DPI, and multi-monitor manual results or
      blockers.
- [x] Record optional real-provider smoke run/skip evidence.
- [x] Record source keyring smoke pass/blocker evidence using only a throwaway
      fake value when optional credentials support is available.
- [ ] Decide credential-capable package feasibility for a later explicit phase.
- [ ] Preserve deterministic no-network tests, fake smoke, P10/P11/P12
      credential boundaries, fail-closed real trial paths, and no-secret
      repository hygiene.
- [ ] Produce P13 boundary scan evidence.
- [ ] Produce P13 final validation report.
- [ ] Produce P13 to P14 handoff.

## Deferred Outside P13

- Production SnapLex Cloud, account OAuth, billing, hosted token broker, remote
  accounts, or cloud sync.
- Raw API-key persistence in app config.
- Production browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to accepted S0/S1 pilot blockers.
- OCR/capture rewrites unrelated to accepted S0/S1 pilot blockers.
- Full localization implementation.
- Credential-capable package implementation unless explicitly approved after
  the P13 feasibility decision.
- Real network validation in automated tests.
- Committed screenshots, package outputs, local app data, `.env`, keyring
  exports, logs, OCR caches, smoke data, tester personal data, or provider
  secrets.
