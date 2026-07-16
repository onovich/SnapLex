# P12 TODO

P12 goal: prepare the first controlled private-trial pilot by producing
tester-facing release notes, feedback intake templates, pass/fail criteria,
manual environment checks, optional real-provider smoke policy, and credential
package variant decision notes while preserving P11/P10 boundaries.

Status: executor-complete; ready for planner check.

Executable guide: `docs/p12_private_trial_pilot_feedback_triage_goal_guide.md`

Estimated budget: 12 conversation rounds.

## Tasks

- [x] Revalidate the accepted P11 baseline.
- [x] Produce private-trial release notes for testers.
- [x] Produce feedback intake template and triage taxonomy.
- [x] Define first private-trial pass/fail criteria.
- [x] Run or document manual assistive-technology, DPI, multi-monitor, visible
  GUI, packaged fake smoke, and trial-script checks.
- [x] Decide optional real-provider smoke policy and record run/skip evidence.
- [x] Decide whether credential-capable package variant should be built,
  deferred, or rejected for the private pilot.
- [x] Update private-trial checklist and onboarding docs.
- [x] Preserve deterministic no-network tests, fake smoke, P10 credential
  boundaries, and no-secret repository hygiene.
- [x] Produce P12 final validation report.
- [x] Produce P12 to P13 handoff.

## Deferred Outside P12

- Production SnapLex Cloud, account OAuth, billing, hosted token broker, or
  remote accounts.
- Raw API-key persistence in app config.
- Production browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to private-trial feedback classification.
- OCR/capture rewrites.
- Full localization implementation.
- Credential-capable package implementation unless explicitly approved later.
- Real network validation in automated tests.
- Committed screenshots, package outputs, local app data, `.env`, keyring
  exports, logs, OCR model caches, tester personal data, or secrets.
