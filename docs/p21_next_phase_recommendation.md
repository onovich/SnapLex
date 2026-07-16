# P21 Next Phase Recommendation

Date: 2026-07-17
Phase: P21 Signing Path Unblock Decision Or Pause Gate
Status: recommend non-signing next phase

Because P21 records signing as PAUSED, the next phase should not be a signing
rehearsal. The recommended P22 is a non-signing private-trial continuity and
tester-support gate.

## Recommended P22

Recommended phase name:

`P22 Non-Signing Private Trial Continuity And Tester Support Gate`

Recommended goal:

- preserve the accepted unsigned `base` and explicit private-trial
  `credentials` package lanes;
- keep signing paused until all unblock inputs are supplied;
- improve private-trial operational readiness without introducing new product
  runtime features;
- refresh tester-facing transfer, trust-label, support, and feedback triage
  documentation for unsigned/private-trial delivery;
- continue deterministic package, credential-smoke, boundary, and no-secret
  validation.

## Why This Is The Right Next Phase

P21 should pause signing because:

- P20 accepted signing as BLOCKED/SKIPPED;
- P21 received no explicit safe throwaway/test signing path approval;
- P21 is not allowed to run signing commands;
- no production certificate, signed archive, installer, updater, release feed,
  or public release is approved;
- continuing package-lane and tester-support readiness does not require
  signing.

## Recommended P22 Scope

- Keep `base` deterministic and keyring-free.
- Keep `credentials` explicit and private-trial only.
- Revalidate fake and credential-capable package lanes.
- Revalidate expected rejection for real-provider paths without configured
  credentials.
- Refresh unsigned/private-trial tester instructions and support intake.
- Record how testers should report trust prompts without sharing screenshots
  containing sensitive content.
- Confirm artifact transfer and retention rules for unsigned private-trial
  archives.
- Keep all package outputs, smoke data, logs, screenshots, local app data,
  `.env`, keyring exports, secrets, certificates, private keys, signed
  binaries, and timestamp responses out of git.

## Recommended P22 Non-Scope

- Signing command execution.
- Certificate creation, import, purchase, invention, or use.
- Timestamp service calls.
- Signed binary or signed archive candidate creation.
- Production signing.
- Public release.
- Installer or updater runtime.
- Release feed or auto-update behavior.
- Silent keyring support in the base package.
- SnapLex Cloud, account OAuth, billing, hosted token broker, browser
  extension runtime, AI summary runtime, global hotkeys, broad provider/OCR/
  capture rewrites, or full localization.

## When To Return To Signing

Return to a signing rehearsal phase only when the P21 unblock requirements are
available. The later signing phase should start from
`docs/p21_signing_unblock_requirements.md`, record approval before commands
run, use ignored local artifact paths, and commit only non-secret evidence.

## P21 Self-Checks

Debug self-check:

- The recommendation follows directly from the PAUSED decision and the missing
  safe signing-path inputs.
- Success, expected rejection, missing approval, paused signing, no
  certificate, no signing command, no timestamp, no-artifact, and no-secret
  states are covered.

Architecture self-check:

- This recommendation changes only planning evidence.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
