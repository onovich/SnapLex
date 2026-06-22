# P5 TODO

P5 goal: persist local settings and optional recent translation history while preserving the accepted clipboard, screen, and provider flows.

Status: planned, ready for executor.

Executable guide: `docs/p5_history_persistence_settings_goal_guide.md`

## Tasks

- [ ] Add file-backed config storage with defaults, malformed-file fallback, and migration hooks.
- [ ] Add settings service behavior for provider, language, provider runtime options, UI preferences, and history preferences.
- [ ] Ensure actual provider API key values are never persisted.
- [ ] Add history storage for recent translation entries with add/list/delete/clear and retention behavior.
- [ ] Add privacy-first history controls, including enabled/disabled state and clear all.
- [ ] Integrate lightweight settings controls into the PySide6 shell.
- [ ] Integrate lightweight history controls into the PySide6 shell.
- [ ] Document local data paths, stored fields, history clearing, and secret handling.
- [ ] Create P5 final validation report and P5-to-P6 handoff.

## Deferred Until Later Phases

- PyInstaller packaging belongs to P6.
- Browser extension, AI summary, and post-MVP expansion belong to P7.
- Global hotkeys remain deferred unless the architect explicitly reopens that scope.
- Cloud sync, accounts, keychain integration, and remote history are outside the P0-P7 MVP scope.
