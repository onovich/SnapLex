# P20 Isolated Rehearsal Evidence

Date: 2026-07-17
Phase: P20 Approved Signing Path Acquisition And Rehearsal Setup Gate
Status: BLOCKED/SKIPPED - no approved safe throwaway/test signing path

P20 does not run an isolated signing rehearsal because the signing path approval
record is BLOCKED/SKIPPED. The phase records this absence honestly and
continues deterministic package-lane validation.

## Rehearsal Decision

Decision: BLOCKED/SKIPPED.

Reason:

- no explicit safe throwaway/test signing path approval exists;
- no approved local throwaway certificate or managed signing sandbox exists;
- no approval was supplied to generate a local test certificate;
- no production certificate is in scope;
- no private-key custody rule exists;
- no timestamp policy execution exists;
- `signtool.exe` is not currently discoverable on PATH;
- P20 must not invent signing material to satisfy the gate.

## Signing Commands

No signing commands were run.

Not run:

- production signing;
- local self-signed certificate generation;
- certificate import;
- signing with a local certificate store;
- signing with a hardware token;
- managed signing service call;
- timestamp service call;
- signature verification against signed output.

Command discovery only is recorded in
`docs/p20_signing_command_discovery.md`.

## Local Artifact State

No P20 signing rehearsal artifact directory was created for output.

Allowed future local-only directories are recorded in
`docs/p20_rehearsal_artifact_directory_policy.md`, but they remain policy
until approval exists.

Not created or committed:

- certificates;
- private keys;
- signed binaries;
- signed archives;
- timestamp responses;
- signing logs;
- screenshots;
- package outputs;
- `.env` files;
- keyring exports;
- tester data;
- provider secrets.

## Package Lane Preservation

Although signing was blocked/skipped, P20 continues to preserve package lane
validation:

- base package validation remains the deterministic, keyring-free lane;
- credentials package validation remains explicit and private-trial only;
- real-provider launchers must fail closed when no real provider is configured;
- fake-provider launchers remain deterministic smoke/dev paths.

Package lane evidence is recorded separately in:

- `docs/p20_base_package_control_evidence.md`;
- `docs/p20_credentials_package_control_evidence.md`.

## Evidence Retained

Retained in git:

- this Markdown BLOCKED/SKIPPED evidence record;
- approval, artifact policy, and command discovery records;
- non-secret package lane evidence docs.

Retained only as ignored local output:

- `build/`
- `dist/`
- `snaplex-smoke-data/`
- cache directories

No binary or secret-bearing evidence is retained in git.

## Round 5 Self-Checks

Debug self-check:

- The evidence is explained by the smallest rehearsal workflow: approval is
  missing, signing is blocked/skipped, no signing command runs, and package
  lanes continue.
- Success, expected rejection, missing approval, skipped signing, skipped
  timestamp, no certificate, no artifact, cleanup requirement, and no-secret
  states are covered.

Architecture self-check:

- Rehearsal evidence does not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness code.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
