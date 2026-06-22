# P3 Lazy Loading Notes

Date: 2026-06-22
Phase: P3 Screen Capture and OCR MVP

## Startup Rule

SnapLex app bootstrap must not import or initialize heavyweight optional capture
or OCR dependencies. These modules must stay unloaded during normal import and
no-GUI bootstrap:

- `mss`
- `mss.tools`
- `paddleocr`

Automated tests enforce this with `tests/test_lazy_optional_dependencies.py`.

## Adapter Creation

- `MssCaptureService.from_optional_dependency()` is the explicit entry point that
  imports `mss`.
- `PaddleOcrService.from_optional_dependency()` is the explicit entry point that
  imports `paddleocr`.
- `PaddleOcrService` initializes the OCR engine on first `extract_text(...)`,
  not at construction or app startup.

## Current Default Runtime Path

The default shell can still run the fake screen translation path without optional
capture/OCR dependencies. Visible real-capture smoke should install the optional
extras explicitly:

```powershell
python -m pip install -e ".[capture]"
python -m pip install -e ".[ocr]"
```

P3 final smoke should record which optional extras were installed and which paths
used fake versus real adapters.

