# P3 Windows Smoke Evidence

Date: 2026-06-22
Phase: P3 Screen Capture and OCR MVP
Environment: Windows PowerShell, PySide6 offscreen smoke

## Automated Validation

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`: PASS
- `python -m pytest`: 102 passed
- `python -m snaplex --version`: `SnapLex 0.1.0`
- `python -m snaplex --no-gui`: `SnapLex bootstrap OK (PySide6 available).`
- Optional backend import probe after importing `snaplex.ui.app_shell`: `mss=False`, `mss.tools=False`, `paddleocr=False`

## PySide6 Offscreen Screen Flow Smoke

The smoke path launched `launch_gui(...)` with:

- `FixedRegionSelector(ScreenRegion(left=0, top=0, width=240, height=120))`
- `FakeCaptureService`
- `FakeOcrService`
- default fake-provider `TranslationPipeline`
- `InMemoryClipboardService`

Verified:

- `Translate Screen` button is visible and clickable.
- Fake selected region flows through capture, OCR, and the P1 translation pipeline.
- Source label shows `Example screen text`.
- Result label shows `Example screen text [en]`.
- `Copy Result` writes `Example screen text [en]` to the clipboard service.

Result: PASS.

## Cancel Smoke

The smoke path launched the shell with `CancelledRegionSelector`.

Verified:

- `Translate Screen` handles a cancelled region selection.
- Status shows `Screen selection cancelled`.
- Error/detail label shows `Select a region to translate.`

Result: PASS.

## Empty OCR Smoke

The smoke path launched the shell with `FakeOcrService(scenario=FakeOcrScenario.EMPTY)`.

Verified:

- Empty OCR output maps to a user-visible state.
- Status shows `No screen text found`.
- Error/detail label shows `No text was detected in the selected region.`

Result: PASS.

## OCR Failure Smoke

The smoke path launched the shell with `FakeOcrService(scenario=FakeOcrScenario.FAILURE)`.

Verified:

- OCR failure maps to a user-visible error.
- Status shows `Translation failed`.
- Error/detail label shows `OCR failed to read text from the selected region. Try again.`

Result: PASS.

## Visible Windows Smoke Still Needed

Offscreen smoke validates shell wiring and fake capture/OCR states. A visible
manual Windows smoke should still be repeated before P3 acceptance for:

- actual full-screen region overlay click-drag-release;
- Escape cancel behavior in the overlay;
- single-monitor real `mss` capture when the `capture` extra is installed;
- visible result rendering after real capture plus fake or real OCR;
- DPI scaling behavior;
- multi-monitor coordinate behavior.

## Current DPI And Multi-Monitor Limitation

The Round 3 overlay uses active-screen local Qt coordinates, while
`MssCaptureService` expects desktop pixel coordinates. The current accepted
automated path uses injected/fixed regions. Single-monitor visible smoke is the
first real-capture target; multi-monitor and DPI conversion should be revisited
before P6 packaging.

