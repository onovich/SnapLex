# P14 Manual AT, DPI, And Multi-Monitor Results

Date: 2026-07-16
Phase: P14 Manual Environment And Source Keyring Validation
Status: assistive-technology blocker recorded; DPI and multi-monitor pending

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
| DPI scaling | PENDING | To be recorded in Round 3. |
| Multi-monitor behavior | PENDING | To be recorded in Round 4. |

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
