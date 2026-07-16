# P16 TODO

Date: 2026-07-17
Phase: P16 Credential-Capable Package Production Hardening
Guide: `docs/p16_credential_capable_package_production_hardening_goal_guide.md`
Status: in progress; Round 1 rebaseline complete.
Estimated budget: 12 conversation rounds.

## Tasks

- [x] Revalidate the accepted P15 baseline.
- [x] Preserve and document deterministic base package behavior.
- [x] Harden explicit `credentials` package variant behavior.
- [x] Harden `--smoke-credentials` modes, output, exit codes, and no-secret
      guarantees.
- [x] Produce tester-facing credential package setup and cleanup guide.
- [x] Document or harden keyring failure modes.
- [x] Define release gate and package artifact policy.
- [x] Decide whether credential-capable packaging is ready for limited private
      tester distribution, needs another phase, or remains deferred.
- [x] Preserve no-network automated validation and fail-closed real trial
      behavior.
- [x] Produce P16 boundary scan evidence.
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

## Round 1 Rebaseline

P16 starts from the planner-accepted P15 baseline at
`8e920c7c70155095cee92df86867535c98993220`.

Baseline commands:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`:
  PASS with ruff, format check, mypy, compileall, and 261 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS.
- `python -m snaplex --check-real-provider`: expected rejection PASS.
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `python scripts\package_windows.py --dry-run --variant credentials`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: expected rejection PASS.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS.
- `cmd /c SmokeTrial.cmd`: PASS.

## P16 Hardening Acceptance

P16 hardening is acceptable only when these gates remain true:

- base package behavior stays deterministic and keyring-free;
- `credentials` remains an explicit opt-in package variant and smoke path;
- credential smoke import, cycle, save, and check-delete modes either PASS or
  record precise environment blockers;
- credential smoke output records backend and non-secret references but never
  raw values;
- missing, unavailable, disabled, locked, unsupported, and cleanup failure
  states are either covered by deterministic tests or documented as support
  policy;
- tester setup, cleanup, and failure guidance is clear enough for a controlled
  private trial;
- release gates state signed-build, artifact, evidence, and support boundaries;
- real-provider network smoke remains optional and human-approved only;
- no generated package outputs, screenshots, local app data, `.env`, keyring
  exports, logs, OCR caches, smoke data, tester personal data, or provider
  secrets are committed.
