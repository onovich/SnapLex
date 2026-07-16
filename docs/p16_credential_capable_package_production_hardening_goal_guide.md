# P16 Credential-Capable Package Production Hardening Goal Mode Guide

Date: 2026-07-17
Status: execution guide for the P16 executor phase.
Estimated budget: 12 conversation rounds.

## 0. Direct Goal Prompt For Executor

You are the executor for SnapLex P16: Credential-Capable Package Production
Hardening. Work in `D:\ToolProjects\SnapLex`.

Use this guide as the source of truth:
`docs/p16_credential_capable_package_production_hardening_goal_guide.md`.

Goal: turn the P15 credential-capable package spike evidence into a
production-hardening decision package, while keeping the base package
deterministic and unchanged. P16 may harden scripts, docs, smoke commands,
failure messages, and release gates for the explicit `credentials` package
variant. P16 must not silently make credential support part of the base package
or promise a broad public release.

Round budget: 12 rounds total. Use rounds 1-8 for main hardening, rounds 9-11
for buffer and release hygiene, and round 12 for final validation, report, and
P17 handoff.

Every round must validate, commit, and push before moving on. Do not stage
unrelated files or ignored build outputs. Report commit hash, push result,
validation results, Debug self-check, architecture self-check, and whether a
buffer round was consumed.

## 1. Required Reading

- `Role.md`
- `README.md`
- `AGENTS.md`
- `docs/phase_plan.md`
- `docs/windows_smoke_checklist.md`
- `docs/p15_isolated_credential_package_spike_design_gate_goal_guide.md`
- `docs/p15_final_validation_report.md`
- `docs/p15_to_p16_handoff.md`
- `docs/p15_package_spike_decision.md`
- `docs/p15_packaging_spike_design.md`
- `docs/p15_packaged_keyring_import_evidence.md`
- `docs/p15_packaged_credential_smoke_evidence.md`
- `docs/p15_packaged_restart_readiness.md`
- `docs/p15_credential_cleanup_guidance.md`
- `scripts/package_windows.py`
- `packaging/snaplex.spec`
- `snaplex/credentials.py`
- `snaplex/release_smoke.py`
- `snaplex/trial_readiness.py`
- `tests/test_package_windows.py`
- `tests/test_release_smoke.py`

## 2. P16 Scope

P16 must:

- Revalidate the accepted P15 baseline.
- Preserve the deterministic base package path and prove it still excludes
  keyring support.
- Harden the explicit `credentials` package variant as a candidate package
  path, not the default.
- Improve tester-facing setup, failure, and cleanup documentation for the
  credential-capable package path.
- Polish or document failure behavior for missing, unavailable, disabled,
  locked, or unsupported keyring backends.
- Define production release gates for a credential-capable package, including
  signed build policy, package artifact handling, smoke evidence, and support
  boundaries.
- Decide whether the credential-capable package is ready for limited private
  tester distribution, needs another hardening phase, or should remain
  deferred.
- Keep automated validation deterministic and no-network.
- Run optional real-provider smoke only if existing local credentials are
  already configured and the user explicitly approves network use in that
  executor session.
- Preserve no-secret repository hygiene.

## 3. P16 Non-Scope

P16 must not implement or promise:

- silent keyring inclusion in the base package;
- raw API key persistence in app config, history, docs, logs, screenshots,
  package resources, or git;
- SnapLex Cloud, account OAuth, billing, hosted token broker, remote accounts,
  or cloud sync;
- browser extension runtime;
- AI summary runtime;
- global hotkeys;
- broad provider rewrites;
- OCR/capture rewrites;
- full localization;
- network-required automated tests;
- committed package outputs, screenshots, smoke data, local app data, keyring
  exports, `.env` files, logs, tester personal data, or provider secrets.

## 4. Architecture Boundaries

- Providers remain behind `TranslationProvider`, provider registry, and
  `TranslationPipeline`.
- Credentials remain behind `CredentialService`, credential stores,
  `SettingsService`, `SettingsPresenter`, provider setup, and trial readiness.
- Packaging may choose explicit variants and hidden imports, but must not own
  provider, credential, settings, history, OCR, capture, or UI business rules.
- UI code must not store, echo, serialize, or make policy decisions about raw
  credential values.
- Base package smoke remains deterministic and fake by default.
- Real-provider trial paths must fail closed when no real provider is
  configured.

## 5. Per-Round Required Workflow

Each round reply must include:

- round goal;
- completed work;
- Debug self-check;
- architecture self-check;
- validation commands and results;
- commit hash and push result;
- next round goal;
- whether a buffer round was consumed.

Progression rules:

- If validation fails, do not commit, push, or move to the next round.
- If validation passes but commit fails, do not move to the next round.
- If commit succeeds but push fails, do not move to the next round.
- After push succeeds, record the commit hash and continue.

Use the repository wrappers:

```powershell
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
C:\Users\Administrator\.codex\skills\project-git-workflow\scripts\git\CommitAndPush.cmd -Message "p16: <summary>" -Paths "<paths>"
```

## 6. Debug Self-Check

Every round must ask:

- Can the current change be explained by the smallest package, credential, or
  trial workflow fixture?
- Can failures be localized to packaging, optional dependency import, keyring
  backend, credential store, trial readiness, CLI output, docs, or smoke data?
- Are success, expected rejection, unavailable backend, locked/unsupported
  backend, cleanup, and restart states covered where relevant?
- If UI or tester-facing copy changed, is there repeatable smoke or review
  evidence?
- If package behavior changed, are base and credentials variants tested
  separately?

## 7. Architecture Self-Check

Every round must ask:

- Does the explicit package variant remain the only credential-capable package
  path?
- Does the base package remain deterministic and keyring-free?
- Do credential decisions stay behind credential services/stores and provider
  setup boundaries?
- Do provider calls stay behind provider registry and `TranslationPipeline`?
- Did the phase avoid cloud/OAuth/browser extension/AI summary/global hotkey
  scope?
- Are generated outputs, screenshots, local data, and user changes left alone?

## 8. Round Plan

Round 1: rebaseline P15 and define P16 hardening acceptance.

Round 2: base package preservation gate.

Round 3: credentials variant build and dependency gate.

Round 4: credential smoke command hardening.

Round 5: tester-facing setup and cleanup docs.

Round 6: failure-mode UX and support policy.

Round 7: release gate and artifact policy.

Round 8: production hardening decision.

Rounds 9-11: buffer hardening.

Round 12: final validation and handoff.

## 9. Required Deliverables

- `docs/p16_todo.md`
- `docs/p16_base_package_preservation_evidence.md`
- `docs/p16_credentials_variant_hardening.md`
- `docs/p16_credential_smoke_hardening.md`
- `docs/p16_tester_setup_cleanup_guide.md`
- `docs/p16_keyring_failure_modes.md`
- `docs/p16_release_gate_artifact_policy.md`
- `docs/p16_production_hardening_decision.md`
- `docs/p16_boundary_scan_evidence.md`
- `docs/p16_final_validation_report.md`
- `docs/p16_to_p17_handoff.md`

## 10. Validation Matrix

Required before final PASS:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python -m snaplex --check-real-provider` expected rejection when no real
  provider is configured.
- `python scripts\package_windows.py --dry-run --variant base`
- `python scripts\package_windows.py --dry-run --variant credentials`
- base package build or smoke evidence when feasible.
- credentials package build or smoke evidence when feasible.
- base package credential smoke expected rejection.
- credentials package `--smoke-credentials --credential-smoke-mode import`
  PASS or documented blocker.
- credentials package `--smoke-credentials --credential-smoke-mode cycle` PASS
  or documented blocker.
- credentials package restart readiness save/check-delete PASS or documented
  blocker.
- `cmd /c StartTrial.cmd --no-gui` expected rejection without real provider.
- `cmd /c StartFakeTrial.cmd --no-gui`
- `cmd /c SmokeTrial.cmd`
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`
- `cmd /c StartPackagedTrial.cmd --no-gui` expected rejection without real
  provider.
- `python scripts\p9_gui_smoke.py`
- `python scripts\p11_visible_gui_smoke.py`
- P16 docs link/index check.
- artifact boundary scan.
- secret pattern scan.

If a package build, keyring backend, or real-provider smoke cannot run in the
executor environment, record the blocker in the final report and decide whether
remaining evidence is enough.

## 11. PASS Criteria

P16 is PASS only if:

- P15 baseline remains intact.
- Base package remains deterministic and keyring-free.
- Credentials variant behavior is explicit, documented, and validated or has a
  precise blocker.
- Credential smoke commands do not print raw values.
- Tester-facing setup/failure/cleanup docs are clear enough for private trial
  use.
- Release gate and artifact policy are explicit.
- Production hardening decision is recorded.
- No forbidden scope enters P16.
- No secrets, local app data, screenshots, package outputs, smoke data, logs,
  OCR caches, keyring exports, or tester personal data are committed.
- Full validation matrix passes or has documented, acceptable blockers.
- Final report and P17 handoff exist.
- Worktree is clean and final commit is pushed to `origin/main`.

## 12. Final Report Template

```markdown
# P16 Final Validation Report

Date:
Phase: P16 Credential-Capable Package Production Hardening
Status: PASS / FAIL / BLOCKED
Final commit:
Push:
Rounds used:
Buffer consumed:

## Main Deliverables

## Base Package Preservation

## Credentials Variant Hardening

## Credential Smoke And Restart Evidence

## Tester-Facing Setup And Cleanup

## Keyring Failure Modes

## Release Gate And Artifact Policy

## Production Hardening Decision

## Validation Commands And Results

## Boundary And Secret Scan

## Known Limitations

## Recommended Next Phase
```
