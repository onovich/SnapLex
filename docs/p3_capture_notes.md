# P3 Capture Notes

Date: 2026-06-22
Phase: P3 Screen Capture and OCR MVP

## Screenshot Backend

P3 introduces `MssCaptureService` behind the existing `CaptureService` protocol.
The adapter lazy-loads `mss` only when `MssCaptureService.from_optional_dependency()`
is called. App bootstrap, no-GUI checks, unit tests, and fake capture flows do not
require the `capture` extra.

Install the optional capture dependency when exercising the real screenshot path:

```powershell
python -m pip install -e ".[capture]"
```

## Error Handling

- Missing `mss` dependency maps to `CaptureError` with an install hint.
- Screenshot grab or PNG encoding failures map to `CaptureError`.
- Automated tests use fake mss clients and do not require screen permissions.

## Current Assumptions

- The initial region selection overlay uses the active screen's local Qt
  coordinates.
- `MssCaptureService` expects `ScreenRegion` values in desktop pixel coordinates.
- Single-monitor smoke is the accepted first path.
- DPI scaling and multi-monitor coordinate conversion need visible Windows smoke
  before P3 acceptance; record final evidence in the P3 smoke report.

