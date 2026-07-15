# P9 TODO

P9 goal: polish the SnapLex PySide6 desktop experience using Apple
HIG-inspired clarity, hierarchy, accessibility, keyboard quality, and
screenshot-backed GUI smoke, while preserving P8 provider/setup boundaries.

Status: ready for execution.

Executable guide: `docs/p9_apple_inspired_ui_ux_goal_guide.md`

Estimated budget: 16 conversation rounds.

## Tasks

- [ ] Revalidate the accepted P8 baseline.
- [ ] Produce a UI audit for main shell, result states, Settings, History, and
  region selector.
- [ ] Add or refine shared visual tokens/styles for spacing, typography, color,
  focus, and stable controls.
- [ ] Polish main shell action hierarchy and result state layout.
- [ ] Improve long text, OCR text, translation text, and small-window behavior.
- [ ] Refine Settings information architecture without moving provider rules
  into widgets.
- [ ] Improve Settings keyboard navigation, focus order, labels, tooltips, and
  accessibility metadata.
- [ ] Polish History empty/list/long-entry states and keyboard operation.
- [ ] Review region selector and screen-flow UI feedback without capture/OCR
  rewrites.
- [ ] Add screenshot-backed offscreen GUI smoke with uncommitted local artifacts.
- [ ] Record visual smoke evidence and update Windows smoke notes.
- [ ] Preserve P8 real/fake trial guardrails and no-secret boundaries.
- [ ] Produce P9 final validation report.
- [ ] Produce P9 to P10 handoff.

## Deferred Outside P9

- SnapLex Cloud, account OAuth, billing, token broker, or keychain integration.
- Raw API-key persistence in app config.
- Production browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites, OCR/capture rewrites, and real network validation in
  automated tests.
- Full localization implementation.
- Committed screenshots, package outputs, local app data, `.env`, or secrets.
