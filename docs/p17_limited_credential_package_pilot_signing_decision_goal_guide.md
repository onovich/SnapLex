# P17 Limited Credential Package Pilot And Signing Decision Goal Mode Guide

Date: 2026-07-17
Status: execution guide for the P17 executor phase.
Estimated budget: 12 conversation rounds.

## 0. Direct Goal Prompt For Executor

You are the executor for SnapLex P17: Limited Credential Package Pilot And
Signing Decision. Work in `D:\ToolProjects\SnapLex`.

Use this guide as the source of truth:
`docs/p17_limited_credential_package_pilot_signing_decision_goal_guide.md`.

Goal: run a controlled, privacy-safe pilot lane for the explicit unsigned
`credentials` package candidate approved by P16, then decide whether the
credential-capable package remains a separate private-trial variant, needs
signing/installer/updater work, or should stay deferred. Preserve the
deterministic base package and all credential/provider boundaries.

Round budget: 12 rounds total. Use rounds 1-8 for pilot preparation, evidence,
and decisions; rounds 9-11 for buffer/hardening; round 12 for final validation,
report, and P18 handoff.

Every round must validate, commit, and push before moving on. Do not stage
package outputs, screenshots, smoke data, logs, `.env`, keyring exports, tester
personal data, or unrelated files.

## 1. Required Reading

- `Role.md`
- `README.md`
- `AGENTS.md`
- `docs/phase_plan.md`
- `docs/windows_smoke_checklist.md`
- `docs/p16_credential_capable_package_production_hardening_goal_guide.md`
- `docs/p16_final_validation_report.md`
- `docs/p16_to_p17_handoff.md`
- `docs/p16_production_hardening_decision.md`
- `docs/p16_release_gate_artifact_policy.md`
- `docs/p16_tester_setup_cleanup_guide.md`
- `docs/p16_keyring_failure_modes.md`
- `docs/p16_boundary_scan_evidence.md`
- `scripts/package_windows.py`
- `packaging/snaplex.spec`
- `snaplex/credentials.py`
- `snaplex/release_smoke.py`
- `tests/test_package_windows.py`
- `tests/test_release_smoke.py`

## 2. P17 Scope

P17 must:

- Revalidate the accepted P16 baseline.
- Define a controlled private tester lane for the explicit `credentials`
  package candidate.
- Build or rehearse the package candidate from a clean source commit and label
  it as unsigned/private-trial only.
- Preserve the base package lane and prove it remains deterministic and
  keyring-free.
- Run the P16 source, base, and credential gates before any pilot/share
  decision.
- Collect or honestly record absence/blockers of no-secret tester feedback.
- Record optional real-provider smoke only if local credentials already exist
  and the user explicitly approves network use in that executor session.
- Decide whether credentials stay as a separate package variant.
- Decide signing, installer, updater, artifact-transfer, retention, and support
  escalation requirements.
- Preserve no-network automated validation and no-secret repository hygiene.

## 3. P17 Non-Scope

P17 must not implement or promise:

- public release;
- signed installer or updater implementation unless explicitly authorized by a
  later phase;
- silent keyring support in the base package;
- SnapLex Cloud, account OAuth, billing, hosted token broker, remote accounts,
  or cloud sync;
- browser extension runtime;
- AI summary runtime;
- global hotkeys;
- broad provider rewrites;
- OCR/capture rewrites;
- full localization;
- network-required automated tests;
- raw provider secrets in app config, docs, tests, logs, screenshots, package
  resources, chat, or git.

## 4. Architecture Boundaries

- Providers remain behind `TranslationProvider`, provider registry, and
  `TranslationPipeline`.
- Credentials remain behind `CredentialService`, credential stores,
  `SettingsService`, `SettingsPresenter`, provider setup, and trial readiness.
- Packaging may produce explicit base/credentials lanes but must not own
  provider, credential, settings, history, OCR, capture, or UI business rules.
- Pilot docs must never ask testers to send raw credentials, `.env` files,
  keyring exports, screenshots of credential fields, logs with secrets, or API
  response captures.
- Base package smoke remains deterministic and fake by default.

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
C:\Users\Administrator\.codex\skills\project-git-workflow\scripts\git\CommitAndPush.cmd -Message "p17: <summary>" -Paths "<paths>"
```

## 6. Debug Self-Check

Every round must ask:

- Can the current result be explained by the smallest pilot, package, signing,
  artifact, or tester-feedback workflow?
- Can failures be localized to source validation, base package, credentials
  package, keyring backend, artifact transfer, tester guidance, real-provider
  approval, signing policy, or support escalation?
- Are success, expected rejection, unavailable backend, no tester feedback,
  skipped network, cleanup, and signing deferral states covered?
- If feedback is recorded, is it privacy-safe and free of secrets?
- If package behavior changed, are base and credentials lanes tested
  separately?

## 7. Architecture Self-Check

Every round must ask:

- Does the credential package remain explicit and separate from base?
- Does the base package remain deterministic and keyring-free?
- Do credential decisions stay behind credential services/stores and provider
  setup boundaries?
- Do provider calls stay behind provider registry and `TranslationPipeline`?
- Did the phase avoid cloud/OAuth/browser extension/AI summary/global hotkey
  scope?
- Are generated outputs, tester data, screenshots, logs, and local artifacts
  left untracked?

## 8. Round Plan

Round 1: rebaseline P16 and define pilot lane.

Round 2: package candidate pre-share gate.

Round 3: tester instructions and feedback intake.

Round 4: pilot feedback collection or honest blocker record.

Round 5: optional real-provider smoke decision and record.

Round 6: artifact transfer, retention, and support escalation policy.

Round 7: signing, installer, and updater requirement decision.

Round 8: credential package lane decision.

Rounds 9-11: buffer hardening.

Round 12: final validation and handoff.

## 9. Required Deliverables

- `docs/p17_todo.md`
- `docs/p17_pilot_lane_plan.md`
- `docs/p17_package_candidate_gate_evidence.md`
- `docs/p17_tester_feedback_intake.md`
- `docs/p17_real_provider_smoke_record.md`
- `docs/p17_artifact_transfer_retention_support.md`
- `docs/p17_signing_installer_updater_decision.md`
- `docs/p17_credential_package_lane_decision.md`
- `docs/p17_boundary_scan_evidence.md`
- `docs/p17_final_validation_report.md`
- `docs/p17_to_p18_handoff.md`

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
- P17 docs link/index check.
- artifact boundary scan.
- secret pattern scan.

Optional real-provider smoke is manual and requires existing local credentials
plus explicit human network approval in the executor session. If absent, record
the skip honestly.

## 11. PASS Criteria

P17 is PASS only if:

- P16 baseline remains intact.
- Base package remains deterministic and keyring-free.
- Credentials package candidate has pre-share gate evidence or a precise
  blocker.
- Tester feedback is collected safely or absence/blockers are recorded without
  fabrication.
- Real-provider smoke is run only with explicit approval or skipped honestly.
- Artifact transfer, retention, and support escalation policy is recorded.
- Signing/installer/updater decision is recorded.
- Credential package lane decision is recorded.
- No forbidden scope enters P17.
- No secrets, screenshots, package outputs, local app data, smoke data, logs,
  keyring exports, tester personal data, or provider secrets are committed.
- Final report and P18 handoff exist.
- Worktree is clean and final commit is pushed to `origin/main`.

## 12. Final Report Template

```markdown
# P17 Final Validation Report

Date:
Phase: P17 Limited Credential Package Pilot And Signing Decision
Status: PASS / FAIL / BLOCKED
Final commit:
Push:
Rounds used:
Buffer consumed:

## Main Deliverables

## Pilot Lane

## Package Candidate Gate Evidence

## Tester Feedback

## Real Provider Smoke

## Artifact Transfer, Retention, And Support

## Signing, Installer, And Updater Decision

## Credential Package Lane Decision

## Validation Commands And Results

## Boundary And Secret Scan

## Known Limitations

## Recommended Next Phase
```
