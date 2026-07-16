# P18 Distribution Readiness Decision

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Status: conditionally ready for a later signing gate; not ready for public
release

P18 evaluates whether SnapLex can move beyond the unsigned private-trial
credential package lane. The decision is conservative: SnapLex is ready to
continue controlled private-trial archive handling and to enter a later signing
rehearsal or signed-candidate gate, but it is not ready for public release,
installer distribution, automatic updates, or broad signed distribution.

## Decision

Distribution readiness decision:

- READY to keep the deterministic `base` archive lane as the control path.
- READY to keep the explicit `credentials` archive lane as private-trial only.
- READY to proceed to a later signing/distribution gate that can supply an
  approved signing identity, custody path, and safe rehearsal environment.
- NOT READY for public release.
- NOT READY for signed production distribution.
- NOT READY for installer or updater runtime.
- NOT READY to merge keyring support into the base package.

## Evidence Supporting Conditional Readiness

P18 has recorded:

- accepted P17 baseline and P18 revalidation;
- signing identity and certificate custody policy;
- signing command, verification, evidence, and revocation expectations;
- explicit SKIPPED signing rehearsal record;
- archive-versus-installer decision;
- rollback and update policy without updater runtime;
- artifact naming, transfer, retention, revocation, and support escalation
  policy.

The repository continues to preserve:

- deterministic no-network automated validation;
- base package keyring-free behavior;
- explicit `credentials` package variant behavior;
- fail-closed real-provider readiness when credentials are missing;
- no-secret, no-artifact, no-package-output repository hygiene.

## Distribution Blockers

Broader signed distribution remains blocked by:

- no approved production signing identity;
- no approved certificate custody execution path;
- no safe signing rehearsal run in P18;
- no signed artifact verification evidence;
- no installer technology or uninstall behavior;
- no updater, release feed, or rollback automation;
- no public support channel;
- no external P18 tester feedback supplied;
- no real-provider network smoke approved in this executor round;
- limited device evidence for locked Credential Locker, enterprise-managed
  policy, unsupported backend, and remote-session keyring behavior.

These blockers do not prevent P18 from passing as a readiness gate if the final
validation matrix remains green and no forbidden artifacts or secrets enter
git.

## Allowed After P18

Allowed after P18, pending final validation and planner acceptance:

- continue documentation-first signing/distribution planning;
- run an isolated signing rehearsal only when a safe throwaway/test path is
  explicitly approved;
- keep private-trial archive transfer policy available for future candidates;
- collect no-secret tester feedback for credential package behavior;
- preserve base and credentials package smoke lanes.

## Still Not Allowed

P18 does not approve:

- public release;
- production signing with an invented or unapproved certificate;
- committed certificates, private keys, signed artifacts, package outputs,
  logs, screenshots, `.env` files, keyring exports, tester data, or provider
  secrets;
- installer/updater runtime;
- silent keyring support in the base package;
- SnapLex Cloud, account OAuth, billing, hosted token broker, remote accounts,
  cloud sync, browser extension runtime, AI summary runtime, global hotkeys,
  broad provider rewrites, OCR/capture rewrites, or full localization.

## Recommended Next Phase

Recommended P19: signing rehearsal and signed archive candidate gate.

P19 should be approved only if it keeps signing isolated from runtime business
rules, uses throwaway/test signing material unless a production certificate is
explicitly approved, preserves base and credentials package separation, and
continues no-secret/no-artifact repository hygiene.

## Round 8 Self-Checks

Debug self-check:

- The decision is explained by the smallest distribution workflow: conditional
  readiness, explicit blockers, allowed next steps, and non-scope.
- Success, expected rejection, skipped signing, skipped network, no tester
  feedback, cleanup, public-release block, and no-secret states are covered.

Architecture self-check:

- Distribution policy does not move provider, credential, settings, history,
  capture, OCR, UI, or trial readiness rules into packaging.
- Provider calls stay behind provider registry and `TranslationPipeline`.
- Credential behavior stays behind credential services, stores, settings,
  provider setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, or full localization is introduced.
