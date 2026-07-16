# P14 TODO

Date: 2026-07-16
Phase: P14 Manual Environment And Source Keyring Validation
Guide: `docs/p14_manual_environment_source_keyring_validation_goal_guide.md`
Status: ready for executor.
Estimated budget: 12 conversation rounds.

## Tasks

- [x] Revalidate the accepted P13 baseline.
- [x] Create a tester feedback intake log and record whether external tester
      feedback is available.
- [x] Run or document blocker for assistive-technology validation on a target
      Windows device.
- [x] Run or document blocker for DPI scaling validation.
- [x] Run or document blocker for multi-monitor validation.
- [ ] Install optional source credential support when feasible and record
      keyring dependency/backend status.
- [ ] Run source keyring save/read/delete smoke with only a throwaway fake
      value when feasible, or document the blocker.
- [ ] Record optional real-provider smoke run/skip evidence.
- [ ] Decide whether evidence justifies a later isolated credential-capable
      package spike.
- [ ] Preserve deterministic no-network tests, fake smoke, P10-P13 credential
      boundaries, fail-closed real trial paths, and no-secret repository
      hygiene.
- [ ] Produce P14 boundary scan evidence.
- [ ] Produce P14 final validation report.
- [ ] Produce P14 to P15 handoff.

## Deferred Outside P14

- Credential-capable package implementation.
- Production SnapLex Cloud, account OAuth, billing, hosted token broker, remote
  accounts, or cloud sync.
- Raw API-key persistence in app config.
- Production browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to accepted validation blockers.
- OCR/capture rewrites unrelated to accepted validation blockers.
- Full localization implementation.
- Real network validation in automated tests.
- Committed screenshots, package outputs, local app data, `.env`, keyring
  exports, logs, OCR caches, smoke data, tester personal data, or provider
  secrets.
