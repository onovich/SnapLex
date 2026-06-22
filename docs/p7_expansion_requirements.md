# P7 Expansion Requirements And MVP Freeze Notes

Date: 2026-06-22
Phase: P7 Expansion Track
Status: design baseline

P7 prepares post-MVP expansion from the accepted P6 release baseline. It is
documentation/design-first. The Windows MVP package, deterministic fake-provider
smoke path, and service boundaries are frozen unless planner validation exposes
a real regression.

## Baseline Revalidation

Round 1 revalidated the accepted P6 baseline before planning expansion:

- `Validate.cmd`: PASS with 190 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: `SnapLex bootstrap OK (PySide6 available).`
- `python scripts\package_windows.py --dry-run --variant base`: PASS.

The first sandboxed `Validate.cmd` attempt failed because pytest could not read
the default Windows temp directory under the managed filesystem sandbox. The
same command passed when rerun with normal temp-directory access. This was an
environment permission issue, not an application regression.

## MVP Freeze

Frozen MVP behavior:

- Clipboard flow remains
  `ClipboardService -> TranslationPipeline -> result presenter -> optional HistoryService`.
- Screen flow remains
  `RegionSelector -> CaptureService -> OcrService -> TranslationPipeline -> result presenter -> optional HistoryService`.
- Settings flow remains `SettingsPresenter -> SettingsService -> ConfigStore`.
- History flow remains `HistoryPresenter -> HistoryService -> HistoryStore`.
- Provider adapters remain behind `TranslationProvider`, provider registry,
  provider config, retry, and mocked HTTP tests.
- Packaging remains `snaplex.__main__ -> snaplex.app.main` through the tracked
  PyInstaller spec and `scripts/package_windows.py`.
- The `base` package remains the deterministic release-smoke path.

Frozen storage and secret handling:

- Config and history files stay in local app data or `SNAPLEX_APP_DATA_DIR`.
- Provider API key values stay in environment variables only.
- Docs, tests, config, package resources, and smoke logs must not include real
  API key values.
- Generated `build\`, `dist\`, screenshots, OCR model caches, local smoke data,
  `.env`, `config.json`, and `history.json` remain out of git.

## Expansion Principles

- Prefer design notes and contracts before runtime code.
- Keep expansion features optional and removable.
- Keep automated validation deterministic, offline, and no-network.
- Put new semantics behind service boundaries rather than UI widgets or
  packaging scripts.
- Treat privacy-sensitive text as user data even when it originates from
  clipboard, OCR, browser pages, or future summaries.
- Avoid dependencies that slow app bootstrap, break `--no-gui`, or change the
  P6 package smoke path.

## Accepted Expansion Candidates

These candidates are appropriate for post-MVP planning:

- Multilingual UX and localization structure for visible copy, locale
  selection, language-pair defaults, OCR hints, provider support messaging, and
  fallback states.
- AI summary as a separate optional capability with future
  `SummaryService`/`SummaryProvider` boundaries.
- Browser extension bridge design with explicit browser-to-desktop data
  contracts, trust boundaries, and local app discovery choices.
- Expansion roadmap that keeps the Windows MVP package as the release baseline.
- Release feedback triage categories for packaging, OCR/capture, providers,
  settings/history, and accessibility.

## Deferred Candidates

These candidates need later approval or implementation phases:

- Production browser extension runtime.
- Real AI summary provider integration.
- Global hotkeys.
- Cloud sync, accounts, keychain integration, encryption, and remote history.
- Export/import history tooling.
- Provider marketplace or plugin marketplace.
- Cross-platform packaging guarantees beyond the Windows MVP.
- Broad visual redesign of the PySide6 shell.

## Rejected For P7

These are explicitly rejected inside P7 because they would destabilize the
accepted release baseline or require external dependencies:

- Adding real network calls for AI summary or provider smoke.
- Adding mandatory dependencies for localization, browser integration, AI
  summary, capture, OCR, or packaging.
- Storing provider secrets in settings, docs, tests, fixtures, or package
  resources.
- Bundling OCR model caches into the default package.
- Making browser-origin text or summarized text persist by default.
- Moving provider, OCR, capture, settings, history, or packaging rules into UI
  widgets.

## P7 Deliverable Map

- Round 1: this requirements and freeze document.
- Round 2: multilingual UX and localization boundary plan.
- Round 3: AI summary capability design.
- Round 4: browser extension bridge design.
- Round 5: expansion roadmap, P7 final validation report, and P0-P7 closure
  report.
