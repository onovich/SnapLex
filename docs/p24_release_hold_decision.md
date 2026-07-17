# P24 Release Hold Decision

Date: 2026-07-17
Phase: P24 Non-Signing Private Trial Candidate Readiness And Feedback Watch Gate
Status: support-ready for non-signing private-trial watch; release held

This decision records the P24 candidate support posture after the unsigned
candidate readiness record, feedback watch register, support watch runbook, base
package candidate evidence, and explicit credentials package candidate evidence
were refreshed.

## Decision Summary

| Decision area | P24 result | Notes |
| --- | --- | --- |
| Non-signing private-trial watch | CONTINUE | The source, base, and credentials lanes have enough documentation and support evidence to remain under private-trial watch. |
| Support readiness | READY WITH HOLD CONDITIONS | Support may continue through privacy-safe intake, sanitized reproduction steps, and deterministic/fake validation paths. |
| External feedback | NONE SUPPLIED | `docs/p24_feedback_watch_register.md` records `P24-FB-000` as no-feedback-to-date. No tester report was fabricated. |
| Base package lane | SUPPORT-READY | Round 5 revalidated base dry-run, base build, source fake smoke, packaged fake smoke, fail-closed real-provider paths, and expected credential-smoke rejection. |
| Credentials package lane | SUPPORT-READY AS EXPLICIT PRIVATE-TRIAL LANE | Round 6 revalidated credentials dry-run/build plus throwaway import/cycle/save/check-delete, then restored the base package and reconfirmed base keyring rejection. |
| Signing | PAUSED | P24 does not run signing commands or approve signing rehearsal. |
| Public release | NOT APPROVED | P24 is not a public release, installer, updater, signed archive, or release-feed phase. |
| Real-provider smoke | NOT RUN | Requires existing local credentials and explicit human network approval. No such approval was supplied. |
| Immediate repair | NONE IDENTIFIED BEFORE FINAL SCANS | Continue to Round 8 boundary scans and Round 10 final validation before READY_FOR_CHECK. |

## Why Support Watch May Continue

P24 may continue the non-signing private-trial watch because:

- `docs/p24_unsigned_candidate_readiness.md` labels the candidate as
  `unsigned-private-trial`, defines source/base/credentials lanes, and keeps
  signing/public release on hold;
- `docs/p24_feedback_watch_register.md` records no external tester feedback
  supplied and defines privacy-safe handling for late feedback;
- `docs/p24_support_watch_runbook.md` gives support routing for unsigned trust
  prompts, package lane issues, fake smoke, expected fail-closed real-provider
  paths, and explicit credentials package checks;
- `docs/p24_base_package_candidate_evidence.md` confirms the deterministic base
  package lane remains keyring-free and rejects credential smoke as expected;
- `docs/p24_credentials_package_candidate_evidence.md` confirms the explicit
  credentials package lane can use throwaway package credential smoke and that
  the base package is restored afterward.

## Why Release Remains Held

The candidate remains held because:

- signing is still PAUSED and P24 is not authorized to run signing commands;
- no certificate, private key, timestamp service, signed binary, signed archive,
  installer, updater, release feed, or public release approval exists;
- no external tester feedback has been supplied, so there is no field evidence
  justifying a broader release decision;
- no real-provider smoke was run because no local credentials and explicit human
  network approval were supplied;
- Round 8 boundary/artifact/secret/signing-material scans and Round 10 final
  validation are still required before the executor can return
  `READY_FOR_CHECK`.

## Hold Conditions

Keep the candidate on hold, or hold the affected lane, if any of these occur:

- deterministic validation, fake source smoke, packaged fake smoke, no-GUI
  bootstrap, or package dry-run fails;
- a real-provider path silently falls back to fake as if it were real
  translation;
- the base package imports keyring support or accepts credential smoke;
- the credentials package cannot complete throwaway import/cycle/save/
  check-delete when that lane is under consideration;
- feedback intake includes secrets, raw logs, sensitive screenshots, keyring
  exports, package outputs, local app data, tester personal data, certificates,
  private keys, signed binaries, timestamp responses, or provider secrets;
- nonignored generated artifacts, screenshots, logs, package outputs, smoke
  data, OCR caches, `.env`, signing material, keyring exports, or secrets are
  staged or committed;
- unsigned/private-trial wording implies the candidate is signed, public,
  installer-ready, updater-ready, release-feed-ready, or production-approved.

## Allowed Next Support Actions

Allowed while release remains held:

- continue privacy-safe support intake using the P24 watch register and support
  runbook;
- keep validating deterministic base package and explicit credentials package
  lanes with no-network, throwaway-value smoke paths;
- record no-feedback honestly unless sanitized external feedback is actually
  supplied;
- prepare P24 final validation and P25 handoff after scans and final validation
  pass.

Not allowed in P24:

- signing commands, certificate creation/import/purchase/use, timestamp calls,
  signed archives, signed binaries, installers, updaters, release feeds, or
  public release;
- SnapLex Cloud, OAuth, billing, hosted token broker, browser extension runtime,
  AI summary runtime, global hotkeys, broad provider/OCR/capture rewrites, full
  localization, or silent keyring support in the base package.

## Round 7 Self-Checks

Debug self-check:

- The decision is explained by the smallest evidence chain: readiness docs and
  package lane evidence support continued private-trial watch, while absent
  signing inputs, absent external feedback, absent real-provider approval, and
  pending final scans keep release held.
- Success, expected rejection, no-feedback, late-feedback, cleanup,
  unsupported, no-network, no-signing, no-artifact, and no-secret states remain
  explicitly covered.

Architecture self-check:

- This document changes only release/support evidence.
- Provider execution remains behind the provider registry and
  `TranslationPipeline`.
- Credential behavior remains behind credential services/stores, settings,
  provider setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The credentials package remains explicit/private-trial.
- No signing, public release, installer, updater, release feed, cloud/account,
  browser, AI summary, hotkey, broad runtime feature, certificate, private key,
  signed artifact, timestamp response, or signing log is introduced.
