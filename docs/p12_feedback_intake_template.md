# P12 Feedback Intake Template And Triage Taxonomy

Date: 2026-07-16
Phase: P12 Private Trial Pilot And Feedback Triage
Status: ready for private-trial intake

Use this template for first private-trial feedback. Keep reports concise,
synthetic, and privacy-safe.

## Privacy Rules

Do not paste or attach:

- provider API keys, bearer tokens, `.env` files, keyring exports, or local
  launchers containing secrets;
- private documents, private chats, account dashboards, customer data, or
  screenshots that show sensitive content;
- raw logs, package outputs, local app data, config/history files, OCR caches,
  or API response captures;
- real names, email addresses, phone numbers, or other personal data unless a
  tester intentionally provides them outside the repository for follow-up.

Use synthetic sample text such as `hello`, `invoice total`, or `screen hello`.
If a screenshot is needed, reproduce the issue with non-sensitive text first.

## Feedback Report Template

Copy this block for each issue:

```text
Title:

Category:
- [ ] Bug
- [ ] Usability
- [ ] Translation quality
- [ ] Credential setup
- [ ] Provider onboarding
- [ ] Packaging/install
- [ ] Accessibility
- [ ] DPI/scaling
- [ ] Multi-monitor
- [ ] Performance/responsiveness
- [ ] Documentation
- [ ] Other:

Mode:
- [ ] Source checkout
- [ ] Packaged base build
- [ ] Fake smoke mode
- [ ] Real provider mode
- [ ] Settings
- [ ] History
- [ ] Clipboard flow
- [ ] Screen flow

Environment:
- Windows version:
- Display scaling:
- Monitor count:
- Assistive technology active? yes/no/unknown
- SnapLex version or commit:
- Command used:

Expected result:

Actual result:

Synthetic sample text used:

Steps to reproduce:
1.
2.
3.

Does this block the first private pilot?
- [ ] Yes, cannot continue trial
- [ ] No, but should fix before wider trial
- [ ] No, can defer
- [ ] Unsure

Privacy check:
- [ ] No API keys, bearer tokens, `.env` files, keyring exports, or local
      launchers are included.
- [ ] No private documents, private chats, customer data, or sensitive
      screenshots are included.
- [ ] No raw logs, package outputs, local app data, config/history files, OCR
      caches, or API response captures are included.
- [ ] Any screenshot uses synthetic/non-sensitive text.
```

## Triage Taxonomy

Use this taxonomy when reviewing feedback.

### Severity

- `S0 Blocker`: prevents launch, bootstrap, fake smoke, or safe feedback intake.
- `S1 Critical`: breaks a core private-trial workflow such as clipboard,
  Settings, History, packaged fake smoke, or real-trial fail-closed behavior.
- `S2 Major`: confusing or unreliable but has a clear workaround.
- `S3 Minor`: cosmetic, copy, layout, or documentation issue with low pilot
  risk.
- `S4 Question`: unclear report, needs reproduction details, or belongs to a
  future product decision.

### Disposition

- `fix-now`: must be repaired before the first private pilot continues.
- `investigate`: needs reproduction, environment details, or a focused smoke.
- `defer`: valid issue, but not blocking this private pilot.
- `reject`: outside P12 scope, already documented limitation, duplicate, or not
  actionable with privacy-safe evidence.

### Category Routing

- Bug: map to the affected layer, such as CLI/bootstrap, trial script, package
  smoke, GUI shell, Settings, History, clipboard, screen flow, provider
  readiness, credential readiness, or documentation.
- Usability: check whether release notes, labels, focus order, or workflow
  sequence are unclear.
- Translation quality: accept only real-provider reports that use non-sensitive
  text and state which provider was intentionally used. Fake mode is not
  translation quality evidence.
- Credential setup: verify whether the report concerns environment variables,
  source keyring setup, missing optional `keyring`, or unsupported packaged
  keyring expectations.
- Packaging/install: classify base package fake smoke separately from optional
  capture/OCR variants or future credential-capable packages.
- Accessibility/DPI/multi-monitor: preserve device details, but do not attach
  sensitive screenshots.
- Provider onboarding: check whether the tester confused fake smoke, real
  provider readiness, `Test Connection`, key rotation, or fail-closed behavior.

## First-Response Checklist

Before moving a report into `fix-now` or `investigate`, confirm:

- The report uses privacy-safe synthetic data.
- The affected mode is clear: source, package, fake, real provider, Settings,
  History, clipboard, or screen.
- Expected and actual results are stated.
- The report can be reproduced without real provider credentials or network
  unless it is explicitly marked as optional real-provider smoke.
- The issue is not already listed in known limitations from
  `docs/p12_private_trial_release_notes.md`.

## Rejection Reasons

Use `reject` only with a short reason:

- duplicate of an existing report;
- outside P12 scope, such as cloud accounts, OAuth, billing, browser extension,
  AI summary runtime, global hotkeys, full localization, provider rewrites, or
  OCR/capture rewrites;
- contains secrets or personal data and must be resubmitted safely;
- asks for packaged keyring support, which is not promised in P12;
- relies on fake mode as translation quality evidence.
