# P6 TODO

P6 goal: package the Windows MVP and make release validation repeatable.

Status: complete, ready for planner validation.

Executable guide: `docs/p6_packaging_release_goal_guide.md`

## Tasks

- [x] Add packaging metadata and a repeatable Windows build command.
- [x] Add a controlled PyInstaller spec or equivalent tracked packaging entry.
- [x] Update `.gitignore` deliberately if a tracked `.spec` exception is needed.
- [x] Document GUI, capture, OCR, provider, settings, and history packaging behavior.
- [x] Build and smoke the packaged app where local dependencies permit.
- [x] Smoke packaged clipboard, settings persistence, history clear, and screen flow where feasible.
- [x] Add release checklist and troubleshooting docs.
- [x] Verify generated build outputs, binaries, local data, `.env`, screenshots, and OCR model caches are not committed.
- [x] Create P6 final validation report and P6-to-P7 handoff.

## Deferred Until Later Phases

- Browser extension, AI summary, multilingual expansion, and post-MVP roadmap belong to P7.
- Global hotkeys remain deferred unless the architect explicitly reopens that scope.
- Cloud sync, accounts, keychain integration, and remote history are outside the P0-P7 MVP scope.
