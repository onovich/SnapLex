# P2 Hotkey Decision

Date: 2026-06-22
Phase: P2 Clipboard Translation MVP
Status: global hotkey deferred

## Decision

P2 keeps the manual `Translate Clipboard` action as the accepted trigger path and
defers global hotkey support to a later phase.

## Investigation Notes

- PySide6 `QShortcut` is suitable for shortcuts while the SnapLex window has
  focus, but it is not a Windows global hotkey mechanism.
- A Windows global hotkey can be built with Win32 `RegisterHotKey` plus Qt native
  event handling, but that needs focused smoke coverage for registration,
  collision handling, cleanup on exit, keyboard layout behavior, and multi-window
  lifecycle.
- Third-party global hotkey packages would add a new dependency and more runtime
  surface before the P2 vertical slice is accepted.

## P2 Rationale

The P2 guide allows hotkey implementation only if it is stable, testable, and
does not jeopardize the clipboard MVP. The current MVP already has a deterministic
manual path:

1. Copy text into the clipboard.
2. Launch SnapLex.
3. Select `Translate Clipboard`.
4. Review, retry, copy, or close the result.

This path exercises the intended clipboard service, P1 translation pipeline, and
result presenter without adding OS-level hotkey risk.

## Deferred Follow-Up

When global hotkeys return to scope, use a small hotkey service boundary rather
than wiring Win32 or third-party hooks directly into widgets. The service should
cover:

- configurable default hotkey;
- registration success and collision/failure states;
- explicit unregister on shutdown;
- Windows manual smoke across normal launch, relaunch, and collision cases;
- no-op or unsupported-platform behavior for non-Windows environments.

