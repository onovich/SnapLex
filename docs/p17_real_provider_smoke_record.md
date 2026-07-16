# P17 Real Provider Smoke Record

Date: 2026-07-17
Phase: P17 Limited Credential Package Pilot And Signing Decision
Status: optional real-provider smoke skipped; fail-closed readiness PASS

P17 keeps automated validation no-network. Real-provider translation smoke is
manual and optional only when local credentials already exist and a human
explicitly approves network use in the executor session.

## Decision

Real-provider network smoke was not run in this P17 executor session.

Reason:

- no explicit human approval for network use was supplied in this session;
- no tester-provided real-provider smoke report was supplied;
- P17 automated validation must remain deterministic and no-network.

This is an honest skip, not a failure. P17 relies on fail-closed readiness and
package credential smoke for deterministic evidence.

## Fail-Closed Evidence

Commands and results:

- `python -m snaplex --check-real-provider`: expected rejection PASS with
  `Real translation provider is not configured.`
- `cmd /c StartTrial.cmd --no-gui`: expected rejection PASS with
  `Real translation provider is not configured.`

No provider API request was made by these readiness checks.

## Conditions Required To Run Later

Optional real-provider smoke may run later only when all are true:

- local credentials already exist outside the repository;
- a human explicitly approves provider network use for that session;
- the smoke uses non-sensitive sample text;
- output and reports omit API keys, bearer tokens, `.env` contents, keyring
  exports, provider dashboard screenshots, private source text, translated
  private text, raw API responses, and logs with secrets;
- failure evidence records status categories only.

If any condition is missing, keep this smoke skipped and rely on fail-closed
readiness.

## Accepted Evidence Shape

If a later approved run occurs, record only:

- provider name;
- credential source type, such as environment variable or local secure
  credential;
- readiness category;
- command status;
- connection or translation pass/fail category using synthetic text;
- whether cleanup was required.

Never record raw provider secrets, translated private text, provider response
payloads, or screenshots containing sensitive information.

## Round 5 Self-Checks

Debug self-check:

- The current result is explained by the smallest real-provider workflow:
  readiness check, trial command expected rejection, no approval, and skipped
  network.
- Success criteria, expected rejection, skipped network, no tester feedback,
  and no-secret states are covered.

Architecture self-check:

- Provider readiness remains behind trial readiness/provider setup boundaries.
- Translation execution remains behind provider registry and
  `TranslationPipeline`; P17 does not call providers directly from docs or UI.
- Credential behavior remains behind `CredentialService` and stores.
- No network-required automated test, cloud/OAuth/account/billing/token broker,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, or full localization scope is added.
