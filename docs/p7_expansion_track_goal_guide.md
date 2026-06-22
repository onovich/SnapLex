# P7 Expansion Track Goal Mode Guide

Date: 2026-06-22
Status: execution guide for P7 after accepted P6
Estimated budget: 5 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P7 in goal mode:

```text
Execute SnapLex P7 - Expansion Track in 5 conversation rounds.

Required reading before changes:
- AGENTS.md
- README.md
- docs/development_plan.md
- docs/phase_plan.md
- docs/p0_p7_goal_mode_execution_guide.md
- docs/p6_final_validation_report.md
- docs/p6_to_p7_handoff.md
- docs/p6_packaging_smoke_evidence.md
- docs/p6_release_checklist.md
- docs/p7_todo.md
- docs/p7_expansion_track_goal_guide.md
- docs/windows_smoke_checklist.md
- docs/codex-git-workflow.md
- docs/codex-ops-workflow.md

P6 is accepted. Prepare the post-MVP expansion track without destabilizing the
Windows MVP release baseline.

Goal:
Create the P7 expansion plan and final P0-P7 closure package: requirements and
MVP freeze notes, multilingual UX plan, AI summary capability design, browser
extension bridge design, expansion roadmap, P7 final validation report, and
P0-P7 overall final report.

Default planner decision:
P7 is documentation/design-first. Do not implement a production browser
extension, real AI service integration, cloud sync, accounts, global hotkeys, or
new runtime product features. A narrow prototype is allowed only if it is
explicitly documented as non-production, has tests, does not affect the P6
package path, and does not require network credentials.

Rules:
- Preserve the accepted P6 packaging path and deterministic fake-provider smoke.
- Keep UI, provider, settings, history, OCR, capture, and packaging boundaries
  intact.
- Do not store provider API key values in config, package resources, docs, logs,
  or test fixtures.
- Automated validation must remain deterministic and no-network.
- Every round must include Debug self-check, architecture self-check, validation
  commands and results, commit hash, push result, next-round target, and whether
  a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to
  the next round.
```

## 1. Required Context

P6 PASS evidence:

- `docs/p6_final_validation_report.md` is planner-accepted.
- P6 used 7 rounds and 0 buffer rounds.
- P6 delivered a PyInstaller packaging path, package variants, tracked spec,
  package/release dry-run wrappers, deterministic packaged workflow smoke,
  release checklist, troubleshooting docs, and artifact/secret boundary scans.
- P6 handoff is `docs/p6_to_p7_handoff.md`.

Accepted runtime boundaries to preserve:

- Clipboard flow: `ClipboardService -> TranslationPipeline -> result presenter -> optional HistoryService`.
- Screen flow: `RegionSelector -> CaptureService -> OcrService -> TranslationPipeline -> result presenter -> optional HistoryService`.
- Settings flow: `SettingsPresenter -> SettingsService -> ConfigStore`.
- History flow: `HistoryPresenter -> HistoryService -> HistoryStore`.
- Provider integrations remain behind `TranslationProvider`, provider registry,
  config, retry, and mocked HTTP tests.
- Packaging invokes `snaplex.__main__ -> snaplex.app.main` and does not own app
  business rules.
- Config/history files live in local app data or `SNAPLEX_APP_DATA_DIR`, not
  inside packaged resources.

## 2. Scope

P7 must complete:

- Revalidate the accepted P6 release baseline before planning expansion.
- Create expansion requirements and MVP freeze notes.
- Create multilingual UX and localization boundary notes.
- Create AI summary design as an optional provider-style capability.
- Create browser extension bridge design with data contracts, trust boundaries,
  and security/privacy notes.
- Create expansion roadmap with accepted, deferred, and rejected ideas.
- Create `docs/p7_final_validation_report.md`.
- Create `docs/p0_p7_final_report.md`.
- Update README, phase plan, development plan, smoke checklist, TODO, and handoff
  references as needed.

Preferred P7 docs:

- `docs/p7_expansion_requirements.md`
- `docs/p7_multilingual_ux_plan.md`
- `docs/p7_ai_summary_design.md`
- `docs/p7_browser_extension_bridge.md`
- `docs/p7_expansion_roadmap.md`
- `docs/p7_final_validation_report.md`
- `docs/p0_p7_final_report.md`

## 3. Non-Scope

Do not implement in P7:

- Production browser extension runtime.
- Real AI summary provider integration or real AI network smoke.
- Cloud sync, accounts, keychain integration, remote history, or encryption.
- Global hotkeys.
- Provider rewrites or new mandatory provider dependencies.
- OCR/capture rewrites.
- UI redesign beyond small documentation-supported terminology notes.
- Packaging changes beyond documentation references unless validation exposes a
  real P6 packaging regression.
- Committing packaged binaries, installers, `dist/`, `build/`, virtual
  environments, OCR model caches, generated config/history files, `.env`,
  screenshots, smoke data, or local user data.

## 4. Planner Decisions And Assumptions

- P7 is design-first because P6 produced the release baseline and expansion
  features should not destabilize it.
- Multilingual UX should start as a product and architecture plan. Do not add a
  broad i18n implementation in P7 unless the planner explicitly reopens scope.
- AI summary should be modeled as a separate capability boundary, not folded
  into the existing translation provider contract.
- Browser extension work should be a bridge design with WebExtension-oriented
  data contracts and trust boundaries, not an installed production extension.
- Any optional prototype must be isolated, deterministic, no-network, and fully
  test-covered. It must be easy to remove without affecting the MVP runtime.
- The `base` package remains the deterministic release-smoke path.

## 5. Architecture Boundaries

Hard constraints:

- Existing source-of-truth layers remain the source of truth. UI widgets must
  not own provider, settings, history, OCR, capture, summary, or bridge rules.
- AI summary design must introduce a separate future boundary such as
  `SummaryService` / `SummaryProvider`, with explicit inputs, outputs, failure
  states, and privacy handling.
- Browser bridge design must keep browser-origin data, local desktop intents,
  provider credentials, and history persistence separate.
- Multilingual UX planning must separate visible copy, locale selection,
  language-pair defaults, provider language support, and OCR language hints.
- P7 must not add mandatory dependencies that affect app bootstrap, no-GUI mode,
  package smoke, or offline tests.
- Tests and validation must not depend on real provider network calls.
- Generated outputs and user data must remain out of git.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P7 Expansion Track
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

- Validation fails: do not commit, do not push, do not move to the next round.
- Validation passes but commit fails: do not move to the next round.
- Commit succeeds but push fails: do not move to the next round.
- Push succeeds: record commit hash and remote branch, then move to the next
  round.
- Any scope expansion beyond this guide must be explicitly approved by the
  architect/PM before implementation.

Debug self-check:

- Can the current change be explained by the smallest relevant expansion
  workflow or document?
- Can failures be localized to docs, links, scope boundaries, UI terminology,
  future capability contracts, bridge contracts, validation, or packaging
  regression?
- Are success, failure, empty, unsupported, privacy-sensitive, stale, and
  incompatible states covered where relevant?
- If a prototype is introduced, is it deterministic, no-network, tested, and
  isolated from MVP runtime paths?
- If generated outputs were created, are they ignored and left uncommitted?

Architecture self-check:

- Does the existing P6 release baseline remain stable?
- Did UI/docs avoid duplicating provider, settings, history, OCR, capture,
  packaging, summary, or bridge semantics?
- Are summary capability, browser bridge, localization, provider support, and
  runtime state separated?
- Did this round avoid pulling deferred production scope into P7?
- Are unrelated files, build outputs, packaged artifacts, model caches,
  screenshots, local data, and user changes left alone?

## 7. Round Plan

Round 1 - Baseline revalidation and expansion requirements:

- Revalidate P6 with the core validation matrix.
- Create expansion requirements and MVP freeze notes.
- Identify accepted, deferred, and rejected expansion candidates from existing
  docs and handoffs.
- Keep P7 explicitly design-first unless a narrow prototype is justified.

Round 2 - Multilingual UX plan:

- Create multilingual UX and localization boundary notes.
- Cover UI copy, locale selection, language-pair defaults, OCR language hints,
  provider language support, fallback messaging, and storage impact.
- Do not implement broad i18n in this round.

Round 3 - AI summary capability design:

- Create AI summary design as an optional capability separate from translation.
- Define future service/provider boundaries, request/response shapes, failure
  states, privacy behavior, history interaction, settings needs, and no-network
  test strategy.
- Do not add real AI provider calls or credentials.

Round 4 - Browser extension bridge design:

- Create browser extension bridge design with WebExtension-oriented flows.
- Define data contracts, desktop handoff options, permission model, trust
  boundary, local app discovery assumptions, privacy risks, and MVP-safe
  rejection criteria.
- Do not implement a production browser extension.

Round 5 - Roadmap, final reports, and closure validation:

- Create expansion roadmap with accepted, deferred, and rejected ideas.
- Create `docs/p7_final_validation_report.md`.
- Create `docs/p0_p7_final_report.md`.
- Mark `docs/p7_todo.md` complete.
- Update README, phase plan, development plan, windows smoke checklist, and
  entry points so they reflect P7 completion.
- Run final validation, boundary scans, commit, push, and report back to the
  planner/checker session for P7 acceptance.

## 8. Validation Matrix

Required P7 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- Documentation link/index check for all new P7 docs.
- Boundary scan showing no committed `build/`, `dist/`, packaged binaries,
  generated local config/history, `.env`, provider keys, OCR model caches,
  screenshots, smoke data, or local app data.

If code or a prototype is introduced, also require:

- Focused unit tests for the new boundary.
- No-network tests.
- Proof that app bootstrap, no-GUI mode, package smoke assumptions, and P6
  boundaries remain unchanged.

No P7 validation may require:

- Real API credentials.
- Real provider network calls.
- Installed browser extension runtime.
- Cloud sync/accounts.
- Committing generated binaries or OCR model caches.

## 9. PASS Criteria

P7 passes when:

- P6 baseline is revalidated or any blocker is documented with a concrete
  remediation path.
- Expansion requirements and MVP freeze notes exist.
- Multilingual UX, AI summary, and browser extension bridge plans exist with
  clear boundaries.
- The expansion roadmap separates accepted, deferred, and rejected ideas.
- P7 final validation report and P0-P7 final report are created.
- Existing MVP validation remains green.
- No generated artifacts, local data, provider secrets, `.env`, screenshots, or
  smoke data are committed.
- Final P7 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P7 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Expansion decisions:
- Deferred scope:
- Architecture notes:
- Prototype status:
- Secret/local-data handling:
- Artifact exclusion evidence:
- Commit hashes:
- Push result:
- Request for architect/PM acceptance:
- Recommended next goal:
```

```text
P0-P7 final report:
- Overall status:
- Accepted phases:
- Release baseline:
- Core workflows:
- Packaging status:
- Expansion roadmap:
- Deferred work:
- Validation summary:
- Final pushed commit:
- Recommended next goal:
```
