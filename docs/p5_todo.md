# P5 TODO

P5 goal: persist local settings and optional recent translation history while preserving the accepted clipboard, screen, and provider flows.

Status: implementation complete, planner-accepted.

Executable guide: `docs/p5_history_persistence_settings_goal_guide.md`

## Tasks

- [x] Add file-backed config storage with defaults, malformed-file fallback, and migration hooks.
- [x] Add settings service behavior for provider, language, provider runtime options, UI preferences, and history preferences.
- [x] Ensure actual provider API key values are never persisted.
- [x] Add history storage for recent translation entries with add/list/delete/clear and retention behavior.
- [x] Add privacy-first history controls, including enabled/disabled state and clear all.
- [x] Integrate lightweight settings controls into the PySide6 shell.
- [x] Integrate lightweight history controls into the PySide6 shell.
- [x] Document local data paths, stored fields, history clearing, and secret handling.
- [x] Create P5 final validation report and P5-to-P6 handoff.

## Deferred Until Later Phases

- PyInstaller packaging belongs to P6.
- Browser extension, AI summary, and post-MVP expansion belong to P7.
- Global hotkeys remain deferred unless the architect explicitly reopens that scope.
- Cloud sync, accounts, keychain integration, and remote history are outside the P0-P7 MVP scope.
