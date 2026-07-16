# P18 Signing And Distribution Readiness Gate Goal Mode Guide

Date: 2026-07-17
Status: execution guide for the P18 executor phase.
Estimated budget: 12 conversation rounds.

## 0. Direct Goal Prompt For Executor

You are the executor for SnapLex P18: Signing And Distribution Readiness Gate.
Work in `D:\ToolProjects\SnapLex`.

Use this guide as the source of truth:
`docs/p18_signing_distribution_readiness_gate_goal_guide.md`.

Goal: decide whether SnapLex is ready to move from an unsigned private-trial
credential package lane toward signed distribution. Define signing identity,
certificate custody, artifact verification, archive-versus-installer policy,
rollback/update expectations, and support escalation. Optionally run a local
signing rehearsal only if the environment already has a safe throwaway or test
signing path; do not require or invent a real code-signing certificate.

Round budget: 12 rounds total. Use rounds 1-8 for readiness policy, rehearsal
evidence, and decisions; rounds 9-11 for buffer/hardening; round 12 for final
validation, report, and P19 handoff.

Every round must validate, commit, and push before moving on. Do not stage
package outputs, signed artifacts, certificates, private keys, screenshots,
smoke data, logs, `.env`, keyring exports, tester personal data, or unrelated
files.

## 1. Required Reading

- `Role.md`
- `README.md`
- `AGENTS.md`
- `docs/phase_plan.md`
- `docs/windows_smoke_checklist.md`
- `docs/p17_limited_credential_package_pilot_signing_decision_goal_guide.md`
- `docs/p17_final_validation_report.md`
- `docs/p17_to_p18_handoff.md`
- `docs/p17_signing_installer_updater_decision.md`
- `docs/p17_credential_package_lane_decision.md`
- `docs/p17_artifact_transfer_retention_support.md`
- `docs/p17_package_candidate_gate_evidence.md`
- `scripts/package_windows.py`
- `packaging/snaplex.spec`
- `snaplex/release_smoke.py`
- `tests/test_package_windows.py`
- `tests/test_release_smoke.py`

## 2. P18 Scope

P18 must:

- Revalidate the accepted P17 baseline.
- Define signing identity and certificate custody requirements.
- Define signing command, verification evidence, and revocation expectations.
- Decide archive versus installer readiness and what remains blocked.
- Define rollback/update expectations without adding updater runtime.
- Define signed artifact naming, transfer, retention, and support escalation.
- Optionally run a local signing rehearsal only with a safe throwaway/test
  signing path and no private keys committed.
- Preserve deterministic base package validation.
- Preserve explicit `credentials` package lane validation.
- Keep real-provider smoke optional and human-approved only.
- Preserve no-secret/no-artifact repository hygiene.

## 3. P18 Non-Scope

P18 must not implement or promise:

- public release;
- production signing with a real certificate unless separately authorized and
  already available through safe local tooling;
- committed certificates, private keys, signed binaries, package outputs, or
  verification screenshots;
- installer/updater runtime implementation;
- silent keyring support in the base package;
- SnapLex Cloud, account OAuth, billing, hosted token broker, remote accounts,
  or cloud sync;
- browser extension runtime;
- AI summary runtime;
- global hotkeys;
- broad provider rewrites;
- OCR/capture rewrites;
- full localization;
- network-required automated tests.

## 4. Architecture Boundaries

- Providers remain behind `TranslationProvider`, provider registry, and
  `TranslationPipeline`.
- Credentials remain behind `CredentialService`, credential stores,
  `SettingsService`, `SettingsPresenter`, provider setup, and trial readiness.
- Packaging/signing may wrap explicit artifacts but must not own provider,
  credential, settings, history, OCR, capture, or UI business rules.
- Base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial until a later
  release gate approves broader distribution.

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
C:\Users\Administrator\.codex\skills\project-git-workflow\scripts\git\CommitAndPush.cmd -Message "p18: <summary>" -Paths "<paths>"
```

## 6. Debug Self-Check

Every round must ask:

- Can the current result be explained by the smallest signing, package,
  artifact, verification, rollback, or support workflow?
- Can failures be localized to source validation, base lane, credentials lane,
  signing identity, certificate custody, signing command, verification,
  artifact transfer, installer policy, updater policy, or support escalation?
- Are success, expected rejection, no certificate, skipped signing rehearsal,
  skipped network, cleanup, revocation, rollback, and no-secret states covered?
- If signing rehearsal is run, is it clearly throwaway/test-only and free of
  committed keys or signed artifacts?

## 7. Architecture Self-Check

Every round must ask:

- Does signing/distribution policy leave base deterministic and keyring-free?
- Does credential packaging remain explicit and separate from base?
- Do credential decisions stay behind credential services/stores and provider
  setup boundaries?
- Do provider calls stay behind provider registry and `TranslationPipeline`?
- Did the phase avoid cloud/OAuth/browser extension/AI summary/global hotkey
  scope?
- Are generated outputs, signed artifacts, keys, screenshots, logs, and tester
  data left untracked?

## 8. Round Plan

Round 1: rebaseline P17 and define signing readiness questions.

Round 2: signing identity and certificate custody policy.

Round 3: signing command and verification evidence policy.

Round 4: optional signing rehearsal decision and record.

Round 5: archive-versus-installer readiness decision.

Round 6: rollback/update expectations and non-implementation policy.

Round 7: artifact naming, transfer, retention, revocation, and support
escalation.

Round 8: distribution readiness decision.

Rounds 9-11: buffer hardening.

Round 12: final validation and handoff.

## 9. Required Deliverables

- `docs/p18_todo.md`
- `docs/p18_signing_identity_certificate_custody.md`
- `docs/p18_signing_verification_policy.md`
- `docs/p18_signing_rehearsal_record.md`
- `docs/p18_archive_installer_readiness_decision.md`
- `docs/p18_rollback_update_policy.md`
- `docs/p18_artifact_retention_revocation_support.md`
- `docs/p18_distribution_readiness_decision.md`
- `docs/p18_boundary_scan_evidence.md`
- `docs/p18_final_validation_report.md`
- `docs/p18_to_p19_handoff.md`

## 10. Validation Matrix

Required before final PASS:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python -m snaplex --check-real-provider` expected rejection without real
  provider setup.
- `python scripts\package_windows.py --dry-run --variant base`
- `python scripts\package_windows.py --dry-run --variant credentials`
- base package build or smoke evidence when feasible.
- credentials package build or smoke evidence when feasible.
- base package credential smoke expected rejection.
- credentials package import/cycle/save/check-delete PASS or documented
  blocker.
- `cmd /c StartTrial.cmd --no-gui` expected rejection without real provider.
- `cmd /c StartFakeTrial.cmd --no-gui`
- `cmd /c SmokeTrial.cmd`
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`
- `cmd /c StartPackagedTrial.cmd --no-gui` expected rejection without real
  provider.
- `python scripts\p9_gui_smoke.py`
- `python scripts\p11_visible_gui_smoke.py`
- P18 docs link/index check.
- artifact boundary scan.
- secret/private-key/signing-material scan.

Optional signing rehearsal must be documented as PASS, SKIPPED, or BLOCKED.
Do not mark P18 FAIL solely because no real certificate exists; P18 is a
readiness gate unless the phase itself introduces a broken signing path.

## 11. PASS Criteria

P18 is PASS only if:

- P17 baseline remains intact.
- Signing identity and certificate custody policy is recorded.
- Signing verification and revocation expectations are recorded.
- Optional signing rehearsal is run safely or skipped with clear reason.
- Archive-versus-installer readiness decision is recorded.
- Rollback/update expectations are recorded without adding updater runtime.
- Artifact retention/revocation/support policy is recorded.
- Distribution readiness decision is recorded.
- Base package remains deterministic and keyring-free.
- Credentials package remains explicit and private-trial unless a later gate
  approves otherwise.
- No forbidden scope enters P18.
- No private keys, certificates, signed artifacts, package outputs,
  screenshots, local app data, logs, keyring exports, tester personal data, or
  provider secrets are committed.
- Final report and P19 handoff exist.
- Worktree is clean and final commit is pushed to `origin/main`.

## 12. Final Report Template

```markdown
# P18 Final Validation Report

Date:
Phase: P18 Signing And Distribution Readiness Gate
Status: PASS / FAIL / BLOCKED
Final commit:
Push:
Rounds used:
Buffer consumed:

## Main Deliverables

## Signing Identity And Certificate Custody

## Signing Verification

## Signing Rehearsal

## Archive Versus Installer

## Rollback And Update Policy

## Artifact Retention, Revocation, And Support

## Distribution Readiness Decision

## Validation Commands And Results

## Boundary And Secret Scan

## Known Limitations

## Recommended Next Phase
```
