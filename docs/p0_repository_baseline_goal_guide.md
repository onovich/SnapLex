# P0 Repository and Product Baseline Goal Mode Guide

Date: 2026-06-22
Status: execution guide for P0
Estimated budget: 4 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P0 in goal mode:

```text
Execute SnapLex P0 - Repository and Product Baseline in 4 conversation rounds.

Required reading:
- AGENTS.md
- README.md
- docs/development_plan.md
- docs/phase_plan.md
- docs/SnapLex_Product_Design.pdf
- docs/SnapLex_Technical_Architecture.pdf
- docs/codex-git-workflow.md
- docs/codex-ops-workflow.md

Goal:
Turn the current document-only SnapLex repository into a runnable Python + PySide6 project skeleton with stable service/provider/storage/UI boundaries, fake implementations, initial tests, and developer docs.

Rules:
- Every round must include a Debug self-check, architecture self-check, validation commands and results, commit hash, push result, next-round target, and whether a buffer was consumed.
- Do not stage unrelated files.
- Do not move provider, OCR, capture, or storage logic into the UI layer.
- Validate before commit.
- Commit and push the successful round before moving to the next round.
- If validation, commit, or push fails, stop and report the blocker instead of moving to the next round.
```

## 1. Required Context

- SnapLex is a desktop floating utility for instant screen text capture and translation.
- MVP target is Windows with Python + PySide6.
- Product flows are screen-region OCR translation and clipboard translation.
- Architecture layers are UI, capture, OCR, clipboard, translation providers, and storage.
- The P0 phase must prepare the repository foundation only; it should not try to complete the clipboard or OCR MVP.

## 2. Scope

- Add Python project metadata and dependency groups.
- Add package layout under `snaplex/`.
- Add app bootstrap that can run without real OCR models or API credentials.
- Define service/provider/storage interfaces and fake implementations.
- Add initial unit tests.
- Add setup, development, and smoke-test documentation.
- Configure repeatable validation commands in the project ops workflow if appropriate.

## 3. Non-Scope

- No full global hotkey implementation.
- No real PaddleOCR model download unless needed for interface validation.
- No real OpenAI, DeepL, or LibreTranslate network integration.
- No PyInstaller package.
- No persistent history UI.
- No browser extension work.

## 4. Per-Round Fixed Workflow

Each round must follow this gate:

```text
Round report must include:
- Round goal
- Completed changes
- Debug self-check
- Architecture self-check
- Validation commands and results
- Commit hash and push result
- Next-round target
- Whether a buffer round was consumed

Progression rules:
- If validation fails: do not commit, do not push, do not move to the next round.
- If validation passes but commit fails: do not move to the next round.
- If commit succeeds but push fails: do not move to the next round.
- If push succeeds: record commit hash and remote branch, then move to the next round.
```

Debug self-check:

- Can the current change be explained by the smallest relevant user workflow?
- Can failures be localized to project metadata, app bootstrap, service contract, provider contract, storage, or UI shell?
- Are success, failure, empty, and missing-dependency states covered where relevant?
- If UI changed, was a repeatable smoke path documented?
- If config changed, are sample, default, and local-secret boundaries clear?

Architecture self-check:

- Does each layer keep its source of truth?
- Does UI avoid duplicating translation, OCR, capture, provider, or storage semantics?
- Are provider contracts, runtime state, and user configuration separated?
- Did the round avoid pulling P1/P2/P3 scope into P0?
- Are generated outputs, local virtual environments, and unrelated files left out of git?

## 5. Round Plan

Round 1 - Project metadata and runnable shell:

- Add `pyproject.toml`.
- Add package directories and app entry point.
- Add a minimal PySide6 app shell or CLI-safe bootstrap fallback if PySide6 is not installed yet.
- Add README setup instructions.
- Validate install/import/bootstrap.

Round 2 - Service contracts and fake implementations:

- Define capture, OCR, clipboard, translation, provider, and storage boundaries.
- Add fake translation provider and fake OCR service.
- Keep contracts testable without launching the UI.
- Validate imports and basic fake service behavior.

Round 3 - Initial tests and developer workflows:

- Add unit tests for text normalization, fake provider, fake OCR, and config defaults.
- Add lint/format/test commands or document why a command is deferred.
- Update project ops workflow config if validation commands become stable.
- Validate tests and docs.

Round 4 - Documentation, smoke checklist, and final cleanup:

- Update development docs with actual commands and package layout.
- Add a Windows manual smoke checklist for app launch.
- Run full available validation.
- Commit and push final P0 state.

## 6. PASS Criteria

P0 passes when:

- The repository has Python project metadata and a clear package layout.
- A developer can install dependencies and run the SnapLex bootstrap command.
- Service/provider/storage interfaces exist and are covered by fake implementations.
- Initial tests pass locally.
- Documentation explains setup, validation, and P1 readiness.
- No secrets, virtual environments, generated outputs, or unrelated files are committed.
- The final P0 commit is pushed to `origin/main`.

## 7. Final Report Template

```text
P0 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation run:
- Known limitations:
- Commit hashes:
- Push result:
- Recommended next phase:
```

