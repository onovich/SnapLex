# P5 to P6 Handoff

Date: 2026-06-22
Status: P5 settings/history implementation complete; awaiting planner acceptance

Recommended next phase: P6 Packaging and Release Readiness

## P6 Goal

Package the Windows MVP and make release validation repeatable.

## P5 Deliverables Available To P6

- `snaplex/storage/config.py`
  - `JsonFileConfigStore`
  - `CONFIG_FILE_NAME`
  - config serialization/deserialization and migration hooks
- `snaplex/storage/history.py`
  - `JsonFileHistoryStore`
  - `TranslationHistoryEntry`
  - history serialization/deserialization
- `snaplex/storage/paths.py`
  - `default_app_data_dir(...)`
  - `SNAPLEX_APP_DATA_DIR`
- `snaplex/services/settings_service.py`
  - settings update/save service boundary
- `snaplex/services/history_service.py`
  - recent translation history service boundary
- `snaplex/ui/settings_presenter.py`
  - testable settings form presenter
- `snaplex/ui/history_presenter.py`
  - testable history list presenter
- `docs/p5_privacy_and_storage.md`
  - local data and privacy notes

## Accepted Runtime Flows

Clipboard:

```text
ClipboardService -> TranslationPipeline -> result presenter -> optional HistoryService
```

Screen:

```text
RegionSelector -> CaptureService -> OcrService -> TranslationPipeline -> result presenter -> optional HistoryService
```

Settings:

```text
Settings dialog -> SettingsPresenter -> SettingsService -> ConfigStore
```

History:

```text
History dialog -> HistoryPresenter -> HistoryService -> HistoryStore
```

P6 should preserve these flows. Packaging should not move provider, settings,
history, OCR, or capture rules into UI or packaging scripts.

## Recommended P6 Implementation Order

1. Add packaging metadata and a PyInstaller spec or equivalent packaging entry.
2. Ensure config/history local data files are outside packaged app resources and
   continue to use the local app data directory.
3. Document optional extras and packaging limitations for GUI, capture, and OCR.
4. Smoke packaged launch with fake provider and no credentials.
5. Smoke packaged clipboard flow, settings persistence, history clear path, and
   screen flow where optional dependencies are available.
6. Add release checklist and troubleshooting docs.

## Guardrails

- Do not commit packaged binaries, build directories, virtual environments,
  generated config/history files, `.env`, OCR model caches, screenshots, or local
  user data.
- Do not store provider API key values in app config or package resources.
- Do not add browser extension, AI summary, cloud sync, accounts, or global
  hotkeys in P6.
- Keep automated tests deterministic and no-network.
- Visible packaging smoke may be manual, but command paths and limitations must
  be documented.

## P5 Known Limitations For P6

- Settings and history UI is compact and utility-focused.
- Visible Windows GUI smoke should be repeated before packaging acceptance.
- History is local text metadata only and has no export/import flow.
- OCR/capture optional dependencies remain lazy and may require explicit package
  inclusion decisions in P6.
