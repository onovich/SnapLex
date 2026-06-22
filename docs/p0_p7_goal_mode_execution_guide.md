# SnapLex P0-P7 Goal Mode Execution Guide

Date: 2026-06-22
Status: full-project execution guide for delegated implementation
Total budget: 53 conversation rounds
Target owner: implementation programmer
Review owner: architect, project manager, and technical guide

## 0. Direct Goal Prompt

Use this prompt when assigning the whole project goal to a dedicated implementation programmer:

```text
Execute SnapLex P0-P7 as one continuous goal in 53 conversation rounds.

Required reading before any code changes:
- AGENTS.md
- README.md
- docs/development_plan.md
- docs/phase_plan.md
- docs/p0_p7_goal_mode_execution_guide.md
- docs/p0_repository_baseline_goal_guide.md
- docs/SnapLex_Product_Design.pdf
- docs/SnapLex_Technical_Architecture.pdf
- docs/codex-git-workflow.md
- docs/codex-ops-workflow.md

Goal:
Build SnapLex from a document-only repository into a Windows-ready Python + PySide6 desktop translation utility with clipboard translation, screen-region OCR translation, provider fallback support, local settings/history, packaging readiness, and a post-MVP expansion plan.

Execution rules:
- Treat P0-P7 as one goal, but do not skip phase gates.
- Every round must include Debug self-check, architecture self-check, validation commands/results, commit hash, push result, next-round target, and buffer usage.
- A round is complete only after relevant validation passes, the round commit is created, and the commit is pushed.
- If validation, commit, or push fails, stop and report the blocker; do not continue to the next round.
- After each phase, produce a phase PASS report and wait for architect/PM acceptance before starting the next phase.
- Do not stage unrelated files.
- Do not commit secrets, virtual environments, generated build outputs, OCR model caches, or local credentials.
- Keep UI thin. Translation, OCR, capture, provider, clipboard, config, and history logic must live behind service boundaries.
```

## 1. Required Context

SnapLex is a desktop floating utility for instant screen text capture and translation. It supports two core user flows:

- Screen translation: capture region -> OCR -> translate -> result popup.
- Clipboard translation: selected text -> hotkey or action -> clipboard -> translate -> result popup.

The MVP stack is Python + PySide6 on Windows. The architecture is layered:

- UI layer: floating widget, region overlay, popup, settings, history.
- Capture layer: screenshot and region selection support.
- OCR layer: image-to-text boundary, initially PaddleOCR-capable and fake-backend testable.
- Clipboard layer: text acquisition and empty clipboard fallback.
- Translation layer: provider abstraction, registry, fallback, timeout handling.
- Storage layer: local config and optional recent translation history.

## 2. Whole-Goal Budget

Total estimate: 53 rounds.

Budget split:

- Main delivery rounds: 45 rounds.
- Buffer rounds: 5 rounds, embedded in the phase budgets and used only for dependency friction, UI smoke fixes, OCR performance issues, packaging issues, or cross-phase regressions.
- Final validation and handoff rounds: 3 rounds, embedded in P6/P7 and used for release readiness, roadmap finalization, and project handoff.

Phase ranges:

| Rounds | Phase | Budget | Phase gate |
| --- | --- | ---: | --- |
| 1-4 | P0 Repository and Product Baseline | 4 | Runnable Python project skeleton and initial tests |
| 5-10 | P1 Core Pipeline Foundation | 6 | Reusable non-UI translation pipeline |
| 11-18 | P2 Clipboard Translation MVP | 8 | Usable clipboard-to-popup flow |
| 19-28 | P3 Screen Capture and OCR MVP | 10 | Region capture and OCR translation flow |
| 29-35 | P4 Provider Hardening and Fallbacks | 7 | Real provider adapters and fallback behavior |
| 36-41 | P5 History, Persistence, and Settings UX | 6 | Persisted settings and optional history |
| 42-48 | P6 Packaging and Release Readiness | 7 | Windows distributable and release checklist |
| 49-53 | P7 Expansion Track | 5 | Post-MVP expansion plan and optional narrow prototype |

## 3. Scope

The whole goal must deliver:

- A runnable Python + PySide6 application skeleton, then a usable desktop MVP.
- Clipboard translation with popup result.
- Screen-region capture with OCR-backed translation.
- Translation provider abstraction with fake/local development mode.
- Real provider adapters for LibreTranslate, OpenAI, and DeepL where feasible behind optional config.
- Timeout, retry, and fallback behavior.
- Local settings and optional recent translation history.
- Windows packaging path using PyInstaller.
- Documentation for setup, validation, packaging, troubleshooting, and roadmap.

## 4. Non-Scope

Do not include unless explicitly approved by the architect/PM:

- Cross-platform guarantee beyond Windows MVP.
- Production browser extension implementation.
- Cloud sync, account systems, team collaboration, or remote history storage.
- Complex plugin marketplace or provider marketplace.
- Automatic OCR model download that makes app launch slow or non-deterministic.
- Committing API keys, generated model caches, local credentials, virtual environments, or packaged build artifacts.

## 5. Architecture Boundaries

These boundaries are hard constraints:

- UI can orchestrate user actions, but must not own OCR, translation, provider, capture, clipboard, config, or history rules.
- Provider adapters must implement a stable provider contract and map external errors into internal error types.
- OCR backends must sit behind an OCR service interface, with fake backend tests available without large model downloads.
- Capture geometry, DPI handling, and screenshot backends must be separable from overlay rendering.
- Config and history storage must be testable without PySide6.
- Network providers must be mocked in automated tests; tests must not require real API keys.
- Any new dependency must be justified in the round report.
- Any deferred scope must be recorded rather than silently half-implemented.

## 6. Architect, PM, And Technical Guide Responsibilities

The architect/PM/technical guide is responsible for:

- Accepting or rejecting each phase PASS report.
- Approving scope changes, dependency additions, provider strategy changes, and storage format changes.
- Reviewing phase-level architecture boundaries before the next phase starts.
- Deciding whether buffer rounds may be consumed.
- Confirming when P6 is an MVP release candidate.
- Confirming whether P7 should remain docs-only or include a narrow prototype.

The implementation programmer is responsible for:

- Owning code changes, tests, validation, commits, and pushes.
- Reporting blockers early with exact failed commands and error snippets.
- Keeping each round small enough to review.
- Preserving unrelated user changes.

## 7. Per-Round Gate

Every round report must include:

```text
Round:
Phase:
Round goal:
Completed changes:
Debug self-check:
Architecture self-check:
Validation commands and results:
Commit hash:
Push result:
Buffer consumed:
Risks or blockers:
Next-round target:
```

Progression rules:

- Validation fails: do not commit, do not push, do not proceed.
- Validation passes but commit fails: do not proceed.
- Commit succeeds but push fails: do not proceed.
- Push succeeds: report commit hash and remote branch, then continue.
- Phase PASS report is rejected: fix within the same phase before starting the next phase.

## 8. Debug Self-Check

Every round must answer:

- Can the change be explained by the smallest relevant user workflow?
- Can failures be localized to a specific layer: tooling, app bootstrap, UI, capture, OCR, clipboard, translation, provider, storage, packaging, or docs?
- Are success, failure, empty, timeout, cancellation, stale, and missing-dependency states covered where relevant?
- If UI changed, was a repeatable manual or automated smoke path added?
- If state changed, are default, load, save, validate, and migration boundaries covered?
- If network changed, are timeout, retry, fallback, and credential-missing states covered?

## 9. Architecture Self-Check

Every round must answer:

- Does the existing source-of-truth layer remain the source of truth?
- Did UI avoid duplicating service, provider, OCR, capture, clipboard, or storage semantics?
- Are provider schema, runtime state, credential handling, and user settings separated?
- Did this round avoid pulling later-phase scope into the current phase?
- Are unrelated files, generated outputs, build artifacts, model caches, and user changes left alone?
- Is the code easier to test after this round than before?

## 10. Phase Execution Plan

### P0 - Repository and Product Baseline

Budget: 4 rounds.

Deliver:

- Python project metadata, package layout, dependency groups, and entry point.
- `snaplex/` modules for app bootstrap, services, providers, storage, and UI placeholders.
- Fake implementations for service testing.
- Initial tests and developer docs.

PASS:

- App bootstrap command runs without credentials.
- Initial tests pass.
- README and development docs explain install, run, test, and next phase.

### P1 - Core Pipeline Foundation

Budget: 6 rounds.

Deliver:

- Text normalization and language parameter handling.
- Translation provider protocol and registry.
- Fake/local provider for deterministic tests.
- Cache and error model.
- Async-friendly pipeline boundary.

PASS:

- Pipeline works without UI and without network.
- Tests cover empty input, provider failure, timeout, fallback, cache hit, and unsupported language.

### P2 - Clipboard Translation MVP

Budget: 8 rounds.

Deliver:

- Floating always-on-top widget.
- Clipboard read service.
- Result popup with source, translation, copy, retry, loading, and error states.
- Manual trigger and Windows hotkey if stable.

PASS:

- User can copy/select text, trigger translation, and see/copy result.
- Fake provider mode works offline.
- Clipboard empty and provider failure states are visible.

### P3 - Screen Capture and OCR MVP

Budget: 10 rounds.

Deliver:

- Region selection overlay.
- Screenshot capture backend.
- OCR service with fake backend and PaddleOCR-capable adapter.
- Capture -> OCR -> translate -> popup flow.
- DPI and multi-monitor smoke notes.

PASS:

- User can select a region, extract text, translate, and see result.
- OCR failure, cancel, empty OCR, and retry states are handled.
- App launch remains responsive through lazy OCR loading.

### P4 - Provider Hardening and Fallbacks

Budget: 7 rounds.

Deliver:

- LibreTranslate adapter.
- OpenAI adapter.
- DeepL adapter.
- Provider config, timeout, retry, fallback order, and provider error mapping.
- Mocked HTTP tests.

PASS:

- Tests do not call external services.
- Missing credentials and network failures are handled cleanly.
- At least fake provider plus one configurable real provider path are smoke-tested when credentials exist.

### P5 - History, Persistence, and Settings UX

Budget: 6 rounds.

Deliver:

- Local config storage.
- Settings UI integration.
- Optional recent translation history.
- History copy/delete/clear controls.
- Privacy docs.

PASS:

- Settings persist across restart.
- History can be added, listed, copied, deleted, and cleared.
- Storage tests cover defaults, malformed config, and migration/versioning.

### P6 - Packaging and Release Readiness

Budget: 7 rounds.

Deliver:

- PyInstaller configuration.
- Windows packaging command.
- Dependency and asset inclusion strategy.
- Packaged launch smoke.
- Release checklist and troubleshooting docs.

PASS:

- Clean install/build succeeds.
- Packaged app launches.
- Clipboard smoke passes in packaged app.
- Screen capture smoke passes or OCR dependency limitation is explicitly documented.

### P7 - Expansion Track

Budget: 5 rounds.

Deliver:

- Multilingual UX improvement plan.
- AI summarization design as optional provider-style capability.
- Browser extension bridge design.
- Updated roadmap with accepted, deferred, and rejected ideas.
- Optional narrow prototype only if architect/PM approves.

PASS:

- Expansion plan does not destabilize MVP.
- Prototype, if any, has tests and does not break provider contracts.
- Roadmap is clear enough for the next project goal.

## 11. Validation Matrix

| Phase | Required validation |
| --- | --- |
| P0 | install/import/bootstrap, unit tests, lint/format if configured |
| P1 | pipeline unit tests, fake provider integration, no-network test run |
| P2 | clipboard service tests, fake-provider UI integration, Windows manual smoke |
| P3 | capture geometry tests, fake OCR integration, fixture image test, Windows capture smoke |
| P4 | mocked HTTP provider tests, fallback tests, missing-credential tests |
| P5 | config and history storage tests, restart persistence smoke, privacy docs check |
| P6 | clean build, PyInstaller package, packaged launch smoke, release checklist |
| P7 | docs review, prototype tests if code exists, no MVP regression |

Always run:

```powershell
git status --short --branch
git diff --check
```

Use project wrappers when configured:

```powershell
C:\Users\Administrator\.codex\skills\project-git-workflow\scripts\git\Status.cmd
C:\Users\Administrator\.codex\skills\project-git-workflow\scripts\git\CommitAndPush.cmd -Message "<message>" -Paths "<paths>"
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
```

## 12. Phase PASS Report Template

```text
Phase:
Status:
Rounds used:
Buffer rounds consumed:
Main deliverables:
Validation commands and results:
Manual smoke evidence:
Known limitations:
Deferred scope:
Architecture notes:
Dependency changes:
Commit hashes:
Push result:
Request for architect/PM acceptance:
Recommended next phase:
```

## 13. Whole-Goal Final Report Template

```text
SnapLex P0-P7 final report:
- Status:
- Total rounds used:
- Buffer rounds consumed:
- MVP deliverables:
- Expansion deliverables:
- Validation summary:
- Packaging artifact status:
- Known limitations:
- Deferred roadmap:
- Architecture decisions:
- Commit range:
- Push result:
- Recommended next goal:
```

## 14. Escalation Rules

Escalate to the architect/PM before proceeding if:

- A phase needs more than two extra rounds.
- A dependency introduces native build friction or large runtime downloads.
- OCR model loading makes app startup slow.
- A provider API requires a contract change.
- A storage migration could lose user settings or history.
- UI implementation starts duplicating service-layer logic.
- Packaging requires committing generated binaries or large model artifacts.

## 15. Definition Of Done

The P0-P7 goal is done when:

- All phase PASS reports are accepted.
- P6 produces a Windows MVP release candidate or a clearly documented blocker.
- P7 produces the post-MVP roadmap and optional approved prototype.
- All relevant validation passes.
- The final state is committed and pushed to `origin/main`.
- README and docs describe how to install, run, test, package, troubleshoot, and continue development.

