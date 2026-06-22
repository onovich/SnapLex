# P4 TODO

P4 goal: add real translation-provider hardening and fallback behavior while preserving the accepted clipboard and screen translation flows.

Status: implementation complete, planner-accepted.

Executable guide: `docs/p4_provider_hardening_goal_guide.md`

## Tasks

- [x] Add provider runtime config and a mocked HTTP transport boundary.
- [x] Add a LibreTranslate adapter behind `TranslationProvider`.
- [x] Add an OpenAI adapter behind explicit local credential configuration.
- [x] Add a DeepL adapter behind explicit local credential configuration.
- [x] Cover missing credential, timeout, retry, HTTP error, malformed response, unsupported language, fallback order, and fallback exhaustion states.
- [x] Keep fake provider as the deterministic default for automated validation.
- [x] Document provider environment variables, local secret handling, and optional real-provider smoke.
- [x] Create P4 final validation report and P4-to-P5 handoff.

## Deferred Until Later Phases

- Persistent settings/history UI belongs to P5.
- PyInstaller packaging belongs to P6.
- Browser extension, AI summary, and post-MVP expansion belong to P7.
- Global hotkeys remain deferred unless the architect explicitly reopens that scope.
