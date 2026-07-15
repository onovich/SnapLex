# P10 Secure Credential And Account Strategy Goal Mode Guide

Date: 2026-07-15
Status: execution guide for P10 after planner-accepted P9
Estimated budget: 16 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P10 in goal mode:

```text
Execute SnapLex P10 - Secure Credential And Account Strategy in 16 conversation
rounds.

Required reading before changes:
- AGENTS.md
- Role.md
- README.md
- TRY.md
- .env.example
- pyproject.toml
- docs/development_plan.md
- docs/phase_plan.md
- docs/p9_final_validation_report.md
- docs/p9_to_p10_handoff.md
- docs/p8_provider_setup_decisions.md
- docs/p8_real_provider_trial_notes.md
- docs/p10_todo.md
- docs/p10_secure_credential_account_strategy_goal_guide.md
- docs/windows_smoke_checklist.md
- snaplex/storage/config.py
- snaplex/services/settings_service.py
- snaplex/services/provider_setup.py
- snaplex/providers/config.py
- snaplex/providers/registry.py
- snaplex/providers/openai.py
- snaplex/providers/deepl.py
- snaplex/providers/libretranslate.py
- snaplex/ui/settings_presenter.py
- snaplex/ui/app_shell.py
- tests/test_provider_setup.py
- tests/test_provider_connection.py
- tests/test_settings_service.py
- tests/test_settings_presenter.py

P9 is planner-accepted. SnapLex is now visually trial-ready, but ordinary users
still need environment variables for real providers. P10 must define and
implement the first safe credential strategy without breaking existing env-var
users or pretending consumer account OAuth already exists.

Goal:
Deliver a secure credential/account strategy and a first local secure credential
path. Introduce credential service boundaries, preserve env-var compatibility,
optionally support OS keyring storage behind lazy optional dependencies and
mocked tests, update Settings and trial readiness to use the credential
boundary, and document account/cloud/token-broker options without implementing
production OAuth, billing, or SnapLex Cloud.

Round budget:
- Rounds 1-12: main architecture and implementation.
- Rounds 13-15: buffer hardening, packaging, and security/privacy fixes.
- Round 16: final validation, report, and P11 handoff.

Rules:
- Raw provider secrets must never be stored in JSON config, history, docs, tests,
  logs, screenshots, package resources, or git.
- Config may store provider names, endpoint/model/timeouts, credential reference
  type, credential reference id, and env var names. It must not store secret
  values.
- Existing env-var based OpenAI, DeepL, and LibreTranslate behavior must keep
  working.
- Any OS keyring integration must be optional, lazy-loaded, and covered by fake
  in-memory tests. Automated validation must not require a real OS keyring.
- Provider adapters must receive credentials through a credential resolver or
  service boundary, not by teaching UI widgets to read secrets.
- Settings UI may accept a secret only for immediate handoff to the credential
  service. It must clear the field after save/test and must not echo the value.
- Test Connection must continue to use provider/service boundaries and mocked
  HTTP in automated tests.
- Account sign-in, token broker, billing, SnapLex Cloud, and production OAuth
  remain design/non-runtime work in P10 unless the architect explicitly reopens
  scope after a separate security decision.
- Every round must include Debug self-check, architecture self-check,
  validation commands and results, commit hash, push result, next-round target,
  and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to
  the next round.
```

## 1. Required Context

P9 accepted baseline:

- P9 final commit: `a2ebc99a47bc810fe3f6245f61a26a16fc6650b3`.
- P9 validation passed with 221 tests.
- P9 added UI style tokens, polished shell/result/settings/history states, and
  screenshot-backed GUI smoke.
- P8/P9 provider setup remains behind SettingsService, SettingsPresenter,
  provider registry, and provider adapters.
- Translation execution remains behind `TranslationPipeline`.
- Fake provider remains deterministic smoke/dev mode and visibly labeled fake.
- Real trial commands still reject missing real provider configuration.
- No account OAuth, SnapLex Cloud, keychain, or raw secret persistence exists
  before P10.

Authentication and credential-source reality refreshed by the planner on
2026-07-15:

- OpenAI API credentials are bearer credentials from API keys or short-lived
  workload-identity tokens; API keys are secrets and should be loaded from an
  environment variable or server-side key management:
  `https://developers.openai.com/api/reference/overview#authentication`.
- DeepL API access requires an authentication key, warns to keep keys
  confidential, and says not to use API keys in client-side code:
  `https://developers.deepl.com/docs/getting-started/auth`.
- Azure Translator supports resource keys, bearer tokens, and Microsoft Entra
  ID; tokens and keys still require resource/account setup:
  `https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/reference/authentication`.
- Windows Credential Locker is the Windows-native credential storage direction:
  `https://learn.microsoft.com/en-us/windows/apps/develop/security/credential-locker`.
- Python `keyring` provides a cross-platform API for OS keyrings including
  Windows Credential Locker, macOS Keychain, and Linux Secret Service/KWallet:
  `https://pypi.org/project/keyring/`.

Planner decision:

- P10 should implement the first local secure credential boundary and optional
  OS keyring path because it materially improves trial usability without
  requiring a backend.
- P10 should not implement a production account/OAuth/cloud flow. It should
  document and compare future account paths so the disabled `Connect account`
  affordance remains honest.

## 2. Scope

P10 must complete:

- Revalidate the accepted P9 baseline.
- Create a credential threat model and strategy decision document.
- Add a credential domain model such as `CredentialReference`,
  `CredentialStatus`, and `CredentialService`.
- Add credential store boundaries such as in-memory/test store, environment
  resolver, and optional keyring-backed store.
- Preserve existing env-var based provider configuration and migration behavior.
- Add optional `credentials` dependency group for keyring if the implementation
  uses Python `keyring`; imports must remain lazy.
- Wire provider readiness and connection testing through credential service
  boundaries without exposing secrets to UI widgets.
- Update Settings presenter and UI to show credential source/status and allow a
  local secure credential save/delete/test flow when supported.
- Update trial readiness checks so real-provider launch paths can recognize the
  new credential boundary while still rejecting missing real providers.
- Add deterministic tests with fake credential stores and mocked HTTP only.
- Add documentation for env var, OS keyring, SnapLex Cloud/token broker, and
  provider account/OAuth tradeoffs.
- Create `docs/p10_final_validation_report.md`.
- Create `docs/p10_to_p11_handoff.md`.
- Update README, phase plan, development plan, smoke checklist, TODO, and entry
  points.

Preferred P10 docs:

- `docs/p10_secure_credential_account_strategy_goal_guide.md`
- `docs/p10_todo.md`
- `docs/p10_credential_strategy_decisions.md`
- `docs/p10_secure_storage_notes.md`
- `docs/p10_account_strategy.md`
- `docs/p10_final_validation_report.md`
- `docs/p10_to_p11_handoff.md`

## 3. Non-Scope

Do not implement in P10:

- Production SnapLex Cloud.
- Production account OAuth or consumer ChatGPT/DeepL account login.
- Billing, subscriptions, user accounts, remote sync, or hosted token broker.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to credential resolution.
- OCR/capture rewrites.
- Full localization implementation.
- Real provider network validation in automated tests.
- Storing raw secrets in config/history/docs/logs/tests/screenshots/package
  resources/git.
- Committing generated screenshots, package outputs, local smoke data, `.env`,
  OCR model caches, local config/history, or keyring export artifacts.

## 4. Planner Decisions And Assumptions

- Environment variables remain a supported first-class secret boundary.
- OS keyring is the recommended local desktop path for users who want a UI-based
  setup without cloud accounts.
- P10 may add `keyring` as an optional dependency group, not a hard default
  dependency, unless packaging validation proves the base package should include
  it.
- Automated tests must use fake stores. Real Windows Credential Locker smoke is
  optional/manual only.
- The disabled `Connect account (future)` affordance stays disabled unless a
  real backend/account security design is approved in a later phase.
- P11 should be chosen after P10 based on what the strategy reveals; likely
  candidates are localization foundation, visible Windows release smoke, or
  account/token-broker prototype design.

## 5. Architecture Boundaries

Hard constraints:

- Credential rules belong in credential services/stores and provider setup
  services, not PySide6 widgets.
- Config stores credential references, never secret values.
- Provider adapters must not independently decide how to find secrets. They
  should receive credentials through provider runtime config or a credential
  resolver boundary.
- Test Connection may use a secret only via the credential service and must not
  log or display it.
- History must not record credential diagnostics that expose values.
- Packaging and no-GUI bootstrap must not require optional keyring imports.
- Existing fake provider/package smoke remains deterministic and no-network.
- Trial scripts must keep real and fake paths separate.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P10 Secure Credential And Account Strategy
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

- Can the current change be explained by credential strategy, credential
  storage, provider readiness, Test Connection, trial launch, Settings UX, or
  docs?
- Can failures be localized to credential reference parsing, credential store,
  provider resolver, settings presenter, UI wiring, mocked HTTP, packaging, or
  docs?
- Are success, missing credential, unsupported store, unavailable keyring,
  delete, rotation, fallback-to-env, fake mode, and no-GUI states covered?
- If a secret enters memory for save/test, is it cleared from UI state and
  absent from logs, reprs, screenshots, docs, tests, and config?
- If generated outputs were created, are they ignored and left uncommitted?

Architecture self-check:

- Does credential state remain behind service/store boundaries?
- Did UI avoid owning provider, credential, translation, settings, or history
  semantics?
- Did provider adapters avoid direct UI/config secret handling?
- Did P10 avoid pulling production cloud/OAuth/billing into a local credential
  phase?
- Are unrelated files, generated outputs, and user changes left alone?

## 7. Round Plan

Round 1 - Rebaseline, threat model, and source refresh:

- Revalidate P9 with the core validation matrix.
- Create `docs/p10_credential_strategy_decisions.md`.
- Record current provider authentication reality from official sources.
- Define threats: config leakage, screenshots, logs, history, package resources,
  test fixtures, generated artifacts, accidental git add, and malicious local
  process limits.
- Decide the first implementation target: env vars plus optional local OS
  keyring, with cloud/account design deferred.

Round 2 - Credential domain model:

- Add credential reference/status models and a credential service protocol.
- Include credential source types such as `environment`, `keyring`, and
  `none`/`unsupported`.
- Add in-memory/fake credential store for tests.
- Add tests proving secret values do not appear in reprs or serialized config.

Round 3 - Env credential resolver compatibility:

- Move existing env-var lookup behind the credential resolver boundary.
- Preserve existing `SNAPLEX_OPENAI_API_KEY`, `SNAPLEX_DEEPL_API_KEY`, and
  LibreTranslate env-var behavior.
- Add migration tests for older configs with only `api_key_env_var`.

Round 4 - Optional keyring adapter:

- Add optional lazy keyring-backed credential store if keyring is selected.
- Add `credentials` optional dependency group if needed.
- Handle unavailable/no-backend/keyring errors as user-facing unsupported or
  unavailable states.
- Automated tests must mock/fake the keyring API and avoid real OS keyring use.

Round 5 - Credential-aware provider setup:

- Update provider setup state to report credential source/status without
  exposing values.
- Keep fake provider smoke state separate.
- Cover OpenAI, DeepL, and LibreTranslate env/keyring/missing/unavailable cases.

Round 6 - Provider connection integration:

- Ensure Test Connection resolves credentials through the credential service.
- Keep mocked HTTP tests for all real providers.
- Verify no provider adapter logs or returns raw credential values in errors.

Round 7 - Settings presenter and service integration:

- Expose credential source, keyring availability, save/delete/test state, and
  migration-safe fields through SettingsPresenter/SettingsService.
- Keep UI-independent tests for all state transitions.

Round 8 - Settings UI secure credential controls:

- Add Settings controls for credential source selection and local secure
  credential save/delete when supported.
- Secret input must be password-style, transient, and cleared after save/test.
- Do not include secret values in accessible names, tooltips, status, screenshots,
  logs, or error messages.

Round 9 - Trial command and CLI readiness:

- Update real trial readiness so `StartTrial.cmd` and `StartPackagedTrial.cmd`
  can recognize credential resolver readiness.
- Missing real provider still rejects clearly.
- Fake trial scripts remain deterministic fake smoke.

Round 10 - Package and optional dependency boundaries:

- Recheck base package dry-run with no keyring dependency required at bootstrap.
- Decide whether packaged app includes keyring by default or documents a
  credentials variant/manual install path.
- Record packaging impact in docs.

Round 11 - Account/cloud/token-broker strategy:

- Create `docs/p10_account_strategy.md`.
- Compare env vars, OS keyring, SnapLex Cloud token broker, provider OAuth or
  enterprise identity, and self-hosted LibreTranslate.
- Keep account sign-in disabled unless a later phase approves backend scope.

Round 12 - Credential smoke and documentation:

- Create `docs/p10_secure_storage_notes.md`.
- Add deterministic credential smoke command or test path with fake store.
- Add optional manual Windows Credential Locker smoke instructions.
- Update `.env.example`, provider configuration docs, TRY docs, and smoke
  checklist where needed.

Rounds 13-15 - Buffer hardening:

- Fix security review issues, migration gaps, UI leaks, optional dependency
  problems, package dry-run regressions, or docs gaps.
- Re-run secret/artifact scans after any UI screenshot or package smoke.
- Preserve P9 UI smoke and P8 provider boundaries.

Round 16 - Final validation, report, and P11 handoff:

- Create `docs/p10_final_validation_report.md`.
- Create `docs/p10_to_p11_handoff.md`.
- Mark `docs/p10_todo.md` complete.
- Update README, phase plan, development plan, smoke checklist, and AGENTS entry
  points to reflect P10 completion.
- Run final validation, boundary scans, commit, push, and report back to the
  planner/checker session for P10 acceptance.
- Recommend P11 based on P10 outcomes and trial feedback.

## 8. Validation Matrix

Required P10 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python scripts\package_windows.py --dry-run --variant base`
- `cmd /c StartTrial.cmd --no-gui` expected rejection when no real provider or
  secure credential is configured.
- `cmd /c StartFakeTrial.cmd --no-gui`
- `cmd /c SmokeTrial.cmd`
- `python scripts\p9_gui_smoke.py`
- Credential service/store unit tests with fake stores.
- Provider setup and connection tests for env/keyring/missing/unavailable
  credential states using mocked HTTP only.
- Config serialization tests proving only credential references are stored.
- Settings presenter/UI tests proving secret input is transient and not echoed.
- Optional dependency/lazy-import test proving no-GUI and package dry-run do not
  require keyring unless the credentials extra is intentionally installed.
- Docs link/index check for P10 docs.
- Artifact and secret boundary scan showing no committed `build/`, `dist/`,
  packaged binaries, generated config/history, `.env`, provider keys,
  screenshots, smoke data, local app data, logs, keyring exports, or API
  response captures.

Optional manual validation:

- Windows Credential Locker smoke with a throwaway fake provider secret.
- Real-provider smoke only when local credentials already exist and the user
  approves using them.
- Packaged credential UI smoke if keyring packaging is intentionally included.

No P10 validation may require:

- Real provider credentials.
- Real network calls in automated tests.
- Production SnapLex Cloud or account OAuth.
- Committed screenshots, local secret stores, or packaged binaries.

## 9. PASS Criteria

P10 passes when:

- Credential strategy and account/cloud tradeoff docs exist.
- Existing env-var users continue to work.
- Credential references are modeled and stored without raw secret values.
- Optional local secure credential storage exists behind service/store
  boundaries or is explicitly deferred with a concrete blocker.
- Provider setup and Test Connection use credential boundaries and remain
  deterministic in automated tests.
- Settings can show credential readiness without displaying secrets.
- Trial commands preserve real/fake separation and recognize the accepted
  credential boundary.
- No raw secrets are committed, logged, serialized, stored in history, shown in
  screenshots, or placed in package resources.
- P9 GUI smoke, P8 provider smoke, no-GUI bootstrap, and package dry-run remain
  green.
- P10 final validation report and P10 to P11 handoff exist.
- Final P10 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P10 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Credential architecture:
- Env-var compatibility:
- Optional keyring behavior:
- Settings and trial behavior:
- Account/cloud strategy:
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
P10 to P11 handoff:
- Accepted P10 baseline:
- Credential storage behavior:
- Account/cloud decisions:
- Known credential/security gaps:
- Recommended P11 scope:
- Validation to preserve:
- Explicit non-scope:
```
