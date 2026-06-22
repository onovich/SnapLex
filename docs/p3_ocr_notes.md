# P3 OCR Notes

Date: 2026-06-22
Phase: P3 Screen Capture and OCR MVP

## OCR Boundary

P3 keeps OCR behind the `OcrService` protocol:

- `FakeOcrService` covers deterministic success, empty result, and failure paths.
- `PaddleOcrService` is an optional real-OCR adapter.
- Translation remains outside OCR and continues through `TranslationPipeline`.

## Lazy Optional Dependency

`PaddleOcrService.from_optional_dependency()` imports `paddleocr` only when a real
adapter is explicitly requested. The engine itself is initialized lazily on the
first `extract_text(...)` call, not during app bootstrap.

Install the optional OCR dependency only for real OCR smoke:

```powershell
python -m pip install -e ".[ocr]"
```

Automated tests do not import PaddleOCR, download OCR models, require screen
permissions, or call the network.

## Error Handling

- Missing PaddleOCR dependency maps to `OcrUnavailableError`.
- PaddleOCR engine initialization failure maps to `OcrUnavailableError`.
- OCR extraction failure maps to `OcrError`.
- Empty OCR output is represented as `OcrResult(text="")` and handled by the
  screen translation presenter/UI.

