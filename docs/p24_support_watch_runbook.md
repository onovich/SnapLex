# P24 Support Watch Runbook

Date: 2026-07-17
Phase: P24 Non-Signing Private Trial Candidate Readiness And Feedback Watch Gate
Status: support watch runbook ready

Use this runbook while P24 keeps a non-signing private-trial candidate under
watch. The runbook covers intake, escalation, privacy screening, real-provider
support, credential package support, and unsigned trust prompt handling. It is
operational support guidance only and does not add runtime product scope.

## Support Scope

Accepted support topics:

- source checkout setup, fake source smoke, and `SmokeTrial.cmd`;
- deterministic `base` package fake smoke and no-GUI bootstrap;
- real-provider readiness checks that fail closed until a tester intentionally
  configures a provider and approves network use;
- explicit `credentials` package import, cycle, save, and check-delete smoke
  with throwaway generated values;
- Settings, History, clipboard, screen, focus, DPI, multi-monitor, and
  assistive-technology observations;
- unsigned-app trust prompts and `unsigned-private-trial` wording clarity;
- candidate documentation gaps and support-template clarity.

Out of scope for P24 support:

- signing commands, certificates, timestamp services, signed archives, signed
  binaries, installers, updaters, release feeds, or public release;
- SnapLex Cloud, OAuth, billing, hosted token broker, browser extension
  runtime, AI summary runtime, global hotkeys, provider rewrites, OCR/capture
  rewrites, or full localization;
- requests to silently add keyring support to the deterministic base package;
- raw provider key handling, keyring exports, or provider dashboard review.

## Intake Steps

1. Confirm the report uses synthetic or non-sensitive sample text.
2. Confirm lane: source, base package, credentials package, or documentation.
3. Confirm mode: fake smoke, real-provider readiness, real-provider
   translation with approved network use, clipboard, screen/OCR,
   Settings/provider setup, History, accessibility/focus, DPI/scaling,
   multi-monitor, unsigned trust prompt, or support docs.
4. Confirm environment categories without personal data:
   Windows version, display scaling, monitor count, assistive technology
   active yes/no/unknown, source commit or package label, command or screen.
5. Confirm expected result, actual result, and reproduction steps.
6. Run the privacy screen before recording a summary in project docs.
7. Classify severity and disposition in `docs/p24_feedback_watch_register.md`
   or a later support-loop register.

## Privacy Screen

Reject or request resubmission when a report includes:

- provider API keys, bearer tokens, passwords, `.env` contents, secret
  launchers, keyring exports, or credential fields;
- provider dashboard screenshots, account pages, private documents, private
  chats, customer data, or screenshots with sensitive content;
- raw logs, package outputs, local app data, config/history files, OCR caches,
  API response captures, crash dumps, certificates, private keys, timestamp
  responses, signed binaries, signing materials, or package archives;
- real names, email addresses, phone numbers, billing details, or other
  personal data unless contact is intentionally provided outside the
  repository.

Maintainers may ask for command names, exit codes, short status summaries,
package labels, environment categories, sanitized reproduction steps, and
whether the trust label was clear. Maintainers must not ask for raw secrets,
private documents, full logs, package outputs, keyring exports, certificates,
private keys, timestamp responses, signed binaries, or screenshots containing
sensitive content.

## Escalation Rules

Escalate as `S0 Blocker` and hold the affected candidate lane when:

- any support path risks storing raw credentials, personal data, private
  documents, certificates, private keys, signed binaries, package outputs, logs,
  screenshots, or signing material in git;
- the base package unexpectedly gains keyring support or fails deterministic
  fake smoke;
- a real-provider path silently falls back to fake translation while presenting
  itself as real;
- unsigned/private-trial wording makes testers believe the candidate is signed,
  public, installer-ready, updater-ready, or production-approved;
- generated package outputs, screenshots, logs, smoke data, local app data,
  OCR caches, `.env`, keyring exports, certificates, private keys, signed
  binaries, timestamp responses, or provider secrets are staged or committed.

Escalate as `S1 Critical` when:

- `Validate.cmd`, `python -m snaplex --no-gui`, `StartFakeTrial.cmd`,
  `SmokeTrial.cmd`, or `StartPackagedFakeTrial.cmd` fails in a clean local
  environment;
- `StartTrial.cmd` or `StartPackagedTrial.cmd` does not fail closed when real
  provider setup is missing;
- the credentials package cannot import the keyring backend or complete
  import/cycle/save/check-delete smoke with throwaway values;
- Settings, History, clipboard, or screen flow is unusable for private-trial
  candidate evaluation and no workaround exists;
- support instructions tell testers to share sensitive material.

Classify as `S2 Major` when the issue affects a realistic trial path but has a
safe workaround. Classify as `S3 Minor` for low-risk copy/layout/docs issues.
Classify as `S4 Question` when the report needs more reproduction detail,
privacy-safe resubmission, duplicate review, or future-scope decision.

## Real-Provider Support Gate

Real-provider support is optional and manual. Before any real-provider network
check:

1. Run or ask the tester to run `python -m snaplex --check-real-provider`.
2. Confirm the credential already exists locally through an accepted credential
   reference.
3. Confirm a human intentionally approves network use for that session.
4. Use synthetic or non-sensitive text.
5. Record only provider name, readiness category, command outcome, and
   sanitized result summary.

Do not treat fake mode as translation-quality evidence. Do not ask testers to
paste keys, provider dashboard content, or private translation text.

## Credentials Package Support Gate

The `credentials` package is explicit and private-trial only. Before using it
for support:

1. Confirm the package label says `credentials` and `unsigned-private-trial`.
2. Confirm the base package was not silently changed.
3. Run smoke with generated throwaway values only:
   `import`, `cycle`, `save`, then `check-delete`.
4. Confirm output includes only backend, reference
   `snaplex/package-credential-smoke`, mode, and PASS/FAIL status.
5. Confirm cleanup passes.
6. Restore or revalidate the base package and confirm base credential smoke
   rejects keyring as unavailable.

Do not accept keyring exports, raw credential values, provider keys, `.env`
files, local config/history files, screenshots of credential fields, or package
outputs.

## Unsigned Trust Prompt Handling

Signing remains PAUSED in P24. When a tester reports Windows trust friction,
record:

- lane and package label;
- whether the artifact was clearly labeled `unsigned-private-trial`;
- whether the tester understood it was private, unsigned, and not public
  release material;
- whether the trust prompt blocked launch or merely warned;
- a short paraphrase of the prompt, without sensitive screenshots.

If a trust prompt prevents testing, classify by impact and keep release held.
Do not change Windows security policy or run signing commands unless a later
planner-approved signing phase supplies every unblock input.

## Closure Checklist

Before closing a support item, confirm:

- privacy screen passed or the report was resubmitted safely;
- lane, mode, environment categories, expected result, actual result, and
  reproduction steps are clear;
- deterministic no-network reproduction was attempted first when applicable;
- any real-provider check was explicitly approved and did not reveal secrets;
- credential smoke, if used, cleaned up throwaway values;
- no package outputs, screenshots, logs, local app data, smoke data, keyring
  exports, certificates, private keys, `.env` files, OCR caches, tester
  personal data, provider secrets, signed binaries, timestamp responses, or
  signing materials were staged or committed.

## Round 4 Self-Checks

Debug self-check:

- The runbook covers intake, escalation, privacy screen, real-provider gate,
  credential package gate, unsigned trust prompt handling, and closure.
- Success, expected rejection, no-feedback, late-feedback, cleanup,
  unsupported, no-network, no-signing, no-artifact, and no-secret states are
  covered.

Architecture self-check:

- Support guidance keeps provider, credential, settings, packaging, and
  trial-readiness boundaries separated.
- The base package remains deterministic and keyring-free.
- The credentials package remains explicit/private-trial.
- No signing, public release, installer, updater, release feed, cloud/account,
  browser, AI summary, hotkey, broad runtime feature, certificate, private key,
  signed artifact, timestamp response, or signing log is introduced.
