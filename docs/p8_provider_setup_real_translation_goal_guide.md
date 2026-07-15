# P8 Provider Setup And Real Translation UX Goal Mode Guide

Date: 2026-07-15
Status: execution guide for P8 after accepted P0-P7
Estimated budget: 8 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P8 in goal mode:

```text
Execute SnapLex P8 - Provider Setup And Real Translation UX in 8 conversation
rounds.

Required reading before changes:
- AGENTS.md
- Role.md
- README.md
- TRY.md
- .env.example
- docs/development_plan.md
- docs/phase_plan.md
- docs/p0_p7_final_report.md
- docs/p7_final_validation_report.md
- docs/p7_expansion_roadmap.md
- docs/p7_to_p8_handoff.md
- docs/p8_todo.md
- docs/p8_provider_setup_real_translation_goal_guide.md
- docs/p4_provider_configuration.md
- docs/p5_privacy_and_storage.md
- docs/p6_release_checklist.md
- docs/windows_smoke_checklist.md
- docs/codex-git-workflow.md
- docs/codex-ops-workflow.md
- StartTrial.cmd
- StartFakeTrial.cmd
- StartPackagedTrial.cmd
- StartPackagedFakeTrial.cmd
- RequireRealProvider.cmd

P0-P7 is accepted and closed. User feedback shows the next bottleneck is not
general expansion polish; it is that real translation is not obvious, fake mode
looks like a broken product result, provider setup is too config-file oriented,
and the PySide6 UI feels too rough for trial use.

Goal:
Deliver the first real-provider trial UX: a Settings-based provider setup flow,
clear fake-versus-real translation status, real-provider connection testing with
mocked automated tests, no-secret persistence, updated trial commands/docs, and
an Apple HIG-inspired visual foundation for the main shell, settings, and result
states.

Default planner decision:
P8 may improve the existing PySide6 UI, settings presenter/service, trial
scripts, provider setup docs, and deterministic tests. P8 must not implement
SnapLex Cloud OAuth, a backend token broker, production account login, or raw
API key persistence in JSON config. Consumer account OAuth remains a mid-term
product track because current direct provider APIs primarily require API keys,
server-side secrets, resource tokens, or enterprise/cloud identity.

Rules:
- Preserve TranslationPipeline, provider registry, settings service, config
  store, history service, capture, OCR, and packaging boundaries.
- UI widgets render presenter state and call presenters/services; they must not
  call providers directly or own credential rules.
- Fake provider remains deterministic smoke/dev mode and must be visibly labeled
  as fake when shown to users.
- Real trial launch paths must not silently fall back to fake as if it were a
  valid user-facing translation.
- Do not store actual provider API key values in config, history, docs, tests,
  logs, package resources, or screenshots.
- Automated tests must stay deterministic and no-network. Use mocked HTTP for
  provider setup and connection checks.
- Apple-inspired means clarity, hierarchy, spacing, typography discipline,
  restrained color, accessibility, and native-control polish. Do not clone macOS
  branding or add decorative marketing layout.
- Every round must include Debug self-check, architecture self-check,
  validation commands and results, commit hash, push result, next-round target,
  and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to
  the next round.
```

## 1. Required Context

P0-P7 accepted baseline:

- `docs/p0_p7_final_report.md` closes the original track.
- `docs/p7_final_validation_report.md` accepts P7 at
  `b6f1c1347b9b4cd71773ddb746893ba10d0c886a`.
- P6 remains the Windows package baseline.
- Current trial commands exist in `TRY.md`, `StartTrial.cmd`,
  `StartPackagedTrial.cmd`, `StartFakeTrial.cmd`, and
  `StartPackagedFakeTrial.cmd`.
- The latest runtime commit before P8 planning is
  `8144ba0db68295b1550ec720b96d97df5e033ecd`, which separates real trial
  launch paths from fake smoke paths.

Accepted runtime boundaries to preserve:

- Clipboard flow:
  `ClipboardService -> TranslationPipeline -> result presenter -> optional HistoryService`.
- Screen flow:
  `RegionSelector -> CaptureService -> OcrService -> TranslationPipeline -> result presenter -> optional HistoryService`.
- Settings flow:
  `SettingsPresenter -> SettingsService -> ConfigStore`.
- History flow:
  `HistoryPresenter -> HistoryService -> HistoryStore`.
- Provider integrations remain behind `TranslationProvider`, provider registry,
  provider config, retry wrapper, and mocked HTTP tests.
- Packaging invokes `snaplex.__main__ -> snaplex.app.main` and does not own app
  business rules.
- Config/history files live in local app data or `SNAPLEX_APP_DATA_DIR`, not
  inside packaged resources.

Authentication reality checked by the planner on 2026-07-15:

- OpenAI API requests use bearer credentials from API keys or short-lived access
  tokens from workload identity federation; API keys are secrets and should be
  loaded from environment variables or server-side key management:
  `https://developers.openai.com/api/reference/overview#authentication`.
- DeepL API access requires an authentication key and warns not to use API keys
  in client-side code:
  `https://developers.deepl.com/docs/getting-started/auth`.
- Azure Translator supports subscription keys, short-lived bearer tokens, and
  Microsoft Entra ID for Azure resources:
  `https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/reference/authentication`.
- Apple design references for the UI direction:
  `https://developer.apple.com/design/human-interface-guidelines`,
  `https://developer.apple.com/design/human-interface-guidelines/typography`,
  `https://developer.apple.com/design/human-interface-guidelines/color`,
  `https://developer.apple.com/design/human-interface-guidelines/layout`,
  `https://developer.apple.com/design/human-interface-guidelines/accessibility`.

## 2. Scope

P8 must complete:

- Rebaseline the app after P0-P7 and the trial-script commits.
- Create a provider setup UX inside Settings.
- Make provider selection, provider order, target language, endpoint, API-key
  environment variable name, and provider readiness visible without editing a
  config file.
- Add presenter/service tests for provider setup state, save behavior,
  readiness, and user-facing error messages.
- Add a `Test Connection` or equivalent provider readiness action that uses the
  existing provider boundaries and mocked HTTP in automated tests.
- Keep OpenAI, DeepL, and LibreTranslate setup explicit about credential
  requirements and local/private handling.
- Keep fake provider available for smoke/dev, while making fake output clearly
  non-production in the shell and result UI.
- Update trial launch docs/scripts if needed so real trial paths require a real
  provider and fake smoke paths are separate.
- Apply an Apple HIG-inspired visual foundation to the main window, result view,
  and settings flow: clear hierarchy, native-feeling controls, consistent
  spacing, accessible labels, readable result typography, restrained color, and
  polished empty/error/loading states.
- Create `docs/p8_final_validation_report.md`.
- Create `docs/p8_to_p9_handoff.md`.
- Update README, phase plan, development plan, smoke checklist, TODO, and entry
  points as needed.

Preferred P8 docs:

- `docs/p8_provider_setup_real_translation_goal_guide.md`
- `docs/p8_todo.md`
- `docs/p7_to_p8_handoff.md`
- `docs/p8_final_validation_report.md`
- `docs/p8_to_p9_handoff.md`

## 3. Non-Scope

Do not implement in P8:

- SnapLex Cloud, account backend, token broker, billing system, or remote
  user accounts.
- Consumer ChatGPT/OpenAI account OAuth, DeepL account OAuth, or a login flow
  that implies ordinary account access to provider APIs.
- Raw API key persistence in JSON config, history, docs, tests, logs, or package
  resources.
- Browser extension runtime or browser bridge implementation.
- AI summary runtime implementation.
- New mandatory provider dependencies or new provider rewrites unless needed for
  provider setup testing.
- Azure Translator adapter unless the architect explicitly reopens scope.
- Global hotkeys.
- OCR/capture rewrites.
- Full design-system rebuild, animation system, localization implementation, or
  cross-platform native design variants. P9 should carry deeper UI/UX work.
- Committing packaged binaries, installers, `dist/`, `build/`, virtual
  environments, OCR model caches, generated config/history files, `.env`,
  screenshots, smoke data, or local user data.

## 4. Planner Decisions And Assumptions

- P8 supersedes the earlier P7 roadmap recommendation of "localization
  foundation" because manual trial feedback exposed a more urgent product gap:
  real translation setup and UI clarity.
- Short term, SnapLex should support no-config-file setup through Settings, but
  it must still respect the current provider auth reality. Storing env var names
  and detecting env var presence is acceptable; storing raw keys in normal JSON
  config is not.
- A temporary in-session secret entry can be considered only if it is not saved,
  not logged, not written to history, and covered by tests. Prefer env vars until
  a secure credential store is designed.
- A provider `Connect account` button may be displayed only as a disabled or
  future-track affordance with honest copy. It must not imply working OAuth
  unless a real provider-supported flow and backend design exist.
- LibreTranslate is the best "free or low-friction" path, but public instances
  are not reliable product infrastructure. P8 should present it as self-hosted
  or user-provided endpoint first.
- Apple-inspired styling should improve the existing desktop app rather than
  turning it into a marketing page. The first screen remains the usable tool.
- P9 should continue with broader UI/UX polish after P8 proves real translation
  setup.

## 5. Architecture Boundaries

Hard constraints:

- Settings state belongs to `SettingsService`, config models, and
  `SettingsPresenter`; UI widgets must not duplicate save rules.
- Provider setup and connection tests must call provider services or provider
  registry boundaries, not raw HTTP from UI.
- `TranslationPipeline` remains the only translation execution path for
  clipboard and screen workflows.
- Provider credentials remain environment/session/server-side only. Config can
  store provider names, endpoint URLs, API-key environment variable names,
  timeout/retry settings, model names, and target language.
- History must never store credential values or provider setup diagnostics that
  expose secrets.
- Fake provider output must be labeled as fake in user-facing states and kept as
  smoke/dev mode.
- Packaged base smoke must remain deterministic and no-network.
- Real network validation is optional manual smoke only when local credentials
  are already available.
- UI changes must preserve no-GUI bootstrap, package dry-run, and automated test
  determinism.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P8 Provider Setup And Real Translation UX
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

- Can the current change be explained by provider setup, real trial UX, fake
  smoke labeling, settings persistence, result presentation, or visual polish?
- Can failures be localized to settings, provider config, provider readiness,
  translation pipeline, trial scripts, UI presentation, validation, or package
  smoke?
- Are success, empty, missing credential, unsupported provider, endpoint
  failure, timeout, fake-mode, no-GUI, and package-smoke states covered?
- Did any optional manual real-provider smoke avoid logging secrets?
- If generated outputs were created, are they ignored and left uncommitted?

Architecture self-check:

- Did UI remain a presenter/service client rather than a provider owner?
- Did P8 avoid storing raw secrets or implying unsupported OAuth?
- Did real trial paths stay separate from fake smoke paths?
- Did existing P0-P7 capture/OCR/history/package behavior remain stable?
- Did design changes improve hierarchy/accessibility without decorative scope
  creep?
- Are unrelated files, build outputs, packaged artifacts, model caches,
  screenshots, local data, and user changes left alone?

## 7. Round Plan

Round 1 - Rebaseline, product decision doc, and provider setup model:

- Revalidate the current baseline with the core validation matrix.
- Audit current Settings, provider config, trial scripts, result UI, and docs.
- Decide the provider setup states and copy:
  `fake smoke`, `missing credential`, `ready from environment`,
  `endpoint unavailable`, `test passed`, `test failed`, and `OAuth future`.
- Add or update tests for pure provider setup state if the model already exists.
- Confirm P8 does not need SnapLex Cloud to finish.

Round 2 - Settings provider setup presenter/service:

- Add provider setup view models behind `SettingsPresenter` and
  `SettingsService`.
- Support provider selection for `fake`, `libretranslate`, `openai`, and
  `deepl`.
- Support target language and provider order updates without editing JSON by
  hand.
- Store environment variable names, endpoints, model names, timeout, and retry
  settings, not raw keys.
- Add tests for defaults, saving, malformed existing config, readiness display,
  and migration compatibility.

Round 3 - Provider readiness and connection testing:

- Add `Test Connection` orchestration behind a service/presenter boundary.
- Use mocked HTTP tests for OpenAI, DeepL, and LibreTranslate readiness.
- Cover missing credentials, bad endpoint, timeout, provider HTTP error,
  malformed response, unsupported language, and success.
- Ensure automated validation performs no real network calls.
- Ensure errors map to user-facing messages without exposing secrets.

Round 4 - Settings UI integration and no-config onboarding:

- Build the Settings provider setup UI with native PySide6 controls.
- Present provider choices, readiness badge, env var presence, base URL/model
  fields, provider order, source/target language, and connection test result.
- Add a disabled or future-track `Connect account` affordance only if copy is
  honest that account OAuth requires a later SnapLex Cloud/provider-supported
  flow.
- Include direct links or concise help text in docs, not noisy in-app essays.
- Add UI/presenter smoke or focused tests where feasible.

Round 5 - Real trial commands, fake guardrails, and docs:

- Verify `StartTrial.cmd` and `StartPackagedTrial.cmd` require a real provider.
- Verify fake-specific commands stay named and documented as fake smoke.
- Ensure result UI displays provider identity and fake-mode warning clearly.
- Update `TRY.md`, `.env.example`, `docs/p4_provider_configuration.md`, and
  `docs/windows_smoke_checklist.md` as needed.
- Add tests or command smoke for real-provider-required behavior without using
  real credentials.

Round 6 - Main shell and result visual foundation:

- Redesign the main shell hierarchy using Apple HIG-inspired principles:
  clear primary actions, restrained spacing, readable text, consistent control
  sizes, accessible contrast, keyboard focus, and polished status/result states.
- Improve result layout for source text, translated text, provider badge,
  language pair, copy/retry/close actions, loading, empty, and error states.
- Keep the first screen as the usable tool, not a landing page.
- Avoid nested cards, decorative gradients, one-note palettes, and text
  overflow.
- Validate offscreen GUI flow and visible smoke notes where possible.

Round 7 - Buffer hardening and package preservation:

- Fix edge cases from rounds 2-6.
- Recheck no-GUI bootstrap, fake package smoke, package dry-run, and local data
  paths.
- Add or update docs for secure credential future work, limitations, and manual
  real-provider smoke.
- Run artifact/secret boundary scan.
- Use this round as buffer only if earlier rounds need repair.

Round 8 - Final validation, report, and P9 handoff:

- Create `docs/p8_final_validation_report.md`.
- Create `docs/p8_to_p9_handoff.md`.
- Mark `docs/p8_todo.md` complete.
- Update README, phase plan, development plan, smoke checklist, and AGENTS entry
  points so they reflect P8 completion.
- Run final validation, boundary scans, commit, push, and report back to the
  planner/checker session for P8 acceptance.
- Recommend P9 as Apple-Inspired UI/UX Polish unless P8 exposes a more urgent
  credential/backend blocker.

## 8. Validation Matrix

Required P8 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python scripts\package_windows.py --dry-run --variant base`
- Provider setup presenter/service tests.
- Mocked HTTP tests for provider readiness and connection testing.
- Trial command smoke showing:
  - real trial path rejects missing real provider with a clear message,
  - fake trial path still runs the deterministic fake smoke bootstrap,
  - packaged fake smoke path remains deterministic when package exists.
- PySide6 offscreen GUI smoke for Settings and main result states when feasible.
- Documentation link/index check for new P8 docs.
- Boundary scan showing no committed `build/`, `dist/`, packaged binaries,
  generated local config/history, `.env`, provider keys, OCR model caches,
  screenshots, smoke data, local app data, or API response captures.

Optional manual validation, only when local credentials or endpoints already
exist:

- Source GUI real-provider clipboard smoke with OpenAI, DeepL, or
  LibreTranslate.
- Packaged GUI real-provider clipboard smoke after `BuildTrial.cmd`.
- LibreTranslate self-hosted endpoint smoke.
- Visible Settings UI smoke on Windows.

No P8 validation may require:

- Real provider credentials.
- Real network calls in automated tests.
- SnapLex Cloud or account OAuth.
- Browser extension runtime.
- Committing generated binaries, screenshots, local config/history, `.env`, or
  OCR model caches.

## 9. PASS Criteria

P8 passes when:

- Settings exposes provider setup without requiring ordinary users to edit JSON
  config by hand.
- Real provider readiness and connection testing exists behind service/presenter
  boundaries and is covered by deterministic tests.
- Fake mode is clearly labeled as fake smoke/dev mode in user-facing states.
- Real trial launch paths do not silently fall back to fake as if it were real
  translation.
- Raw provider API key values are not stored in config, history, docs, tests,
  logs, package resources, or screenshots.
- OpenAI, DeepL, and LibreTranslate setup behavior is documented honestly,
  including the current limitation that consumer account OAuth is not part of
  P8.
- Main shell, settings, and result views receive a coherent Apple HIG-inspired
  visual foundation.
- Existing clipboard, screen, settings, history, no-GUI, and package dry-run
  validations remain green.
- P8 final validation report and P8 to P9 handoff exist.
- Final P8 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P8 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Provider setup UX:
- Real trial behavior:
- Fake-mode guardrails:
- UI/UX changes:
- Credential and privacy handling:
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
P8 to P9 handoff:
- Accepted P8 baseline:
- Provider setup behavior:
- Credential limitations:
- UI/UX baseline:
- Known visual/accessibility gaps:
- Recommended P9 scope:
- Validation to preserve:
- Explicit non-scope:
```
