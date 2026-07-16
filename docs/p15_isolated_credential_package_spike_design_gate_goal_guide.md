# P15 Isolated Credential-Capable Package Spike Design Gate Goal Mode Guide

Date: 2026-07-16
Status: execution guide for P15 after planner-accepted P14
Estimated budget: 12 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P15 in goal mode:

```text
Execute SnapLex P15 - Isolated Credential-Capable Package Spike Design Gate in
12 conversation rounds.

Required reading before changes:
- AGENTS.md
- Role.md
- README.md
- TRY.md
- .env.example
- pyproject.toml
- docs/development_plan.md
- docs/phase_plan.md
- docs/p14_manual_environment_source_keyring_validation_goal_guide.md
- docs/p14_final_validation_report.md
- docs/p14_to_p15_handoff.md
- docs/p14_source_keyring_smoke_evidence.md
- docs/p14_credential_package_spike_decision.md
- docs/p14_boundary_scan_evidence.md
- docs/p15_todo.md
- docs/windows_smoke_checklist.md
- packaging/README.md
- packaging/snaplex.spec
- scripts/package_windows.py
- RequireRealProvider.cmd
- StartTrial.cmd
- StartFakeTrial.cmd
- StartPackagedTrial.cmd
- StartPackagedFakeTrial.cmd
- SmokeTrial.cmd
- snaplex/credentials.py
- snaplex/trial_readiness.py
- tests/test_credentials.py
- tests/test_package_windows.py
- tests/test_release_smoke.py
- tests/test_trial_readiness.py

P14 is planner-accepted. Source checkout keyring smoke passed through
CredentialService and KeyringCredentialStore with a throwaway fake value on
Windows WinVaultKeyring. P14 recommended a later isolated credential-capable
package spike, but did not implement or promise packaged keyring support.

Goal:
Run a narrow design-gated package spike for credential-capable packaging while
preserving the deterministic base package path. Prove, reject, or defer an
explicit credential-capable package variant by testing packaged keyring import
and backend discovery, packaged save/read/delete with throwaway fake values,
packaged restart readiness, cleanup guidance, and no-secret/no-network hygiene.

Round budget:
- Rounds 1-8: main package spike investigation and evidence.
- Rounds 9-11: buffer fixes for accepted package, docs, smoke, or hygiene gaps.
- Round 12: final validation, report, and P16 handoff.

Rules:
- P15 is an isolated spike/design gate, not a production release promise.
- The deterministic base package path must remain unchanged and green.
- Credential-capable packaging must be explicit: use a variant, spike script,
  or documented manual build path. Do not silently add keyring to the base
  package.
- Use only throwaway fake credential values.
- Do not store, print, log, screenshot, package, or commit raw credential
  values, keyring exports, `.env` files, local config/history, package outputs,
  smoke data, or tester personal data.
- Do not run real-provider network smoke unless local credentials already exist
  and a human explicitly approves network use in that round.
- Do not implement SnapLex Cloud, account OAuth, billing, hosted token broker,
  browser extension runtime, AI summary runtime, global hotkeys, broad
  provider/OCR/capture rewrites, or full localization.
- Every round must include Debug self-check, architecture self-check,
  validation commands and results, commit hash, push result, next-round target,
  and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to
  the next round.
```

## 1. Required Context

P14 accepted baseline:

- P14 final commit: `1f7c3e388e01fb4514f8d08b8d3978feb14727e3`.
- P14 validation passed with 255 tests and deterministic no-network smoke.
- Source keyring save/read/delete/cleanup passed with a throwaway fake value on
  Windows WinVaultKeyring.
- Packaged keyring behavior is not implemented, tested, shipped, or promised.
- Base package fake smoke and real-trial fail-closed behavior remain stable.

P15 planning decision:

- P15 may prototype an explicit credential-capable package path, but it must
  keep the base package deterministic and unchanged.
- The output of P15 is a go/defer/reject decision plus evidence. A successful
  spike can recommend a later production hardening phase, but must not present
  itself as a shipped release path unless the evidence and docs say so.

## 2. Scope

P15 must complete:

- Revalidate the accepted P14 baseline.
- Audit current packaging variant behavior and optional dependency inclusion.
- Design the credential-capable package spike boundary.
- Prove or reject packaged import discovery for `keyring` and the Windows
  backend.
- Prove or reject packaged credential save/read/delete/cleanup with a throwaway
  fake value.
- Prove or reject packaged restart readiness without displaying or printing the
  fake value.
- Preserve source fake, packaged fake, package dry-run, and real-trial
  fail-closed behavior.
- Produce cleanup guidance for local throwaway/manual packaged credentials.
- Decide whether credential-capable packaging should be promoted to a later
  production hardening phase, deferred, or rejected.
- Create preferred P15 docs:
  - `docs/p15_packaging_spike_design.md`
  - `docs/p15_packaged_keyring_import_evidence.md`
  - `docs/p15_packaged_credential_smoke_evidence.md`
  - `docs/p15_packaged_restart_readiness.md`
  - `docs/p15_credential_cleanup_guidance.md`
  - `docs/p15_package_spike_decision.md`
  - `docs/p15_boundary_scan_evidence.md`
  - `docs/p15_final_validation_report.md`
  - `docs/p15_to_p16_handoff.md`
- Update README, phase plan, development plan, smoke checklist, TODO, and
  planning entry points.

## 3. Non-Scope

Do not implement in P15:

- Silent keyring inclusion in the base package.
- Production SnapLex Cloud.
- Production account OAuth, billing, hosted token broker, remote accounts, or
  cloud sync.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to credential-package spike evidence.
- OCR/capture rewrites.
- Full localization implementation.
- Automated tests that require real provider credentials or network calls.
- Collection or storage of real tester personal data inside the repo.
- Committed screenshots, package outputs, local app data, `.env`, provider
  secrets, keyring exports, logs, OCR model caches, or smoke data.

## 4. Architecture Boundaries

- Providers remain behind `TranslationProvider`, provider registry, and
  `TranslationPipeline`.
- Credential behavior remains behind `CredentialService`, credential stores,
  SettingsService/SettingsPresenter, provider setup, and trial readiness.
- Packaging changes must stay in packaging scripts/specs or explicit spike
  helpers.
- The base package path must continue to support deterministic fake smoke
  without requiring keyring, credentials, network, screen permissions, or model
  downloads.
- Any credential-capable package path must fail closed when no real provider is
  configured and must not fall back to fake for real trial commands.

## 5. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P15 Isolated Credential-Capable Package Spike Design Gate
Round goal:
Completed changes:
Debug self-check:
Architecture self-check:
Validation commands and results:
Commit hash:
Push result:
Buffer consumed:
Risks or blockers:
Next-round target:
```

Debug self-check:

- Can the current change be explained by package spike design, keyring import,
  packaged credential smoke, restart readiness, cleanup guidance, package
  decision, or boundary scan?
- Can failures be localized to package variant selection, PyInstaller spec,
  optional dependency discovery, keyring backend availability, credential
  service, trial readiness, or cleanup?
- Are pass, fail, skipped, blocked, unavailable, no-secret, and fail-closed
  states covered?
- If generated outputs were created, are they ignored and uncommitted?

Architecture self-check:

- Did P15 avoid silently changing the base package path?
- Did credential/provider/trial boundaries stay in existing services?
- Did docs avoid promising production packaged keyring support beyond spike
  evidence?
- Are package outputs, keyring state, logs, screenshots, and secrets kept out
  of git?

## 6. Round Plan

Round 1 - Rebaseline and package spike boundary:

- Revalidate P14.
- Create `docs/p15_packaging_spike_design.md`.
- Decide whether the spike uses an explicit variant, temporary spike command, or
  documented manual build path.

Round 2 - Packaging optional dependency audit:

- Inspect `pyproject.toml`, `scripts/package_windows.py`, and
  `packaging/snaplex.spec`.
- Identify what must be included for keyring and Windows backend discovery.

Round 3 - Packaged keyring import evidence:

- Create `docs/p15_packaged_keyring_import_evidence.md`.
- Build or dry-run the explicit credential-capable package path when feasible.
- Record import/backend discovery pass, fail, or blocker.

Round 4 - Packaged credential save/read/delete smoke:

- Create `docs/p15_packaged_credential_smoke_evidence.md`.
- Use only a throwaway fake value.
- Prove or reject save/read/delete/cleanup through packaged app or packaged
  helper path.

Round 5 - Packaged restart readiness:

- Create `docs/p15_packaged_restart_readiness.md`.
- Prove or reject readiness after packaged process restart without displaying or
  printing the throwaway value.

Round 6 - Base package preservation:

- Re-run base package dry-run and fake package smoke.
- Confirm base package remains deterministic and no-network.

Round 7 - Cleanup guidance:

- Create `docs/p15_credential_cleanup_guidance.md`.
- Document how to remove throwaway/manual credentials and local smoke data.

Round 8 - Spike decision:

- Create `docs/p15_package_spike_decision.md`.
- Decide promote/defer/reject for a later production hardening phase.

Rounds 9-11 - Buffer hardening:

- Fix accepted package, docs, smoke, cleanup, or hygiene issues found during
  P15.
- Repeat relevant validation after each fix.
- Keep scope narrow.

Round 12 - Final validation, report, and P16 handoff:

- Create `docs/p15_boundary_scan_evidence.md`.
- Create `docs/p15_final_validation_report.md`.
- Create `docs/p15_to_p16_handoff.md`.
- Mark `docs/p15_todo.md` complete.
- Update README, phase plan, development plan, smoke checklist, and AGENTS entry
  points to reflect P15 completion.
- Run final validation, boundary scans, commit, push, and report back to the
  planner/checker session.

## 7. Validation Matrix

Required P15 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python -m snaplex --check-real-provider` expected rejection without real
  provider setup.
- `python scripts\package_windows.py --dry-run --variant base`
- Credential-capable package spike build/dry-run command when feasible.
- `cmd /c StartTrial.cmd --no-gui` expected rejection.
- `cmd /c StartFakeTrial.cmd --no-gui`
- `cmd /c SmokeTrial.cmd`
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`
- `cmd /c StartPackagedTrial.cmd --no-gui` expected rejection.
- `python scripts\p9_gui_smoke.py`
- `python scripts\p11_visible_gui_smoke.py`
- Docs link/index check for P15 docs.
- Artifact and secret boundary scan showing no committed `build/`, `dist/`,
  packaged binaries, generated config/history, `.env`, provider keys,
  screenshots, smoke data, local app data, logs, keyring exports, OCR caches,
  tester personal data, or API response captures.

Optional manual validation:

- Packaged credential smoke with a throwaway fake value.
- Packaged restart readiness.
- Real-provider smoke only with existing local credentials and explicit human
  approval.

## 8. PASS Criteria

P15 passes when:

- The credential-capable package spike boundary is explicit.
- Base package behavior remains deterministic and unchanged.
- Packaged keyring import/backend discovery has pass/fail/blocker evidence.
- Packaged credential save/read/delete/cleanup has pass/fail/blocker evidence.
- Packaged restart readiness has pass/fail/blocker evidence.
- Cleanup guidance exists.
- The package spike decision is promote/defer/reject with evidence.
- Required validation and boundary scans pass.
- P15 final validation report and P15 to P16 handoff exist.
- Final P15 commit is pushed to `origin/main`.

## 9. Final Report Template

```text
P15 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Package spike design:
- Packaged keyring import evidence:
- Packaged credential smoke:
- Packaged restart readiness:
- Base package preservation:
- Cleanup guidance:
- Package spike decision:
- Credential/privacy handling:
- Deferred scope:
- Architecture notes:
- Artifact and secret exclusion evidence:
- Commit hashes:
- Push result:
- Request for architect/PM acceptance:
- Recommended next goal:
```
