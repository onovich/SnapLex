# P8 Provider Setup Decisions

Date: 2026-07-15
Phase: P8 Provider Setup And Real Translation UX
Status: Round 1 decision record

P8 starts from the accepted P0-P7 baseline and the P8 trial-script commits. The
first product decision is to make provider setup visible and testable without
turning credentials into saved app data.

## Baseline Revalidation

Round 1 revalidated the current P8 starting point:

- `Validate.cmd`: PASS with 190 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: `SnapLex bootstrap OK (PySide6 available).`
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: expected rejection when no real provider
  is configured.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS with fake smoke mode.

## Product Decision

P8 does not need SnapLex Cloud, a backend token broker, billing, accounts, or
consumer provider OAuth to finish. The short-term provider setup UX should:

- let users choose `fake`, `libretranslate`, `openai`, or `deepl` in Settings,
- store provider names, order, target language, endpoints, model names,
  timeout, retry, and API-key environment variable names,
- never store raw API key values,
- show whether the configured env var is present in the current process,
- make fake mode visibly different from real translation,
- support `Test Connection` behind service/presenter boundaries with mocked
  tests,
- keep real trial commands separate from fake smoke commands.

## Provider Setup States

P8 uses these user-facing setup states:

- `fake_smoke`: deterministic placeholder translation for development,
  package smoke, and UI smoke; not real translation.
- `missing_credential`: a provider requires a configured env var or the env var
  is not set in the current process.
- `ready_from_environment`: the provider has enough local configuration to run
  a connection test without saving secrets.
- `endpoint_unavailable`: future connection test reached the provider boundary
  and the endpoint was unavailable.
- `test_passed`: future connection test succeeded.
- `test_failed`: future connection test failed without exposing secrets.
- `oauth_future`: account sign-in is a later SnapLex Cloud or provider-supported
  flow, not P8.

Round 1 adds the pure `snaplex.services.provider_setup` model for the first
three runtime states plus unsupported-provider handling. Round 3 will attach
connection-test results behind a service/presenter boundary.

## Provider-Specific Rules

Fake:

- Always available for deterministic smoke/dev.
- Cannot be tested as a real provider connection.
- Must say it is not real translation in user-facing copy.

LibreTranslate:

- Treat a configured endpoint as enough to run a connection test when no key env
  var is configured.
- If a key env var name is configured, require that env var to be present before
  testing.
- Present public instances as user-provided endpoints, not product
  infrastructure.

OpenAI and DeepL:

- Require an API-key env var name and a value in the current process before
  testing.
- Store only env var names in config.
- Never display or persist the secret value.

OAuth:

- `Connect account` may appear only as disabled/future-track UI copy until
  SnapLex Cloud or a provider-supported desktop-safe flow is designed.

## Architecture Decision

- Provider setup state is a service-level model, not PySide6 widget logic.
- Settings UI may render setup state and ask presenters/services to save or test
  providers.
- Translation execution remains behind `TranslationPipeline`.
- Provider readiness and future connection tests must use provider boundaries
  and mocked HTTP in automated tests.
- History must not store provider setup diagnostics that could expose secrets.

## Round 1 Audit Notes

- `SettingsPresenter` already loads and saves provider selection, provider
  order, provider endpoints, API-key env var names, timeout/retry, OpenAI model,
  DeepL model type, and history settings.
- Current Settings UI is form-based and config-file oriented. Later P8 rounds
  should make provider choices, readiness badges, env var presence, and
  connection testing first-class controls.
- `StartTrial.cmd` and `StartPackagedTrial.cmd` already call
  `RequireRealProvider.cmd`, while fake trial scripts force `SNAPLEX_PROVIDER`
  and `SNAPLEX_PROVIDER_ORDER` to `fake`.
- Result UI currently shows provider name but does not warn that `fake` is
  smoke/dev output. Round 5 or Round 6 must make that user-facing distinction
  clear.

## Round 2 Presenter Integration

Round 2 connects the pure provider setup model to Settings boundaries:

- `SettingsService.load_provider_setup_states(...)` returns supported provider
  readiness states from persisted provider configs and process environment.
- `SettingsPresenter.load_state(...)` exposes stable provider choices and
  readiness states for Settings UI rendering.
- `SettingsPresenter.apply_state(...)` continues to save provider names,
  provider order, language defaults, endpoints, API-key env var names,
  timeout/retry, OpenAI model, DeepL model type, and history preferences.
- Tests cover default fake/real readiness display, env-var-present readiness,
  missing credential display, malformed legacy config compatibility, and secret
  values staying out of repr/serialized state.

Connection testing remains out of Round 2. Round 3 will add the service and
presenter orchestration for `Test Connection` using mocked HTTP only.

## Round 3 Connection Testing

Round 3 adds `Test Connection` behavior without introducing real network
validation:

- `snaplex.services.provider_setup.test_provider_connection(...)` runs a probe
  translation through the provider registry and provider adapters.
- `SettingsService.test_provider_connection(...)` loads persisted config and
  delegates to the provider setup service.
- `SettingsPresenter.test_provider_connection(...)` exposes the action for the
  future Settings UI without calling providers directly from widgets.
- Automated tests inject mocked `HttpTransport` objects for OpenAI, DeepL, and
  LibreTranslate.
- Fake mode and missing credentials return user-facing states before any HTTP
  request is attempted.
- Timeout, network/bad endpoint, HTTP error, malformed response, unsupported
  language, and success states are covered by deterministic no-network tests.

## Round 4 Settings UI Integration

Round 4 renders the provider setup model in the PySide6 Settings dialog:

- Provider selection is now a constrained native combo box for `fake`,
  `libretranslate`, `openai`, and `deepl`.
- Readiness, provider details, and API-key env var presence are visible without
  opening `config.json`.
- `Test Connection` is exposed from Settings and delegates through
  `SettingsPresenter` / `SettingsService`; widgets do not call providers or HTTP
  transports directly.
- A disabled `Connect account (future)` affordance is present with honest copy
  that account sign-in requires a later SnapLex Cloud or provider-supported
  flow.
- Provider-specific endpoint, env var name, timeout, retry, and model fields
  remain editable and save through existing presenter/service rules.

The connection button uses saved/current Settings values and still requires the
user to have local provider credentials or endpoints configured. Automated
tests remain mocked and no-network.

## Round 5 Fake And Real Trial Guardrails

Round 5 makes fake mode visible in result state and docs:

- `TranslationResultState.provider_notice` carries a fake-mode warning from
  shared presenter state to clipboard and screen result views.
- Fake provider success states say the output is deterministic placeholder text,
  not real translation.
- Real trial docs state that `StartTrial.cmd` and `StartPackagedTrial.cmd`
  reject missing real provider configuration instead of falling back to fake.
- Fake trial docs keep `StartFakeTrial.cmd`, `StartPackagedFakeTrial.cmd`, and
  `SmokeTrial.cmd` positioned as package/UI smoke only.
- `.env.example`, provider docs, and the Windows smoke checklist now repeat the
  no-secret, fake-vs-real distinction.

## Round 6 Main Shell Visual Foundation

Round 6 applies the first Apple HIG-inspired visual foundation to the main
shell and result view:

- The first screen remains the usable translation tool, not a landing page.
- Primary clipboard/screen actions, utility actions, result content, result
  actions, and status are visually separated.
- Source and translated text use selectable, readable result areas.
- Provider identity, fake-mode warning, and errors have separate visual states.
- Styling uses restrained neutral surfaces with blue primary action, amber fake
  warning, and red error treatment.
- No new animation system, decorative marketing layout, or broad design-system
  rebuild was introduced.

Offscreen GUI smoke was run by launching the PySide6 shell with
`QT_QPA_PLATFORM=offscreen` and a timer-driven app quit.

## Round 7 Hardening

Round 7 preserves the package/no-GUI baseline and records credential
limitations:

- `SmokeTrial.cmd` passed source version/no-GUI, package dry-run, and existing
  packaged executable fake workflow smoke.
- `StartTrial.cmd --no-gui` rejected missing real-provider configuration as
  expected.
- `StartFakeTrial.cmd --no-gui` passed with fake smoke mode.
- Boundary scan was tightened to reject OpenAI-like test key placeholders.
- `docs/p8_real_provider_trial_notes.md` records real trial paths, fake smoke
  paths, manual smoke steps, and future secure credential options.
