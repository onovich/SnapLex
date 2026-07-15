# P7 to P8 Handoff

Date: 2026-07-15
Status: P0-P7 accepted; P8 ready for execution planning

Recommended next phase: P8 Provider Setup And Real Translation UX

Executable P8 guide: `docs/p8_provider_setup_real_translation_goal_guide.md`

## Why P8 Supersedes The Earlier Roadmap Pick

P7 recommended localization foundation as the lowest-risk first post-MVP goal.
After trial feedback, the higher-priority product blocker is clearer:

- The app can show fake output such as `Pluck [en]`, which looks like broken
  translation to users.
- Real translation setup still feels like environment/config work rather than a
  product flow.
- Trial commands now separate real and fake launch paths, but the UI still needs
  to make that distinction obvious.
- The PySide6 shell is functional but visually rough for broader trial use.

P8 therefore focuses on real-provider setup and first-pass UI polish while
preserving the accepted P6 Windows release baseline.

## Baseline Available To P8

- `TranslationPipeline` already supports fake, LibreTranslate, OpenAI, and DeepL
  through provider contracts.
- `SettingsService`, `SettingsPresenter`, and config storage already persist
  provider names, provider order, endpoint/model settings, and API-key
  environment variable names.
- Actual API key values are not stored by the app.
- `StartTrial.cmd` and `StartPackagedTrial.cmd` require real providers.
- `StartFakeTrial.cmd` and `StartPackagedFakeTrial.cmd` remain deterministic
  fake smoke paths.
- P6 package dry-run and fake package smoke remain the release baseline.

## Guardrails For P8

- Do not implement SnapLex Cloud or account OAuth.
- Do not store raw provider API keys in JSON config or docs.
- Do not move provider rules into UI widgets.
- Do not let real trial commands silently fall back to fake.
- Do not add real network calls to automated validation.
- Keep generated packages, screenshots, local smoke data, OCR model caches,
  `.env`, provider secrets, and user config/history files uncommitted.

## Recommended P8 First Steps

1. Read `docs/p8_provider_setup_real_translation_goal_guide.md`.
2. Revalidate the current baseline with `Validate.cmd`, no-GUI bootstrap, and
   package dry-run.
3. Audit Settings, provider config, trial scripts, and result states before
   editing UI.
4. Implement provider setup state at service/presenter boundaries before PySide6
   widget changes.
5. Keep fake smoke and real translation trial states visually distinct.
