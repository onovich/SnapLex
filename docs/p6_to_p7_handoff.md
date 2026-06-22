# P6 to P7 Handoff

Date: 2026-06-22
Status: P6 accepted by planner; P7 ready for execution planning

Recommended next phase: P7 Expansion Track

Executable P7 guide: `docs/p7_expansion_track_goal_guide.md`

## P6 Deliverables Available To P7

- `pyproject.toml`
  - Optional `package` extra for PyInstaller.
- `scripts/package_windows.py`
  - Repeatable package wrapper with `base`, `capture`, `ocr`, and `full`
    variants.
- `packaging/snaplex.spec`
  - Tracked PyInstaller spec for the Windows MVP package.
- `snaplex/release_smoke.py`
  - Deterministic packaged workflow smoke.
- `snaplex/app.py`
  - `--smoke-package` CLI path for source and packaged release validation.
- `docs/p6_packaging_smoke_evidence.md`
  - Build, launch, and workflow smoke evidence.
- `docs/p6_release_checklist.md`
  - Release candidate checklist and cleanup guidance.
- `packaging/README.md`
  - Build, variant, smoke, troubleshooting, and cleanup instructions.
- `docs/windows_smoke_checklist.md`
  - Updated P6 smoke steps.
- `.codex/project-ops-workflow.json`
  - Package and release dry-run commands.

## Accepted Packaging Boundaries

- Packaging scripts and specs call the existing app bootstrap.
- UI remains thin and does not own provider/settings/history/OCR/capture rules.
- Settings/history continue through services and storage stores.
- Translation continues through `TranslationPipeline`.
- Local config/history live outside packaged resources and can be overridden by
  `SNAPLEX_APP_DATA_DIR`.
- Provider secrets remain environment-only values and are not persisted.

## P7 Starting Point

P7 may plan post-MVP expansion from the accepted P6 release baseline. The
planner-selected default is documentation/design-first with no production
browser extension or real AI service integration in P7. Workstreams:

- Browser extension bridge planning.
- AI summary design as an optional provider-style capability.
- Multilingual UX polish.
- Expansion roadmap and release feedback triage.

## Guardrails For P7

- Do not destabilize the P6 packaging path.
- Do not commit generated packages, screenshots, local smoke data, OCR model
  caches, `.env`, provider secrets, or user config/history files.
- Keep automated tests deterministic and no-network.
- Keep browser extension, AI summary, and multilingual work behind explicit
  boundaries; do not fold those rules into packaging scripts or existing UI
  widgets without an accepted P7 design.
- Keep global hotkeys, cloud sync/accounts, keychain integration, and provider
  rewrites out of scope unless the architect explicitly reopens them.

## Recommended P7 First Steps

1. Read `docs/p7_expansion_track_goal_guide.md`.
2. Revalidate P6 with `docs/p6_final_validation_report.md`.
3. Define expansion boundaries before touching MVP runtime code.
4. Preserve the `base` package as the deterministic release-smoke path.
