# P15 TODO

Date: 2026-07-16
Phase: P15 Isolated Credential-Capable Package Spike Design Gate
Guide: `docs/p15_isolated_credential_package_spike_design_gate_goal_guide.md`
Status: ready for executor.
Estimated budget: 12 conversation rounds.

## Tasks

- [x] Revalidate the accepted P14 baseline.
- [x] Create package spike design notes.
- [x] Audit optional dependency and packaging variant behavior.
- [x] Prove or reject packaged keyring import/backend discovery.
- [x] Prove or reject packaged credential save/read/delete/cleanup with only a
      throwaway fake value.
- [x] Prove or reject packaged restart readiness without displaying or printing
      the fake value.
- [ ] Preserve deterministic base package dry-run and fake package smoke.
- [ ] Document cleanup guidance for throwaway/manual credentials and local
      smoke data.
- [ ] Decide whether to promote, defer, or reject a later production
      credential-capable package hardening phase.
- [ ] Preserve no-secret, no-network automated validation and fail-closed real
      trial behavior.
- [ ] Produce P15 boundary scan evidence.
- [ ] Produce P15 final validation report.
- [ ] Produce P15 to P16 handoff.

## Deferred Outside P15

- Production SnapLex Cloud, account OAuth, billing, hosted token broker, remote
  accounts, or cloud sync.
- Raw API-key persistence in app config.
- Production browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to credential-package spike evidence.
- OCR/capture rewrites.
- Full localization implementation.
- Real network validation in automated tests.
- Committed screenshots, package outputs, local app data, `.env`, keyring
  exports, logs, OCR caches, smoke data, tester personal data, or provider
  secrets.
