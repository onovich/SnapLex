# P0 to P1 Handoff

Date: 2026-06-22
Status: P0 baseline complete

## Current Repository Shape

- Python project metadata lives in `pyproject.toml`.
- Runtime package lives under `snaplex/`.
- Desktop bootstrap lives in `snaplex/app.py` and `snaplex/ui/app_shell.py`.
- Service contracts live in `snaplex/services/`.
- Translation provider contracts live in `snaplex/providers/`.
- Config storage contracts live in `snaplex/storage/`.
- Initial unit tests live in `tests/`.

## Validation

Use the project ops wrapper:

```powershell
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
```

The wrapper currently runs:

- `python -m ruff check .`
- `python -m ruff format --check .`
- `python -m mypy snaplex`
- `python -m compileall snaplex`
- `python -m pytest`
- repository structure check
- README docs check

## P1 Readiness

P1 can start from the existing boundaries:

- `normalize_text(...)` in `snaplex/services/text.py`
- `TranslationProvider` and request/response models in `snaplex/providers/base.py`
- `TranslationService` in `snaplex/services/translation_service.py`
- `FakeTranslationProvider` for deterministic tests
- `AppConfig` and `InMemoryConfigStore` for config defaults

Use `docs/p1_core_pipeline_goal_guide.md` as the executable P1 goal-mode guide.

## Guardrails

- Keep provider behavior outside UI.
- Keep OCR/capture behavior outside UI.
- Do not introduce network calls in tests.
- Keep fake providers deterministic.
- Keep secrets in local ignored files or environment variables only.
- Update validation config when P1 adds stable commands.
