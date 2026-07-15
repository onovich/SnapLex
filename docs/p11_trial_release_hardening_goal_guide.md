# P11 Trial Release Hardening Goal Mode Guide

Date: 2026-07-16
Status: execution guide for P11 after planner-accepted P10
Estimated budget: 12 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P11 in goal mode:

```text
Execute SnapLex P11 - Trial Release Hardening in 12 conversation rounds.

Required reading before changes:
- AGENTS.md
- Role.md
- README.md
- TRY.md
- .env.example
- pyproject.toml
- docs/development_plan.md
- docs/phase_plan.md
- docs/p10_final_validation_report.md
- docs/p10_to_p11_handoff.md
- docs/p10_credential_strategy_decisions.md
- docs/p10_secure_storage_notes.md
- docs/p10_account_strategy.md
- docs/p10_smoke_evidence.md
- docs/p11_todo.md
- docs/p11_trial_release_hardening_goal_guide.md
- docs/windows_smoke_checklist.md
- packaging/README.md
- packaging/snaplex.spec
- scripts/package_windows.py
- scripts/p9_gui_smoke.py
- RequireRealProvider.cmd
- StartTrial.cmd
- StartFakeTrial.cmd
- StartPackagedTrial.cmd
- StartPackagedFakeTrial.cmd
- SmokeTrial.cmd
- snaplex/app.py
- snaplex/credentials.py
- snaplex/trial_readiness.py
- snaplex/ui/app_shell.py
- snaplex/services/provider_setup.py
- snaplex/services/settings_service.py
- snaplex/ui/settings_presenter.py
- tests/test_trial_readiness.py
- tests/test_credentials.py
- tests/test_settings_service.py
- tests/test_provider_setup.py

P10 is planner-accepted. SnapLex now has secure credential boundaries and
optional lazy keyring support, but it still needs release-hardening evidence
before broader trial distribution.

Goal:
Harden SnapLex for a private Windows trial release by validating visible desktop
behavior, credential/keyring behavior, packaged trial behavior, and provider
onboarding clarity. Preserve P10 credential boundaries, no-secret repository
hygiene, deterministic fake smoke paths, and no-network automated tests.

Round budget:
- Rounds 1-8: main release-hardening work.
- Rounds 9-11: buffer fixes for smoke, packaging, copy, or security notes.
- Round 12: final validation, report, and P12 handoff.

Rules:
- Do not implement production SnapLex Cloud, account OAuth, billing, hosted
  token broker, browser extension runtime, AI summary runtime, global hotkeys,
  provider rewrites, OCR/capture rewrites, or full localization.
- Do not require real provider credentials, real network calls, or real OS
  keyring access in automated validation.
- Use a throwaway fake value only for manual Windows Credential Locker/keyring
  smoke. Never commit keyring exports, .env files, screenshots, local app data,
  logs, package outputs, or provider secrets.
- If visible Windows desktop smoke cannot be run in the executor environment,
  document the blocker precisely and do not claim broad trial release readiness.
- Keep base package smoke deterministic and fake-provider based unless a
  credential-capable package variant is explicitly validated.
- Provider onboarding copy may be polished, but provider/account/security
  semantics must stay behind existing service/presenter boundaries.
- Every round must include Debug self-check, architecture self-check,
  validation commands and results, commit hash, push result, next-round target,
  and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to
  the next round.
```

## 1. Required Context

P10 accepted baseline:

- P10 final commit: `5a37564993c67dcf9c5bfe5da2ed06a44327874c`.
- P10 validation passed with 255 tests.
- P10 added `CredentialReference`, `CredentialStatus`, `CredentialService`,
  environment credential compatibility, optional lazy keyring store, Settings
  credential controls, and credential-aware trial readiness.
- P10 did not run manual Windows Credential Locker smoke, real provider network
  smoke, visible Windows desktop smoke with normal fonts, or assistive
  technology checks.
- P10 kept production account/cloud/OAuth/billing/token broker out of runtime
  scope.

P11 release-hardening decision:

- The next risk is not another product feature. The next risk is whether the
  P8-P10 trial experience holds up on a visible Windows desktop and in packaged
  credential scenarios.
- P11 should collect repeatable evidence, fix small copy/packaging/smoke issues
  found by that evidence, and make an explicit credential packaging decision.
- Localization, browser extension, AI summary, global hotkeys, and cloud account
  work remain deferred.

## 2. Scope

P11 must complete:

- Revalidate the accepted P10 baseline.
- Run or explicitly document blocker for visible Windows GUI smoke covering
  shell, Settings, History, long text, focus, fake-provider warnings, and
  real/fake trial launch behavior.
- Run manual Windows Credential Locker or keyring smoke with a throwaway fake
  provider credential when the environment supports it.
- Decide and document whether packaged SnapLex includes keyring support by
  default, through a credential-capable variant, or only as a manual install
  path for this trial.
- Verify packaged source/fake trial behavior and real-trial fail-closed behavior
  after the credential packaging decision.
- Polish provider onboarding and credential setup copy where users still need
  clearer instructions.
- Add provider key-rotation and least-privilege notes.
- Preserve P10 credential, Settings, provider, and trial readiness boundaries.
- Create release-hardening docs and evidence:
  - `docs/p11_visible_windows_smoke_evidence.md`
  - `docs/p11_keyring_packaging_decision.md`
  - `docs/p11_provider_onboarding_notes.md`
  - `docs/p11_final_validation_report.md`
  - `docs/p11_to_p12_handoff.md`
- Update README, phase plan, development plan, smoke checklist, TODO, and
  planning entry points.

## 3. Non-Scope

Do not implement in P11:

- Production SnapLex Cloud.
- Production account OAuth, billing, hosted token broker, remote accounts, or
  cloud sync.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to release-hardening validation or onboarding
  copy.
- OCR/capture rewrites.
- Full localization implementation.
- Automated tests that require real provider credentials, network calls, a real
  OS keyring, model downloads, or screen permissions.
- Storing raw secrets in config, history, docs, tests, logs, screenshots,
  package resources, or git.
- Committing generated screenshots, package outputs, local app data, `.env`,
  provider secrets, keyring exports, logs, OCR model caches, or smoke data.

## 4. Planner Decisions And Assumptions

- P11 uses a 12-round budget because it is release hardening, not a broad new
  feature phase.
- Base package should remain deterministic and fake-provider safe unless P11
  proves keyring packaging is ready.
- A credential-capable package variant is acceptable to investigate, but not to
  promise unless package dry-run and manual smoke support it.
- Visible Windows smoke is the preferred evidence. Offscreen smoke is still
  useful but cannot replace normal desktop-font and focus checks for trial
  readiness.
- Real provider network smoke is optional and requires explicit user-approved
  local credentials. Do not use real credentials by default.
- P12 should be chosen after P11 based on evidence; likely candidates are
  localization foundation, public release documentation, or global hotkey
  feasibility.

## 5. Architecture Boundaries

Hard constraints:

- Credential semantics remain in credential services/stores and provider setup
  services, not PySide6 widgets.
- Config stores credential references only, never secret values.
- Provider adapters remain behind `TranslationProvider` and registry contracts.
- Translation execution remains behind `TranslationPipeline`.
- Trial scripts keep real and fake paths separate.
- Packaging decisions must not make no-GUI bootstrap or base fake smoke depend
  on optional keyring, real network, real provider credentials, OCR model
  downloads, or screen permissions.
- UI copy improvements must not duplicate provider, credential, trial, or
  settings business rules inside widgets.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P11 Trial Release Hardening
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

Progression rules:

- Validation fails: do not commit, do not push, do not move to the next round.
- Validation passes but commit fails: do not move to the next round.
- Commit succeeds but push fails: do not move to the next round.
- Push succeeds: record commit hash and remote branch, then move to the next
  round.
- Any scope expansion beyond this guide must be explicitly approved by the
  architect/PM before implementation.

Debug self-check:

- Can the current change be explained by visible smoke, keyring smoke,
  packaging, provider onboarding copy, release docs, or credential safety?
- Can failures be localized to UI runtime, desktop environment, keyring backend,
  packaging, trial script, provider readiness, settings presenter, or docs?
- Are success, missing credential, unsupported keyring, unavailable keyring,
  fake mode, real-trial fail-closed, packaged fake smoke, and no-GUI states
  covered?
- If a manual smoke artifact was produced, is it ignored and uncommitted?
- If a throwaway secret entered memory, is it absent from config, history, logs,
  screenshots, docs, tests, package resources, and git?

Architecture self-check:

- Did credential state remain behind service/store boundaries?
- Did UI avoid owning provider, credential, translation, settings, or history
  semantics?
- Did packaging avoid changing base deterministic fake smoke behavior without
  explicit evidence?
- Did P11 avoid pulling cloud/OAuth/billing/localization/global-hotkey scope into
  release hardening?
- Are unrelated files, generated outputs, and user changes left alone?

## 7. Round Plan

Round 1 - Rebaseline and release-risk audit:

- Revalidate P10 with core validation.
- Audit P10 handoff limitations, release checklist, package docs, and smoke
  checklist.
- Create or update `docs/p11_visible_windows_smoke_evidence.md` with planned
  visible smoke coverage and environment constraints.

Round 2 - Visible Windows GUI smoke:

- Run visible Windows smoke when possible for shell, Settings, History, focus,
  long text, fake warnings, and result states.
- If visible smoke is blocked, document exact blocker and preserve offscreen
  smoke as fallback evidence.
- Fix only narrow UI/copy issues found by the smoke.

Round 3 - Manual keyring smoke:

- Run Windows Credential Locker/keyring smoke with a throwaway fake credential
  when supported.
- Confirm Settings save/delete/readiness behavior and no secret echo.
- If unsupported, document exact backend/environment blocker and expected user
  fallback.

Round 4 - Packaged credential decision:

- Create `docs/p11_keyring_packaging_decision.md`.
- Decide base package versus credential-capable variant versus manual
  credentials extra for the private trial.
- Validate package dry-run and preserve deterministic base package smoke.

Round 5 - Packaged trial hardening:

- Run packaged version/no-GUI/fake smoke and real-trial fail-closed checks.
- Check whether credential-capable packaging needs extra hidden imports,
  optional dependency notes, or explicit variant docs.
- Do not commit package outputs.

Round 6 - Provider onboarding copy:

- Create `docs/p11_provider_onboarding_notes.md`.
- Polish README/TRY/Settings copy for env vars, keyring, fake mode, real trial,
  Test Connection, and missing-provider states.
- Keep copy factual; do not imply consumer OAuth/account login is implemented.

Round 7 - Key rotation and least privilege:

- Add provider key-rotation, least-privilege, and cleanup notes to relevant docs.
- Include OpenAI/DeepL/LibreTranslate self-hosted guidance without storing
  secrets or requiring network tests.
- Preserve P10 no-secret boundaries.

Round 8 - Release checklist consolidation:

- Update `docs/windows_smoke_checklist.md`, `packaging/README.md`, and README
  to reflect the P11 release-hardening path.
- Add a trial-readiness checklist for private testers.

Rounds 9-11 - Buffer hardening:

- Fix issues found by visible smoke, keyring smoke, package dry-run, docs
  review, or secret/artifact scans.
- Repeat relevant smoke after each fix.
- Keep scope narrow.

Round 12 - Final validation, report, and P12 handoff:

- Create `docs/p11_final_validation_report.md`.
- Create `docs/p11_to_p12_handoff.md`.
- Mark `docs/p11_todo.md` complete.
- Update README, phase plan, development plan, smoke checklist, and AGENTS entry
  points to reflect P11 completion.
- Run final validation, boundary scans, commit, push, and report back to the
  planner/checker session for P11 acceptance.
- Recommend P12 based on trial-hardening evidence.

## 8. Validation Matrix

Required P11 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python -m snaplex --check-real-provider` expected rejection without real
  provider setup.
- `python scripts\package_windows.py --dry-run --variant base`
- `cmd /c StartTrial.cmd --no-gui` expected rejection without real provider
  setup.
- `cmd /c StartFakeTrial.cmd --no-gui`
- `cmd /c SmokeTrial.cmd`
- `python scripts\p9_gui_smoke.py`
- Visible Windows GUI smoke if environment allows it.
- Manual Windows Credential Locker/keyring smoke with a throwaway fake secret if
  environment allows it.
- Packaged executable version/no-GUI/fake workflow smoke when a local package is
  built or already exists.
- Docs link/index check for P11 docs.
- Artifact and secret boundary scan showing no committed `build/`, `dist/`,
  packaged binaries, generated config/history, `.env`, provider keys,
  screenshots, smoke data, local app data, logs, keyring exports, OCR model
  caches, or API response captures.

Optional manual validation:

- Real-provider network smoke only when local credentials already exist and the
  user approves using them.
- Assistive technology checks.
- DPI and multi-monitor visible smoke.

No P11 validation may require:

- Real provider credentials by default.
- Real network calls in automated tests.
- Production SnapLex Cloud or account OAuth.
- Committed screenshots, local secret stores, package outputs, or packaged
  binaries.

## 9. PASS Criteria

P11 passes when:

- P10 credential boundaries remain intact.
- Visible Windows smoke is passed or its blocker is explicitly documented and
  release readiness is scoped accordingly.
- Manual keyring smoke is passed with a throwaway key or its blocker is
  explicitly documented.
- A packaged keyring/credential support decision exists.
- Provider onboarding, key rotation, least privilege, and trial setup docs are
  clearer and accurate.
- Real/fake trial separation remains fail-closed and deterministic.
- Base package dry-run and fake package smoke remain green.
- No raw secrets are committed, logged, serialized, stored in history, shown in
  screenshots, or placed in package resources.
- P11 final validation report and P11 to P12 handoff exist.
- Final P11 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P11 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Visible Windows smoke:
- Keyring/Credential Locker smoke:
- Packaging decision:
- Provider onboarding changes:
- Key rotation / least privilege notes:
- Credential/privacy handling:
- Deferred scope:
- Architecture notes:
- Manual smoke evidence:
- Artifact and secret exclusion evidence:
- Commit hashes:
- Push result:
- Request for architect/PM acceptance:
- Recommended next goal:
```

```text
P11 to P12 handoff:
- Accepted P11 baseline:
- Release-hardening evidence:
- Keyring and packaging decision:
- Known release/security gaps:
- Recommended P12 scope:
- Validation to preserve:
- Explicit non-scope:
```
