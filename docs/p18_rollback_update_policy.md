# P18 Rollback And Update Policy

Date: 2026-07-17
Phase: P18 Signing And Distribution Readiness Gate
Status: rollback and update expectations recorded; updater runtime not approved

P18 records how SnapLex should handle package rollback and update decisions
before broader signed distribution. It does not implement an updater, installer,
release feed, cloud account service, or public release channel.

## Decision

Use manual archive replacement only for the current private-trial lane.

Do not implement automatic update checks, background downloads, installer
repair, update feed parsing, delta updates, rollback services, or account-based
entitlement in P18.

Keep the previously accepted deterministic base package lane as the fallback
control path.

## Rollback Triggers

Stop distribution and roll back to the last accepted candidate when any of
these occur:

- package build or smoke fails for the selected variant;
- signing verification fails or points to the wrong identity;
- artifact hash differs from the approved transfer manifest;
- base package begins importing keyring or credential-only dependencies;
- credentials package smoke prints raw values, leaves cleanup uncertain, or
  changes provider/setup boundaries;
- `StartPackagedTrial.cmd --no-gui` stops failing closed when real provider
  setup is missing;
- tester feedback includes provider secrets, keyring exports, `.env` files,
  screenshots with sensitive content, package logs with secrets, or personal
  data that cannot be safely triaged;
- Windows trust prompt, malware warning, enterprise policy block, or locked
  Credential Locker behavior cannot be explained by the accepted package lane.

## Manual Rollback Steps

For private-trial archives, rollback means:

- mark the affected artifact label as withdrawn in the evidence record;
- disable or remove private transfer access;
- notify testers not to run or redistribute the affected archive;
- keep the last accepted source commit and artifact label as the fallback;
- rebuild only from a clean source commit after validation passes;
- rerun base and credentials package smoke before sharing a replacement;
- verify credential cleanup returns to PASS or `missing` after credential
  smoke;
- keep local config, history, credential references, and keyring data outside
  packaged app resources.

Rollback must not delete tester user data automatically. Tester cleanup
instructions must distinguish package files from local app data and credentials.

## Update Expectations

Private-trial updates are manual:

- testers receive an explicit replacement archive label and hash;
- testers stop the current app before replacing package files;
- testers keep or delete local app data only by explicit instruction;
- credential continuity is not assumed across machines or Windows users;
- real-provider readiness remains fail-closed when credentials are missing;
- the deterministic fake smoke remains the control path after every update.

Future update work requires a later gate that defines:

- release channel and version compatibility policy;
- signed artifact verification before update;
- installer or archive replacement behavior;
- rollback if update smoke fails;
- local app data migration policy;
- credential reference compatibility;
- support escalation for interrupted update, locked files, enterprise policy,
  and trust prompts.

## Non-Implementation Boundary

P18 does not add:

- updater runtime;
- installer repair or uninstall logic;
- update feed format;
- auto-download or background network behavior;
- cloud account, OAuth, billing, token broker, or entitlement checks;
- remote feature flags;
- package self-modification.

## Round 6 Self-Checks

Debug self-check:

- The policy is explained by the smallest rollback/update workflow: manual
  archive replacement, stop triggers, fallback candidate, and later updater
  gate.
- Success, expected rejection, cleanup, rollback, update skipped, no network,
  and no-secret states are covered.

Architecture self-check:

- Rollback/update policy does not move provider, credential, settings, history,
  capture, OCR, UI, or trial readiness rules into packaging.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No updater runtime, installer, public release, cloud, OAuth, browser
  extension, AI summary, global hotkey, provider rewrite, OCR/capture rewrite,
  or full localization is introduced.
