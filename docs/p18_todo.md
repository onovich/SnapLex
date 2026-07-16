# P18 TODO

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Guide: `docs/p18_signing_distribution_readiness_gate_goal_guide.md`
Status: ready for executor.
Estimated budget: 12 conversation rounds.

## Tasks

- [x] Revalidate the accepted P17 baseline.
- [x] Define signing identity and certificate custody policy.
- [x] Define signing command, verification, and revocation expectations.
- [x] Run or explicitly skip/block a safe signing rehearsal.
- [x] Decide archive versus installer readiness.
- [x] Define rollback and update policy without implementing updater runtime.
- [x] Define artifact naming, transfer, retention, revocation, and support
      escalation policy.
- [ ] Decide distribution readiness.
- [ ] Preserve deterministic base package validation.
- [ ] Preserve explicit credentials package validation.
- [ ] Produce P18 boundary scan evidence.
- [ ] Produce P18 final validation report.
- [ ] Produce P18 to P19 handoff.

## Deferred Outside P18

- Public release.
- Production signing with a real certificate unless separately authorized.
- Committed certificates, private keys, signed binaries, package outputs, or
  verification screenshots.
- Installer/updater runtime implementation.
- Silent keyring support in the base package.
- Production SnapLex Cloud, account OAuth, billing, hosted token broker, remote
  accounts, or cloud sync.
- Production browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Broad provider rewrites.
- OCR/capture rewrites.
- Full localization implementation.
- Network-required automated tests.
