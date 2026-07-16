# P12 Manual Environment Checks

Date: 2026-07-16
Phase: P12 Private Trial Pilot And Feedback Triage
Status: partial PASS with manual-device blockers recorded

P12 records environment checks for the first controlled private trial. Automated
executor checks can validate visible Qt windows, package smoke, and trial script
guardrails. Human assistive-technology, DPI scaling, and multi-monitor checks
remain device-specific and must be run by a tester or release owner with the
target hardware.

## Summary

| Check | Result | Notes |
| --- | --- | --- |
| Visible GUI smoke | PASS | `python scripts\p11_visible_gui_smoke.py` passed on native Windows Qt platform. |
| Packaged fake smoke | PASS | `SmokeTrial.cmd` passed and exercised packaged executable smoke because local `dist\SnapLex\SnapLex.exe` existed. |
| Source fake trial | PASS | `StartFakeTrial.cmd --no-gui` passed and labeled fake smoke mode. |
| Source real trial fail-closed | PASS | `StartTrial.cmd --no-gui` rejected missing real provider configuration. |
| Packaged fake trial | PASS | `StartPackagedFakeTrial.cmd --no-gui` passed and labeled fake smoke mode. |
| Packaged real trial fail-closed | PASS | `StartPackagedTrial.cmd --no-gui` rejected missing real provider configuration. |
| Assistive technology | NOT RUN | Requires a human tester with the intended screen reader or accessibility tooling. |
| DPI scaling | NOT RUN | Requires manual Windows display scaling changes and visual review. |
| Multi-monitor behavior | NOT RUN | Requires multiple monitor hardware or a configured equivalent. |

Generated screenshots and smoke data remain ignored local artifacts under
`snaplex-smoke-data\`.

## Commands Run

Visible GUI:

```cmd
python scripts\p11_visible_gui_smoke.py
```

Result: PASS with six ignored local screenshots:

- `idle.png`
- `fake-success.png`
- `long-small.png`
- `settings.png`
- `history-empty.png`
- `focus.png`

Packaged fake smoke:

```cmd
SmokeTrial.cmd
```

Result: PASS. The smoke checked version, no-GUI bootstrap, base package dry-run,
and packaged executable workflow smoke.

Trial scripts:

```cmd
StartFakeTrial.cmd --no-gui
StartTrial.cmd --no-gui
StartPackagedFakeTrial.cmd --no-gui
StartPackagedTrial.cmd --no-gui
```

Results:

- `StartFakeTrial.cmd --no-gui`: PASS.
- `StartTrial.cmd --no-gui`: expected rejection PASS.
- `StartPackagedFakeTrial.cmd --no-gui`: PASS.
- `StartPackagedTrial.cmd --no-gui`: expected rejection PASS.

Expected rejection text:

```text
Real translation provider is not configured.
```

## Assistive Technology Runbook

Run with the intended Windows accessibility tool, such as Narrator or another
screen reader available to the tester. Use synthetic text only.

1. Launch `StartFakeTrial.cmd`.
2. Confirm the main window title and primary actions can be discovered.
3. Move focus through `Translate Clipboard`, `Translate Screen`, `Settings`,
   and `History`.
4. Open Settings and confirm provider tabs, credential source fields, and
   disabled `Connect account (future)` are discoverable.
5. Open History and confirm disabled/empty guidance is understandable.
6. Record blocker severity using `docs/p12_feedback_intake_template.md`.

Do not attach screen-reader logs if they contain private text or personal data.

## DPI Scaling Runbook

Run on a Windows device where display scaling can be changed safely. Use fake
mode and synthetic text.

1. Set display scaling to the target value, such as 125%, 150%, or 200%.
2. Launch `StartFakeTrial.cmd`.
3. Check main shell, fake result, long text, Settings, History, and focus.
4. Run `python scripts\p11_visible_gui_smoke.py` if Qt can open windows under
   that scaling setting.
5. Record whether text overlaps, clips, becomes unreadable, or makes controls
   hard to target.

Do not capture or share screenshots that include private documents, chats,
account dashboards, or personal data.

## Multi-Monitor Runbook

Run on hardware with two or more monitors. Use fake mode and non-sensitive
regions.

1. Launch `StartFakeTrial.cmd`.
2. Move the shell between monitors and confirm it remains visible and usable.
3. Open Settings and History on each monitor if practical.
4. Try `Translate Screen` on each monitor with a non-sensitive region.
5. Cancel region selection with `Esc` and confirm recovery.
6. Record monitor layout, scaling, and whether selection geometry is wrong,
   offset, clipped, or inconsistent.

Do not attach screenshots with sensitive content. Reproduce with synthetic text
before sharing visual evidence.

## Pilot Impact

The first private pilot may continue only as a controlled pilot while AT, DPI,
and multi-monitor checks remain open manual validation items. If any manual
check later reveals an S0 blocker, apply `docs/p12_trial_pass_fail_criteria.md`
and pause the pilot until fixed.
