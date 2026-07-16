# P22 Tester Support Intake And Escalation

Date: 2026-07-17
Phase: P22 Non-Signing Private Trial Continuity And Tester Support Gate
Status: support intake refreshed for unsigned private trial

Use this document when a private-trial tester needs help with the unsigned
SnapLex source checkout, deterministic base package, or explicit credentials
package. P22 support is operational only: it records safe evidence, routes
feedback, and keeps signing paused.

## Support Scope

Accepted support topics:

- source checkout setup, `SetupTrial.cmd`, `BuildTrial.cmd`, and `SmokeTrial.cmd`;
- deterministic fake smoke through `StartFakeTrial.cmd` and
  `StartPackagedFakeTrial.cmd`;
- real-provider readiness checks that fail closed until a tester intentionally
  configures a provider and approves network use;
- explicit credentials package import, cycle, save, and check-delete smoke;
- Settings, History, clipboard, screen, focus, DPI, multi-monitor, and
  assistive-technology observations;
- unsigned-app trust prompts and private-trial wording clarity;
- documentation gaps in the private-trial lane.

Out of scope for P22 support:

- signing commands, certificates, timestamp services, signed archives, signed
  binaries, installers, updaters, release feeds, or public release;
- SnapLex Cloud, account OAuth, billing, hosted token broker, browser extension
  runtime, AI summary runtime, global hotkeys, provider rewrites, OCR/capture
  rewrites, or full localization;
- requests to silently add keyring support to the deterministic base package.

## Privacy Screen

Before triage, confirm the report contains none of these materials:

- provider API keys, bearer tokens, passwords, `.env` files, local launchers
  containing secrets, or keyring exports;
- provider dashboard screenshots, account pages, private documents, private
  chats, customer data, or screenshots with sensitive content;
- raw logs, package outputs, local app data, config/history files, OCR caches,
  API response captures, crash dumps, certificates, private keys, timestamp
  responses, or signed binaries;
- real names, email addresses, phone numbers, billing details, or other personal
  data unless the tester intentionally provides contact information outside the
  repository.

If a report includes sensitive material, discard the sensitive copy, do not
quote it in project docs, and ask for a sanitized report using synthetic text.

## Tester Support Request Template

Ask testers to use this block when they report a problem:

```text
Title:

Lane:
- [ ] Source checkout
- [ ] Base package
- [ ] Credentials package
- [ ] Documentation only

Mode:
- [ ] Fake smoke
- [ ] Real provider readiness
- [ ] Real provider translation with approved network use
- [ ] Clipboard
- [ ] Screen/OCR
- [ ] Settings/provider setup
- [ ] History
- [ ] Accessibility/focus
- [ ] DPI/scaling
- [ ] Multi-monitor
- [ ] Unsigned-app trust prompt

Environment:
- Windows version:
- Display scaling:
- Monitor count:
- Assistive technology active? yes/no/unknown
- SnapLex version, commit, or package label:
- Command or screen used:

Expected result:

Actual result:

Synthetic sample text used:

Steps to reproduce:
1.
2.
3.

Privacy check:
- [ ] No API keys, bearer tokens, passwords, `.env` files, keyring exports, or
      secret launchers are included.
- [ ] No private documents, private chats, customer data, provider dashboards,
      or sensitive screenshots are included.
- [ ] No logs, package outputs, local app data, config/history files, OCR
      caches, certificates, private keys, timestamp responses, signed binaries,
      or API captures are included.
- [ ] Any screenshot uses synthetic/non-sensitive text.
- [ ] Real provider network use, if any, was intentionally approved by a human.
```

## Maintainer Response Rules

Maintainers may ask for:

- command names, exit codes, and short status summaries;
- package label, commit, lane, and whether the app was source, base package, or
  credentials package;
- Windows version, display scaling, monitor count, and whether assistive
  technology was active;
- sanitized reproduction steps using synthetic text;
- whether the tester saw an unsigned-app prompt and whether the trust label was
  clear.

Maintainers must not ask for:

- raw provider keys, secret values, `.env` contents, keyring exports, provider
  dashboard screenshots, or private documents;
- full logs, package outputs, generated app data, OCR caches, certificates,
  private keys, timestamp responses, signed binaries, or screenshots containing
  sensitive content;
- real-provider network tests unless the tester already has local credentials
  and explicitly approves that check for the session.

## Escalation Rules

Escalate as `S0 Blocker` and pause the affected private-trial lane when:

- any support path risks exposing or storing raw credentials, personal data,
  private documents, certificates, private keys, or signed/package artifacts in
  git;
- the base package unexpectedly gains keyring support or fails the deterministic
  fake smoke path;
- a real-provider path silently falls back to fake translation while presenting
  itself as real;
- unsigned/private-trial wording makes testers believe the package is signed,
  public, or production-approved;
- generated package outputs, screenshots, logs, smoke data, or local app data
  are staged or committed.

Escalate as `S1 Critical` when:

- `Validate.cmd`, `python -m snaplex --no-gui`, `StartFakeTrial.cmd`,
  `SmokeTrial.cmd`, or `StartPackagedFakeTrial.cmd` fails in a clean local
  environment;
- `StartTrial.cmd` or `StartPackagedTrial.cmd` does not fail closed when real
  provider setup is missing;
- the credentials package cannot import the keyring backend or complete
  cycle/save/check-delete smoke with throwaway values;
- Settings, History, clipboard, or screen flow is unusable for the private
  trial and no documented workaround exists;
- support instructions tell testers to share sensitive material.

Classify as `S2 Major` when the issue has a workaround but affects a realistic
trial path, such as DPI, multi-monitor, assistive technology, provider setup, or
trust-prompt confusion.

Classify as `S3 Minor` for copy, layout, typo, or documentation issues that do
not block safe trial use.

Classify as `S4 Question` when the report needs reproduction details, asks for
future scope, or cannot be evaluated without sensitive material.

## Real Provider Support Gate

Real-provider support is optional and manual. Before any real-provider network
check:

1. Run or ask the tester to run `python -m snaplex --check-real-provider`.
2. Confirm the provider credential already exists locally through an accepted
   credential reference.
3. Confirm the tester intentionally approves network use for that session.
4. Record only provider name, readiness category, command outcome, and sanitized
   text.

Do not treat fake mode as translation-quality evidence. Do not ask testers to
paste keys, provider dashboard content, or private translation text.

## Unsigned Trust Prompt Support

Signing remains paused in P22. When a tester reports Windows trust friction,
record:

- lane and package label;
- whether the artifact was clearly labeled `unsigned-private-trial`;
- whether the tester understood it was private, unsigned, and not public
  release material;
- a short paraphrase of the prompt or block screen, without screenshots that
  contain sensitive content.

If the trust prompt prevents testing, classify the issue by impact and keep the
signing path paused unless a later approved signing gate changes that decision.

## Closure Checklist

Before closing a support item, confirm:

- privacy screen passed or the report was resubmitted safely;
- lane, mode, environment, expected result, actual result, and reproduction
  steps are clear;
- deterministic no-network reproduction was attempted first when applicable;
- any real-provider check was explicitly approved and did not reveal secrets;
- no package outputs, screenshots, logs, local app data, keyring exports,
  certificates, private keys, `.env` files, OCR caches, tester personal data, or
  provider secrets were staged or committed.

## Round 3 Self-Checks

Debug self-check:

- Support intake covers source, base package, credentials package, real-provider
  readiness, unsigned trust prompts, and device-specific reports.
- Escalation rules identify privacy leaks, fake/real confusion, base package
  drift, package-lane failures, and unsafe support instructions as blockers.

Architecture self-check:

- The document keeps support and credential handling behind existing service,
  presenter, registry, and pipeline boundaries.
- It does not add signing, certificate, installer, updater, release feed, public
  release, or new runtime feature work to P22.
