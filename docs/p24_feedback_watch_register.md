# P24 Feedback Watch Register

Date: 2026-07-17
Phase: P24 Non-Signing Private Trial Candidate Readiness And Feedback Watch Gate
Status: watch active; no external feedback supplied

P24 keeps a privacy-safe feedback watch for late private-trial feedback while
the non-signing candidate readiness package is prepared. This register does not
store raw tester payloads. It records whether feedback arrived, how it was
screened, and what action is safe inside the current non-signing phase.

## Sources Checked

Round 3 checked these available sources:

- current P24 planner dispatch in this Codex task;
- `docs/p23_final_validation_report.md`;
- `docs/p23_to_p24_handoff.md`;
- `docs/p24_unsigned_candidate_readiness.md`;
- `docs/p24_todo.md`;
- `docs/p24_non_signing_private_trial_candidate_readiness_feedback_watch_goal_guide.md`.

Result:

- no external P24 tester report was supplied;
- no support message was supplied;
- no sanitized reproduction was supplied;
- no screenshot, log, package output, `.env` file, keyring export, local app
  data, OCR cache, provider secret, certificate, private key, signed binary,
  timestamp response, signing log, or tester personal data was supplied.

## Watch Register

| ID | Source | Privacy result | Severity | Disposition | Next action |
| --- | --- | --- | --- | --- | --- |
| P24-FB-000 | P24 intake/watch inventory | PASS; no payload supplied | none | no-feedback-to-date | Keep watch active and continue candidate readiness validation. |

No S0 blocker, S1 critical issue, S2 major issue, S3 minor issue, or S4
question was opened from external P24 feedback in Round 3.

## Privacy Screen For Late Feedback

Late feedback can be recorded only after it passes this screen:

- no provider API keys, bearer tokens, passwords, `.env` contents, secret
  launchers, or keyring exports;
- no provider dashboard screenshots, account pages, private documents, private
  chats, customer data, or screenshots with sensitive content;
- no raw logs, package outputs, local app data, config/history files, OCR
  caches, API response captures, crash dumps, certificates, private keys,
  timestamp responses, signed binaries, or signing material;
- no real names, email addresses, phone numbers, billing details, or other
  personal data unless the tester intentionally provides contact information
  outside the repository;
- real-provider network use, if any, was intentionally approved by a human for
  that session.

If a report includes sensitive material, discard the sensitive copy from the
project record, do not quote it in docs, and request a sanitized resubmission
using synthetic text.

## Late Feedback Routing

When feedback arrives, record only:

- lane: source, base package, credentials package, or documentation;
- mode: fake smoke, real-provider readiness, real-provider translation with
  approved network use, clipboard, screen/OCR, Settings/provider setup,
  History, accessibility/focus, DPI/scaling, multi-monitor, unsigned trust
  prompt, or support docs;
- Windows environment categories without personal data;
- expected result and actual result;
- sanitized reproduction steps;
- privacy screen outcome;
- severity and disposition.

Do not record raw secrets, raw logs, package outputs, sensitive screenshots,
provider dashboard content, keyring exports, local app data, OCR caches,
certificates, private keys, signed binaries, timestamp responses, or personal
tester data.

## Severity Rules

Use the current private-trial severity model:

- `S0 Blocker`: secret/privacy leak risk, validation failure, base package
  drift, fake/real confusion, unsafe support intake, or signed/public-release
  confusion.
- `S1 Critical`: core private-trial workflow failure in source, base package,
  credentials package, Settings, History, clipboard, screen, provider
  readiness, or credential smoke.
- `S2 Major`: realistic trial friction with a safe workaround, such as DPI,
  multi-monitor, assistive technology, provider setup, or trust-prompt
  confusion.
- `S3 Minor`: low-risk copy, layout, typo, or documentation issue.
- `S4 Question`: needs reproduction details, privacy-safe resubmission,
  duplicate review, or future-scope decision.

## Watch Boundaries

- Signing remains PAUSED.
- P24 does not run signing commands, create/import/purchase/invent/use
  certificates, call timestamp services, or produce signed artifacts.
- The base package must remain deterministic and keyring-free.
- The credentials package remains explicit and private-trial only.
- Optional real-provider smoke requires existing local credentials and explicit
  human network approval.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.

## Round 3 Self-Checks

Debug self-check:

- The watch register is explained by the smallest P24 support workflow:
  inventory available feedback sources, record no-feedback honestly, define
  privacy screening, define late-feedback routing, and keep watch active.
- Success, no-feedback, late-feedback, reject/resubmit, unsupported,
  no-network, no-signing, no-artifact, and no-secret states are covered.

Architecture self-check:

- The register changes only support/watch documentation.
- It does not change provider, credential, settings, history, capture, OCR, UI,
  package specification, or trial readiness behavior.
- The base package remains deterministic and keyring-free.
- The credentials package remains explicit/private-trial.
- No signing, public release, installer, updater, release feed, cloud/account,
  browser, AI summary, hotkey, broad runtime feature, certificate, private key,
  signed artifact, timestamp response, or signing log is introduced.
