# P9 Visual Smoke Evidence

Date: 2026-07-15
Phase: P9 Apple-Inspired UI/UX Polish
Status: Round 12 evidence

## Automated Offscreen Smoke

Command:

```powershell
python scripts\p9_gui_smoke.py
```

Result:

- PASS.
- Generated seven local screenshots under
  `snaplex-smoke-data\p9-screenshots`.
- Verified each screenshot is non-null, at least 300x250, and has more than
  one sampled color.
- Screenshots remain ignored local smoke artifacts and are not committed.

Scenarios covered:

- `idle.png`: main shell idle.
- `loading.png`: loading state.
- `fake-success.png`: fake provider success with fake-mode warning.
- `error.png`: provider/error state.
- `long-small.png`: long source and translation text at 390x420.
- `settings.png`: Settings provider setup tabs.
- `history-empty.png`: History empty/disabled state.

## Focus And Accessibility Smoke

Round 7 offscreen smoke verified key Settings controls expose accessible names:

- Provider.
- Fallback provider order.
- Source language.
- Target language.
- Test provider connection.
- OpenAI API key env var.
- DeepL API key env var.
- Enable translation history.
- Save Settings.

Main shell commands and History commands keep visible text labels while adding
Qt standard icons, tooltips, and accessible names. P9 did not introduce
icon-only commands.

## Long Text And Small Window Smoke

Round 5 offscreen smoke rendered a long fake-provider success result at
390x420. Source and translated text now use read-only, selectable, wrapped,
scrollable text regions with stable heights.

## Known Offscreen Limitation

In this Codex execution environment, Qt offscreen font discovery reports zero
font families. Screenshots therefore render visible text as square glyphs even
after the app sets the preferred `Segoe UI` family. The smoke still catches
nonblank rendering, geometry, state visibility, local artifact placement, and
basic layout constraints. Visible Windows smoke with normal desktop fonts
remains recommended before public trial distribution.

## Visible Windows Smoke

Visible Windows smoke was not run in this executor session because the work was
validated through deterministic offscreen automation. Recommended manual visible
checks:

1. Launch `python -m snaplex` with a local `SNAPLEX_APP_DATA_DIR`.
2. Confirm main shell hierarchy, icons, focus outlines, fake warning, and long
   text scrolling.
3. Open Settings and verify Setup, Provider Details, and History tabs.
4. Verify tab order through Settings and History.
5. Open History when empty and after adding entries.
6. Run `StartTrial.cmd --no-gui` and `StartFakeTrial.cmd --no-gui` to preserve
   real/fake guardrails.

## Artifact Boundary

Screenshot files, smoke app data, package outputs, local config/history,
ignored caches, `.env`, and secrets must remain out of git. Round 12 status
confirmed screenshot artifacts are ignored under `snaplex-smoke-data`.
