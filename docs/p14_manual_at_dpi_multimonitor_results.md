# P14 Manual AT, DPI, And Multi-Monitor Results

Date: 2026-07-16
Phase: P14 Manual Environment And Source Keyring Validation
Status: AT/DPI/multi-monitor blockers recorded

P14 records target-device manual environment validation separately from
automated GUI smoke. Automated smoke can prove that SnapLex still opens,
renders, exposes focusable controls, and keeps screenshots local and ignored.
It cannot honestly prove a human screen-reader, DPI scaling, or multi-monitor
workflow unless those device conditions are available.

## Summary

| Check | Result | Evidence |
| --- | --- | --- |
| Visible GUI baseline | PASS | Round 1 `python scripts\p11_visible_gui_smoke.py` passed with six ignored local screenshots. |
| Assistive technology | BLOCKED / NOT RUN | No human screen-reader session or target assistive-technology tool was supplied to this executor. |
| DPI scaling | BLOCKED / NOT RUN | No manual Windows display-scaling change or target scaling review was supplied to this executor. |
| Multi-monitor behavior | BLOCKED / NOT RUN | No multi-monitor hardware, configured equivalent, or manual overlay/capture review was supplied to this executor. |

## Assistive-Technology Validation

Result: BLOCKED / NOT RUN.

Blocker:

- No human tester with Windows Narrator or another target assistive-technology
  tool was supplied.
- No privacy-safe screen-reader transcript or tester observation was supplied.
- The executor cannot truthfully claim screen-reader usability without a human
  AT session.

Supporting automated evidence:

- Round 1 `python scripts\p11_visible_gui_smoke.py` passed on the visible
  Windows Qt platform.
- The visible smoke exercised shell, Settings, History, long text, fake
  warnings, and focus states.
- The `focus` scenario checks that the `Translate Clipboard` control can be
  focused through its accessible name.

This supporting evidence lowers launch risk but is not a substitute for a
manual assistive-technology pass.

## Required AT Follow-Up

Run this on a target Windows device with the intended screen reader. Use only
synthetic text.

1. Launch `StartFakeTrial.cmd`.
2. Confirm the main window title and primary actions can be discovered.
3. Move focus through `Translate Clipboard`, `Translate Screen`, `Settings`,
   and `History`.
4. Open Settings and confirm provider tabs, credential source fields,
   readiness status, and disabled `Connect account (future)` are discoverable.
5. Open History and confirm disabled/empty guidance is understandable.
6. Record blocker severity with the P12/P13 taxonomy.

Do not attach screen-reader logs if they contain private text, personal data,
provider secrets, `.env` content, keyring exports, screenshots with sensitive
content, or local app data.

## Current Severity

Assistive technology remains an S2 investigation item, not an accepted S0/S1
runtime blocker, because:

- deterministic validation passes;
- fake and packaged smoke paths pass;
- real trial paths fail closed;
- no external tester reported an AT failure;
- the missing condition is the human screen-reader session, not a known broken
  SnapLex workflow.

If a future AT run produces privacy-safe S0/S1 evidence, add it to
`docs/p14_tester_feedback_intake_log.md`, reproduce safely, and triage before
any code fix.

## DPI Scaling Validation

Result: BLOCKED / NOT RUN.

Blocker:

- No target Windows display-scaling change was supplied for this executor
  session.
- No privacy-safe tester observation was supplied for 125%, 150%, 200%, or
  other target scaling values.
- The executor cannot truthfully claim DPI scaling pass without changing the
  display environment and reviewing the visible result.

Supporting automated evidence:

- Round 1 `python scripts\p9_gui_smoke.py` passed offscreen GUI smoke at fixed
  representative sizes, including the `long-small` scenario at 390x420.
- Round 1 `python scripts\p11_visible_gui_smoke.py` passed visible Windows GUI
  smoke, including `long-small`, Settings, History, and focus states.
- These smoke paths show that common small-window layouts still render and
  remain nonblank in the current desktop environment.

This supporting evidence is not a replacement for manual DPI scaling review.

## Required DPI Follow-Up

Run this on a target Windows device where display scaling can be changed safely.
Use fake mode and synthetic text only.

1. Set display scaling to a target value such as 125%, 150%, or 200%.
2. Launch `StartFakeTrial.cmd`.
3. Check the main shell, fake result, long source/translation text, Settings,
   History, and visible focus states.
4. Run `python scripts\p11_visible_gui_smoke.py` if Qt can open windows under
   that scaling setting.
5. Record whether text overlaps, clips, becomes unreadable, or makes controls
   hard to target.

Do not capture or share screenshots that include private documents, chats,
account dashboards, personal data, provider secrets, `.env` content, or local
app data.

## DPI Severity

DPI scaling remains an S2 investigation item, not an accepted S0/S1 runtime
blocker, because:

- deterministic validation passes;
- visible GUI smoke passes in the current desktop environment;
- no external tester reported clipping or unusable DPI behavior;
- the missing condition is manual target scaling review, not known broken
  SnapLex behavior.

If future DPI evidence shows clipping, overlap, or unusable controls, add it to
`docs/p14_tester_feedback_intake_log.md`, reproduce safely, and triage before
any code fix.

## Multi-Monitor Validation

Result: BLOCKED / NOT RUN.

Blocker:

- No multiple-monitor hardware or configured equivalent was supplied to this
  executor.
- No privacy-safe tester observation was supplied for moving the shell,
  Settings, History, or result windows between monitors.
- No manual screen-translation overlay/capture coordinate review was supplied.
- The executor cannot truthfully claim multi-monitor pass without target
  hardware or a validated equivalent.

Supporting automated evidence:

- Round 1 `python scripts\p11_visible_gui_smoke.py` passed visible Windows GUI
  smoke on the current desktop environment.
- Round 1 `cmd /c SmokeTrial.cmd` passed deterministic packaged workflow smoke,
  including fake capture/OCR screen translation inside the packaged executable.
- Existing tests continue to cover region selection, fake capture/OCR, and
  screen presenter behavior deterministically.

This supporting evidence is not a replacement for a real multi-monitor
geometry and overlay review.

## Required Multi-Monitor Follow-Up

Run this on hardware with two or more monitors, or on a configured equivalent
that exercises Windows monitor geometry. Use fake mode and non-sensitive
synthetic content.

1. Launch `StartFakeTrial.cmd`.
2. Move the shell between monitors and confirm it remains visible and usable.
3. Open Settings and History on each monitor if practical.
4. Try `Translate Screen` on each monitor with a non-sensitive region.
5. Cancel region selection with `Esc` and confirm recovery.
6. Record monitor layout, scaling, and whether selection geometry is wrong,
   offset, clipped, or inconsistent.

Do not attach screenshots with private documents, chats, account dashboards,
personal data, provider secrets, `.env` content, keyring exports, or local app
data. Reproduce with synthetic text before sharing visual evidence.

## Multi-Monitor Severity

Multi-monitor behavior remains an S2 investigation item, not an accepted S0/S1
runtime blocker, because:

- deterministic validation passes;
- fake screen/capture smoke passes in the current environment;
- no external tester reported multi-monitor geometry failure;
- the missing condition is target multi-monitor hardware/manual review, not a
  known broken SnapLex workflow.

If future multi-monitor evidence shows overlay coordinate errors, stuck
selection, unrecoverable cancel behavior, or unusable windows, add it to
`docs/p14_tester_feedback_intake_log.md`, reproduce safely, and triage before
any code fix.

## Round 2 Self-Checks

Debug self-check:

- The current change is explained by assistive-technology validation evidence.
- Pass, blocked, no-feedback, ignored-screenshot, and no-secret states are
  covered.
- No screenshots, logs, package outputs, keyring exports, `.env` files, tester
  personal data, or provider secrets are staged.

Architecture self-check:

- No UI, provider, credential, trial, OCR, capture, or packaging code was
  changed.
- The document does not promise account OAuth, SnapLex Cloud, hosted token
  brokering, packaged keyring support, or real network validation.
- P14 still avoids a credential-capable package implementation.

## Round 3 Self-Checks

Debug self-check:

- The current change is explained by DPI scaling validation evidence.
- Pass, blocked, no-feedback, ignored-screenshot, small-window, and no-secret
  states are covered.
- No screenshots, logs, package outputs, keyring exports, `.env` files, tester
  personal data, or provider secrets are staged.

Architecture self-check:

- No UI, provider, credential, trial, OCR, capture, or packaging code was
  changed.
- The document does not promise account OAuth, SnapLex Cloud, hosted token
  brokering, packaged keyring support, or real network validation.
- P14 still avoids a credential-capable package implementation.

## Round 4 Self-Checks

Debug self-check:

- The current change is explained by multi-monitor validation evidence.
- Pass, blocked, no-feedback, fake screen smoke, ignored-screenshot, and
  no-secret states are covered.
- No screenshots, logs, package outputs, keyring exports, `.env` files, tester
  personal data, or provider secrets are staged.

Architecture self-check:

- No UI, provider, credential, trial, OCR, capture, or packaging code was
  changed.
- The document does not promise account OAuth, SnapLex Cloud, hosted token
  brokering, packaged keyring support, or real network validation.
- P14 still avoids a credential-capable package implementation.
