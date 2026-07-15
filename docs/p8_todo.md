# P8 TODO

P8 goal: make real translation setup usable from Settings, separate fake smoke
from real trial behavior, and establish the first Apple HIG-inspired UI
foundation for trial users.

Status: ready for execution.

Executable guide: `docs/p8_provider_setup_real_translation_goal_guide.md`

## Tasks

- [x] Revalidate the accepted P0-P7/P6 package baseline and current trial
  scripts.
- [x] Add Settings-based provider setup state for fake, LibreTranslate, OpenAI,
  and DeepL.
- [x] Add provider readiness and connection test behavior behind
  service/presenter boundaries.
- [ ] Keep raw provider API key values out of JSON config, history, docs, tests,
  logs, package resources, and screenshots.
- [x] Make fake provider mode visibly labeled as fake smoke/dev mode.
- [x] Verify real trial launch paths do not silently fall back to fake.
- [x] Update provider setup docs, trial docs, and smoke checklist.
- [x] Apply Apple HIG-inspired visual foundation to the main shell, settings,
  and result view.
- [ ] Produce P8 final validation report.
- [ ] Produce P8 to P9 handoff.

## Deferred Outside P8

- SnapLex Cloud, account backend, token broker, billing, or remote user accounts.
- Consumer account OAuth for OpenAI, DeepL, or other providers.
- Raw API key persistence in normal app config.
- Production browser extension runtime.
- AI summary runtime implementation.
- Global hotkeys.
- Full design-system rebuild, localization implementation, or broad
  cross-platform native UI variants.
