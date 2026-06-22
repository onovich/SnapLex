# P7 Expansion Roadmap

Date: 2026-06-22
Phase: P7 Expansion Track
Status: executor-complete roadmap, pending planner acceptance

P7 closes the P0-P7 execution track with a design-first expansion roadmap. The
accepted P6 Windows MVP package remains the product baseline. Expansion work
must start from explicit service boundaries, deterministic tests, and
privacy-first defaults before any runtime feature is added.

## Baseline To Preserve

- The `base` package remains the deterministic Windows release smoke path.
- Clipboard and screen translation continue to flow through
  `TranslationPipeline`.
- Capture, OCR, settings, history, provider configuration, packaging, future
  summary, and future browser bridge rules remain outside UI widgets.
- Config and history remain in local app data or `SNAPLEX_APP_DATA_DIR`.
- Provider API key values remain environment-only and are never stored in docs,
  config, tests, logs, package resources, or history.

## Accepted Next Ideas

These ideas are suitable for post-MVP implementation planning after P7 is
accepted.

### Localization Foundation

Start with a small locale catalog boundary and settings storage for
`ui_locale`. Keep locale selection separate from translation source/target
language and future OCR language hints.

Recommended first implementation:

- English defaults plus Simplified Chinese UI copy.
- Presenter-level message lookup tests without PySide6.
- Migration behavior for older configs without `ui_locale`.
- No change to fake provider smoke, `--no-gui`, or package smoke.

### Summary Capability Prototype

Add AI summary only as an optional capability behind future
`SummaryService`/`SummaryProvider` contracts. The first implementation should
use a deterministic fake provider and no network calls.

Recommended first implementation:

- Pure request/response models.
- Fake summary provider with success, empty input, text-too-long, timeout, and
  provider failure scenarios.
- Summary config disabled by default.
- Summary history disabled by default or kept in a separate store.
- Presenter tests before UI wiring.

### Browser Selection Bridge Proof Of Concept

Begin with local contract validation before any production extension runtime.
The browser remains an untrusted client and the desktop app remains the owner of
provider selection, credentials, settings, and history.

Recommended first implementation:

- Browser intent dataclasses and JSON schema validation.
- Rejection tests for unsupported versions, unsupported intents, empty text,
  oversized text, and disabled bridge state.
- Native messaging design remains preferred if installer work is approved.
- Clipboard handoff remains the lowest-risk fallback.
- Localhost bridge remains deferred until loopback token and origin protection
  are designed.

### Release Feedback Triage

Use P6 package smoke and manual Windows smoke feedback to decide whether the
next implementation goal should prioritize localization, summary, browser
bridge, or release hardening.

Suggested feedback buckets:

- Packaging and launch reliability.
- OCR/capture usability and optional dependency friction.
- Provider configuration and error recovery.
- Settings/history privacy clarity.
- Accessibility and keyboard operation.
- Browser workflow demand.

## Deferred Ideas

These ideas are valid future work, but should not be next unless the architect
explicitly reopens scope:

- Production browser extension implementation and browser-store packaging.
- Real AI summary provider integration and real AI network smoke.
- Global hotkeys.
- Cloud sync, accounts, keychain integration, remote history, or encryption.
- Export/import history tooling.
- Provider marketplace or plugin marketplace.
- Cross-platform packaging guarantees beyond the Windows MVP.
- Broad PySide6 visual redesign.

## Rejected For The First Post-MVP Goal

These approaches should be rejected because they weaken the accepted release
baseline or privacy model:

- Browser-side storage of provider API keys.
- Direct browser-to-provider calls for translation or summary.
- Mandatory bridge server startup during app bootstrap.
- Real network validation in automated tests.
- Bundling OCR model caches into the default package.
- Storing browser-origin text, summary text, or origin URLs by default.
- Moving provider, OCR, capture, settings, history, summary, bridge, or package
  rules into UI widgets.
- Committing extension build output, package output, screenshots, smoke data,
  local config/history, `.env`, or binaries.

## Recommended Next Goal

Recommended next implementation goal: localization foundation.

Reasoning:

- It directly improves user polish without requiring network providers, browser
  runtimes, installer work, or new package variants.
- It can be tested at service/presenter boundaries with deterministic unit
  tests.
- It prepares visible copy for later summary and browser bridge workflows.
- It has the lowest risk to the P6 package baseline.

Alternative next goals:

- Summary capability prototype if product feedback shows stronger demand for
  condensed results than localized UI.
- Browser intent contract prototype if browser-selection handoff is the top
  workflow request.
- Release hardening if P6 package smoke or manual Windows smoke reports
  priority regressions.

## Exit Criteria For Future Expansion Goals

Every post-P7 implementation goal should prove:

- `Validate.cmd` passes without network.
- `git diff --check` passes.
- `python -m snaplex --version` passes.
- `python -m snaplex --no-gui` passes.
- Package dry-run or package smoke remains green when packaging boundaries are
  touched.
- No generated artifacts, local data, provider secrets, `.env`, screenshots,
  OCR model caches, smoke data, browser build outputs, or binaries are
  committed.
- Any new runtime capability is optional, disabled by default when appropriate,
  and covered by deterministic tests.

