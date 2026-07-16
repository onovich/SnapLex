# P19 Signed Archive Candidate Decision

Date: 2026-07-17
Phase: P19 Signing Rehearsal And Signed Archive Candidate Gate
Status: not ready for signed archive candidate; ready for later approved
signing rehearsal gate

P19 decides whether signed archive candidate work can proceed. Because no
approved safe throwaway/test signing path was supplied and no signing rehearsal
was run, P19 does not approve a signed archive candidate.

## Decision

Signed archive candidate decision:

- NOT READY to produce or transfer a signed archive candidate.
- NOT READY for production signing.
- NOT READY for public release.
- NOT READY for installer or updater runtime.
- READY to preserve unsigned/private-trial archive planning.
- READY to proceed to a later isolated signing rehearsal gate only if safe
  signing-path approval is supplied.

## Evidence Supporting The Decision

P19 has recorded:

- accepted P18 baseline and P19 rebaseline;
- signing path decision as SKIPPED;
- deterministic base package control evidence;
- explicit credentials package candidate evidence;
- signing rehearsal evidence as SKIPPED;
- signature verification, trust, timestamp, and evidence policy;
- signed archive stop conditions, cleanup, rollback, and support
  implications.

Package lane evidence remains green:

- base package builds and fake smoke passes;
- packaged real trial fails closed when no real provider is configured;
- base credential smoke rejects keyring as unavailable;
- credentials variant builds explicitly and discovers WinVault keyring backend;
- credentials import/cycle/save/check-delete smoke passes and cleanup passes;
- local `dist\SnapLex` was restored to base after credentials smoke.

## Candidate Blockers

P19 blocks signed archive candidate promotion because:

- no approved safe throwaway/test signing path exists;
- no signing command was run;
- no signed artifact exists;
- no signature verification output exists;
- no timestamp policy execution exists;
- no production signing identity or certificate custody execution path exists;
- no installer, updater, release feed, public support channel, or public
  release gate exists;
- no external P19 tester feedback or real-provider network smoke was supplied.

These blockers are expected and do not fail P19 as a gate when recorded
honestly and validation remains green.

## Allowed Next Work

Allowed after P19, pending planner acceptance:

- keep unsigned/private-trial archive policies available;
- run a later isolated signing rehearsal only with explicit safe-path approval;
- continue package lane validation and no-secret boundary scans;
- collect no-secret tester feedback for credential package behavior;
- keep real-provider smoke optional and human-approved only.

## Still Not Allowed

P19 does not approve:

- public release;
- production certificate purchase, import, custody execution, or use;
- committed certificates, private keys, signed binaries, package outputs,
  timestamp responses, screenshots, logs, `.env`, keyring exports, tester data,
  local app data, smoke data, OCR caches, or provider secrets;
- installer runtime, updater runtime, release feed, or auto-update behavior;
- silent keyring support in the base package;
- SnapLex Cloud, OAuth, billing, hosted token broker, browser extension
  runtime, AI summary runtime, global hotkeys, broad provider/OCR/capture
  rewrites, or full localization.

## Recommended Next Phase

Recommended P20: approved signing path acquisition and isolated signing
rehearsal setup gate, or planner-side decision to pause signing work until a
safe test-signing path is available.

P20 should not proceed into signing commands unless it first records explicit
safe-path approval and an ignored local artifact directory.

## Round 8 Self-Checks

Debug self-check:

- The decision is explained by the smallest candidate gate workflow: signing
  path is SKIPPED, no signed artifact exists, so signed archive candidate is
  blocked while package lanes remain validated.
- Success, expected rejection, skipped signing, no signed artifact, no
  timestamp, no tester feedback, cleanup, and no-secret states are covered.

Architecture self-check:

- Candidate decision does not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
