# P18 Archive Versus Installer Readiness Decision

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Status: archive lane only; installer not ready

P18 decides whether SnapLex is ready to move from unsigned private-trial
archives toward signed distribution. The decision is to keep any P18/P19
candidate on the archive lane unless a later gate explicitly approves installer
work.

## Decision

Keep archive distribution as the only eligible private-trial package format.

Do not create, ship, or promise a Windows installer in P18.

Do not approve automatic updates in P18.

Do not present a credential-capable archive as public release, installer-ready,
or auto-update-ready.

## Archive Lane Requirements

A private-trial archive candidate may be considered only when all of these are
true:

- artifact is built from a clean pushed source commit;
- package variant is explicit: `base` or `credentials`;
- artifact label includes product, commit or version, variant, date, and
  distribution status;
- deterministic base package validation passes;
- explicit credentials package validation passes when that variant is shared;
- signing and verification policy is satisfied, or unsigned status is clearly
  labelled for private trial only;
- SHA256 hash is recorded in a transfer manifest;
- transfer path is private, access-controlled, and time-limited;
- testers receive no-secret feedback rules and cleanup instructions;
- package outputs, signed artifacts, transfer links, screenshots, logs, local
  app data, keyring exports, tester data, and provider secrets remain out of
  git.

Archive candidates must preserve the accepted local data boundary: config,
history, credential references, and keyring data stay outside packaged app
resources.

## Installer Blockers

An installer is not ready because P18 has not approved or implemented:

- production signing identity and certificate custody execution;
- signed installer build tooling;
- installer technology selection;
- per-user versus machine-wide install policy;
- install location and upgrade behavior;
- uninstall behavior and local data retention policy;
- rollback behavior after failed install or failed smoke;
- update channel, feed, or automatic updater runtime;
- Windows trust prompt and SmartScreen evidence for a signed installer;
- support workflow for partial install, locked files, policy-managed devices,
  or enterprise restrictions.

These blockers are policy and release-gate blockers, not product runtime
requirements for the current private archive lane.

## Installer Gate For Later Phase

A later installer phase must decide:

- whether installer scope is private pilot, beta, or public release;
- whether both `base` and `credentials` remain separate installer artifacts;
- whether the installer can be built and verified without moving provider,
  credential, settings, history, capture, OCR, or UI rules into packaging;
- how uninstall handles app binaries while leaving user data and credential
  stores under explicit user control;
- how update rollback preserves deterministic fake smoke and credential cleanup
  safety;
- how signed installer hashes, signatures, and verification evidence are
  retained without committing binaries or signing material.

## Round 5 Self-Checks

Debug self-check:

- The decision is explained by the smallest distribution workflow: archive
  candidate, explicit variant label, no installer, no updater, and later
  installer blockers.
- Success, unsigned private-trial, expected rejection, skipped signing,
  cleanup, rollback precursor, and no-secret states are covered.

Architecture self-check:

- Archive/installer policy does not move provider, credential, settings,
  history, capture, OCR, UI, or trial readiness rules into packaging.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No installer, updater, public release, cloud, OAuth, browser extension, AI
  summary, global hotkey, provider rewrite, OCR/capture rewrite, or full
  localization is introduced.
