# P6 TODO

P6 goal: package the Windows MVP and make release validation repeatable.

Status: planned, ready for executor.

Executable guide: `docs/p6_packaging_release_goal_guide.md`

## Tasks

- [ ] Add packaging metadata and a repeatable Windows build command.
- [ ] Add a controlled PyInstaller spec or equivalent tracked packaging entry.
- [ ] Update `.gitignore` deliberately if a tracked `.spec` exception is needed.
- [ ] Document GUI, capture, OCR, provider, settings, and history packaging behavior.
- [ ] Build and smoke the packaged app where local dependencies permit.
- [ ] Smoke packaged clipboard, settings persistence, history clear, and screen flow where feasible.
- [ ] Add release checklist and troubleshooting docs.
- [ ] Verify generated build outputs, binaries, local data, `.env`, screenshots, and OCR model caches are not committed.
- [ ] Create P6 final validation report and P6-to-P7 handoff.

## Deferred Until Later Phases

- Browser extension, AI summary, multilingual expansion, and post-MVP roadmap belong to P7.
- Global hotkeys remain deferred unless the architect explicitly reopens that scope.
- Cloud sync, accounts, keychain integration, and remote history are outside the P0-P7 MVP scope.
