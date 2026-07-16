# P12 To P13 Handoff

Date: 2026-07-16
Status: P12 planner-accepted; P13 ready for execution

Selected next phase: P13 Private Trial Feedback Response And Credential
Package Feasibility.

P12 final validation report: `docs/p12_final_validation_report.md`
P12 private trial release notes: `docs/p12_private_trial_release_notes.md`
P12 feedback intake template: `docs/p12_feedback_intake_template.md`
P12 triage workflow: `docs/p12_trial_triage_workflow.md`
P13 execution guide:
`docs/p13_private_trial_feedback_response_credential_package_feasibility_goal_guide.md`
P13 TODO: `docs/p13_todo.md`

## Accepted Input And Executor Baseline

P12 started from planner-accepted P11 at
`66d3cef11db492b6c6170c26b69e483528186767`.

P12 implementation and closure commits through
`1b5c690b4c974c254b9d45d63a78ec4b11a4d583` are pushed to `origin/main`.
Planner recheck accepted P12 on 2026-07-16.

## What P12 Leaves Stable

- P10 credential boundaries remain intact: providers, provider setup, Test
  Connection, trial readiness, SettingsService, and SettingsPresenter resolve
  credentials through service/store boundaries.
- UI widgets remain clients of presenter/service boundaries and do not own
  provider or secret business rules.
- Fake source/package smoke remains deterministic and visibly fake.
- Real source/package trial paths reject missing real-provider configuration
  instead of falling back to fake translation.
- Automated validation remains no-network and does not require real provider
  credentials, real OS keyring state, screen permissions, model downloads, or
  tester devices.
- Generated screenshots, package outputs, smoke app data, pytest temp data,
  `.env`, logs, keyring exports, OCR caches, tester personal data, and provider
  secrets remain untracked.

## Private-Trial Materials

- `docs/p12_private_trial_release_notes.md`: tester-facing pilot brief, trial
  paths, known limitations, privacy warnings, and baseline validation evidence.
- `docs/p12_feedback_intake_template.md`: privacy-safe report template,
  severity taxonomy, dispositions, and category routing.
- `docs/p12_trial_pass_fail_criteria.md`: pilot GO, CONDITIONAL GO, and NO-GO
  gates.
- `docs/p12_manual_environment_checks.md`: visible GUI/package/trial-script
  results plus manual AT/DPI/multi-monitor runbooks and blockers.
- `docs/p12_real_provider_smoke_decision.md`: real-provider smoke skip decision
  and future approved-manual runbook.
- `docs/p12_credential_package_variant_decision.md`: decision to defer
  credential-capable package support for the first pilot.
- `docs/p12_trial_triage_workflow.md`: maintainer workflow for privacy screen,
  classification, deterministic reproduction, disposition, and closure.
- `docs/p12_boundary_scan_evidence.md`: artifact/secret boundary evidence.

## Feedback Triage Model

P13 should use the P12 triage flow:

1. Reject or resubmit feedback containing secrets, personal data, private
   documents, sensitive screenshots, `.env` files, keyring exports, logs with
   secrets, package outputs, OCR caches, local app data, or provider response
   captures.
2. Classify one primary area: launch/install, package smoke, fake trial, real
   trial readiness, provider onboarding, credential setup, translation quality,
   OCR/capture behavior, Settings, History, accessibility/focus, DPI,
   multi-monitor, performance/responsiveness, documentation, or repository
   hygiene.
3. Assign severity and disposition using
   `docs/p12_trial_pass_fail_criteria.md`.
4. Reproduce with deterministic no-network commands first.
5. Run real-provider smoke only with existing local credentials and explicit
   human approval.
6. Close each item with command/manual evidence and artifact/secret hygiene.

## Manual Validation Results And Blockers

Recorded P12 results:

- visible GUI smoke: PASS;
- packaged fake smoke: PASS;
- source fake trial: PASS;
- source real trial fail-closed: PASS;
- packaged fake trial: PASS;
- packaged real trial fail-closed: PASS;
- assistive technology: NOT RUN, requires tester hardware/tooling;
- DPI scaling: NOT RUN, requires manual display scaling review;
- multi-monitor behavior: NOT RUN, requires multi-monitor hardware.

These manual blockers are acceptable for P12 pilot preparation but should be
tracked during the first tester sessions.

## Credential Package Decision

P12 defers a credential-capable package variant. Keep the first pilot paths as:

- deterministic base package for fake smoke and package confidence;
- environment variables for optional real-provider source/package trial;
- source checkout plus `.[gui,credentials]` for local secure credential testing
  when optional `keyring` support is installed;
- no packaged keyring support promise until a later explicit phase validates it
  with throwaway credentials from the packaged executable.

## Known Trial Gaps

- No real-provider network smoke was run in P12.
- Optional `keyring` is missing in the executor environment, so Windows
  Credential Locker smoke remains blocked.
- Assistive technology, DPI scaling, and multi-monitor validation remain manual.
- Base package does not promise secure local credential/keyring support.
- Fake mode is smoke/dev output only and cannot validate translation quality.
- Global hotkeys, browser extension runtime, AI summary runtime, full
  localization, cloud accounts, OAuth, billing, hosted token broker, provider
  rewrites, and OCR/capture rewrites remain out of scope.

## Selected P13 Scope

Selected P13: run the first private-trial feedback response loop and decide
credential-package feasibility.

Suggested P13 deliverables:

- private-trial feedback log using the P12 template;
- S0/S1 blocker fixes, if any, with deterministic validation;
- assistive technology, DPI, and multi-monitor manual results or blockers;
- one optional real-provider smoke record only if credentials and explicit
  network approval exist;
- manual keyring smoke from source when optional `keyring` can be installed;
- credential-capable package feasibility decision with a go/no-go prototype only
  if architect-approved;
- P13 final report and P13-to-P14 handoff.

## Validation To Preserve

- `Validate.cmd` full validation.
- `git diff --check`.
- `python -m snaplex --version`.
- `python -m snaplex --no-gui`.
- `python -m snaplex --check-real-provider` expected rejection when no real
  provider is configured.
- `python scripts\package_windows.py --dry-run --variant base`.
- `cmd /c StartTrial.cmd --no-gui` expected rejection.
- `cmd /c StartFakeTrial.cmd --no-gui`.
- `cmd /c SmokeTrial.cmd`.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`.
- `cmd /c StartPackagedTrial.cmd --no-gui` expected rejection.
- `python scripts\p9_gui_smoke.py`.
- `python scripts\p11_visible_gui_smoke.py`.
- P12 docs link/index check.
- Artifact/secret boundary scan.

## Explicit Non-Scope

- Production SnapLex Cloud.
- Account OAuth, billing, remote accounts, hosted token broker, or cloud sync.
- Browser extension runtime.
- AI summary runtime.
- Global hotkeys.
- Provider rewrites unrelated to accepted feedback blockers.
- OCR/capture rewrites unrelated to accepted feedback blockers.
- Full localization implementation.
- Automated validation requiring real provider credentials, network calls, real
  OS keyring state, screen permissions, model downloads, or tester devices.
- Committed screenshots, package outputs, local app data, `.env`, provider
  secrets, keyring exports, logs, OCR model caches, tester personal data, smoke
  data, or provider response captures.
