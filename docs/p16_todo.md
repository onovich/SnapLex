# P16 TODO

Date: 2026-07-17
Phase: P16 Credential-Capable Package Production Hardening
Guide: `docs/p16_credential_capable_package_production_hardening_goal_guide.md`
Status: ready for executor.
Estimated budget: 12 conversation rounds.

## Tasks

- [ ] Revalidate the accepted P15 baseline.
- [ ] Preserve and document deterministic base package behavior.
- [ ] Harden explicit `credentials` package variant behavior.
- [ ] Harden `--smoke-credentials` modes, output, exit codes, and no-secret
      guarantees.
- [ ] Produce tester-facing credential package setup and cleanup guide.
- [ ] Document or harden keyring failure modes.
- [ ] Define release gate and package artifact policy.
- [ ] Decide whether credential-capable packaging is ready for limited private
      tester distribution, needs another phase, or remains deferred.
- [ ] Preserve no-network automated validation and fail-closed real trial
      behavior.
- [ ] Produce P16 boundary scan evidence.
- [ ] Produce P16 final validation report.
- [ ] Produce P16 to P17 handoff.

## Deferred Outside P16

- Silent keyring support in the base package.
- Production SnapLex Cloud, account OAuth, billing, hosted token broker, remote
  accounts, or cloud sync.
- Raw API-key persistence in app config.
- Production browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Broad provider rewrites unrelated to credential-capable package hardening.
- OCR/capture rewrites.
- Full localization implementation.
- Network-required automated tests.
- Committed screenshots, package outputs, local app data, `.env`, keyring
  exports, logs, OCR caches, smoke data, tester personal data, or provider
  secrets.
