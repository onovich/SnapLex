# P12 Trial Triage Workflow

Date: 2026-07-16
Phase: P12 Private Trial Pilot And Feedback Triage
Status: private-trial triage workflow

Use this workflow when a private-trial tester reports an issue, concern, or
translation-quality observation. P12 triage is operational: it classifies and
routes feedback while preserving the accepted P11/P10 runtime and credential
boundaries.

## Intake Sources

Accepted intake formats:

- completed entries from `docs/p12_feedback_intake_template.md`;
- short tester notes copied into an issue or local triage note after privacy
  review;
- maintainer-run smoke evidence from `docs/p12_manual_environment_checks.md`;
- optional real-provider smoke notes only when local credentials already exist
  and a human intentionally approved network use.

Do not accept raw API keys, `.env` files, keyring exports, provider account
screenshots, private documents, sensitive screenshots, personal data, local app
data directories, logs that may contain secrets, package outputs, OCR caches, or
credential values. Ask the tester to resubmit a scrubbed report when needed.

## Triage Steps

1. Privacy screen.

   Confirm the report contains no provider secrets, personal data, private
   documents, sensitive screenshots, ignored local artifacts, package binaries,
   OCR caches, logs with secrets, `.env` content, or keyring exports. If it does,
   discard the sensitive material and request a sanitized report.

2. Classify the area.

   Use one primary area: launch/install, package smoke, fake trial, real trial
   readiness, provider onboarding, credential setup, translation quality, OCR or
   capture behavior, Settings, History, accessibility/focus, DPI, multi-monitor,
   performance/responsiveness, documentation, or repository hygiene.

3. Assign severity.

   Use the definitions in `docs/p12_trial_pass_fail_criteria.md`: blocker,
   must-fix, investigate, defer, or reject/resubmit.

4. Reproduce deterministically first.

   Start with no-network paths: `Validate.cmd`, `python -m snaplex --no-gui`,
   `StartFakeTrial.cmd --no-gui`, `SmokeTrial.cmd`, or
   `StartPackagedFakeTrial.cmd --no-gui`. Use a local
   `SNAPLEX_APP_DATA_DIR` override for GUI and package smoke.

5. Gate real-provider checks.

   Run `python -m snaplex --check-real-provider` before any real-provider
   launch. Run `StartTrial.cmd` or `StartPackagedTrial.cmd` only when a local
   credential already exists and a human intentionally approves the provider
   network call. Never use real-provider smoke as an automated requirement.

6. Decide disposition.

   Apply one disposition: fix-now, investigate, defer, reject/resubmit, or
   accepted limitation. Link the decision to the pass/fail criteria and any
   smoke evidence used.

7. Close with evidence.

   Record the command or manual check used, the outcome, and any remaining
   limitation. Confirm no generated artifact, screenshot, package output, local
   app data, tester data, log, keyring export, `.env`, OCR cache, or secret was
   staged.

## Disposition Guide

- `fix-now`: blocks launch, fails closed-path safety, leaks secrets, corrupts
  config/history, breaks deterministic fake/package smoke, or makes the primary
  trial flow unusable.
- `investigate`: credible but not yet reproduced, environment-specific, or
  depends on manual DPI, multi-monitor, assistive technology, provider, or OS
  keyring behavior.
- `defer`: valuable product work outside P12, such as global hotkeys, full
  localization, browser extension runtime, AI summary runtime, provider
  rewrites, capture/OCR rewrites, or SnapLex Cloud.
- `reject/resubmit`: report contains sensitive material, lacks enough
  reproduction detail, or asks P12 to accept a boundary-breaking implementation.
- `accepted limitation`: already documented in P12 release notes, pass/fail
  criteria, real-provider smoke decision, manual environment checks, or
  credential package decision.

## Required Cross-Checks

Before calling the private pilot ready, verify these documents point to one
another and stay consistent:

- `docs/p12_private_trial_release_notes.md`
- `docs/p12_feedback_intake_template.md`
- `docs/p12_trial_pass_fail_criteria.md`
- `docs/p12_manual_environment_checks.md`
- `docs/p12_real_provider_smoke_decision.md`
- `docs/p12_credential_package_variant_decision.md`
- `docs/p12_trial_triage_workflow.md`
- `docs/p12_boundary_scan_evidence.md`
- `docs/p11_private_trial_release_checklist.md`
- `docs/p11_provider_onboarding_notes.md`
- `docs/windows_smoke_checklist.md`

## Boundary Reminder

P12 does not implement production SnapLex Cloud, account OAuth, billing, hosted
token broker, browser extension runtime, AI summary runtime, global hotkeys,
provider rewrites, OCR/capture rewrites, full localization, or a
credential-capable package variant. It prepares private-trial operations and
feedback triage from the accepted P11 runtime baseline.
