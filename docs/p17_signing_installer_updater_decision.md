# P17 Signing, Installer, And Updater Decision

Date: 2026-07-17
Phase: P17 Limited Credential Package Pilot And Signing Decision
Status: signing/installer/updater deferred beyond limited private trial

P17 decides whether the explicit `credentials` package candidate can continue
as an unsigned private-trial artifact and what must happen before broader
distribution. P17 does not implement code signing, installer packaging, updater
runtime, rollback, account systems, or public release infrastructure.

## Decision

Keep the P17 credential package candidate unsigned and private-trial only.

Do not implement a signed installer or updater in P17.

Before any wider external distribution, SnapLex needs a later signing and
distribution phase that decides:

- code-signing identity and certificate custody;
- signing command/process and verification evidence;
- installer versus archive distribution;
- update and rollback policy;
- artifact retention and revocation workflow;
- support escalation and tester communication channel;
- whether the credential-capable package remains a separate variant.

## Rationale

The current P17 evidence supports controlled private tester handling because:

- the credential-capable path is explicit as `--variant credentials`;
- the base package remains deterministic and keyring-free;
- credential import/cycle/save/check-delete smoke passes with WinVault;
- cleanup status returns to `missing`;
- tester intake and artifact policy prohibit secret-bearing feedback.

The evidence does not yet support broader unsigned distribution because:

- no external tester feedback was supplied in this executor session;
- no locked Credential Locker, enterprise-managed keyring policy, or wider
  tester device matrix has been exercised in P17;
- no real-provider network smoke was approved in P17;
- no public support channel, revocation workflow, installer rollback, or update
  path exists;
- unsigned artifacts are expected to trigger Windows trust prompts that are
  acceptable only in a small trusted private lane.

## Signing Gate For Later Phase

A later phase should require:

- clean source commit and release tag policy;
- reproducible base and credentials package gates;
- signing certificate owner and storage procedure;
- signed artifact verification command;
- Windows SmartScreen/trust prompt assessment;
- no-secret artifact and documentation scan;
- private tester re-smoke after signing.

Signing must not add keyring support to the base package.

## Installer Gate For Later Phase

A later installer decision should define:

- archive versus installer format;
- install location and uninstall behavior;
- whether per-user install is required;
- how local app data, config, history, and credentials remain outside packaged
  resources;
- how testers can remove package files without touching unrelated data;
- whether the installer includes only `base`, only `credentials`, or separate
  explicit artifacts.

Installer work must not move settings, provider, credential, history, capture,
OCR, or UI business rules into packaging scripts.

## Updater Gate For Later Phase

A later updater decision should define:

- whether automatic updates are allowed for private trial;
- manual update instructions and rollback steps;
- version compatibility for config/history files;
- credential continuity expectations;
- update artifact signing verification;
- failure behavior when update is interrupted.

No updater runtime is approved in P17.

## Current P17 Distribution Label

Use this label shape for any controlled P17 credential candidate:

```text
SnapLex-<commit>-credentials-<yyyymmdd>-unsigned-private-trial
```

The label must not imply public release, signed status, installer support, or
automatic updates.

## Round 7 Self-Checks

Debug self-check:

- The decision covers unsigned private-trial status, signing deferral,
  installer deferral, updater deferral, broader-distribution blockers, and
  later gates.
- Success, expected rejection, skipped network, no feedback, support blocker,
  and no-secret states are represented.

Architecture self-check:

- The decision keeps credential packaging explicit and separate from base.
- Signing/installer/updater policy does not change provider, credential,
  settings, history, capture, OCR, or UI ownership.
- No SnapLex Cloud, OAuth, billing, token broker, browser extension runtime, AI
  summary runtime, global hotkey, broad provider rewrite, OCR/capture rewrite,
  or full localization scope enters P17.
