# P17 Credential Package Lane Decision

Date: 2026-07-17
Phase: P17 Limited Credential Package Pilot And Signing Decision
Status: keep credentials as a separate explicit private-trial variant

P17 evaluates the explicit credential-capable package candidate after P16
production hardening and P17 pre-share gate rehearsal. The decision is to keep
credential support out of the deterministic base package and continue the
credential-capable path only as an explicit `credentials` package variant.

## Decision

Keep the `credentials` package as a separate explicit variant.

Do not silently add keyring support to the base package.

Do not make the credential package a public release in P17.

The P17 credential package lane may continue as a controlled unsigned
private-trial candidate when the pre-share gates pass. Broader distribution
requires later signing/distribution work and additional tester evidence.

## Evidence Supporting Separate Lane

Base lane evidence:

- base package build passed in P17 Round 2;
- `cmd /c SmokeTrial.cmd` passed;
- `cmd /c StartPackagedFakeTrial.cmd --no-gui` passed;
- `cmd /c StartPackagedTrial.cmd --no-gui` rejected missing real provider as
  expected;
- base credential smoke rejected keyring as unavailable, proving keyring was
  not silently included.

Credentials lane evidence:

- `python scripts\package_windows.py --variant credentials` passed;
- PyInstaller analyzed `keyring.backends.Windows`;
- packaged credential import discovered
  `keyring.backends.Windows.WinVaultKeyring`;
- cycle smoke passed save/read/delete and cleanup;
- save/check-delete passed restart readiness and cleanup;
- cleanup status returned to `missing`;
- smoke reference is phase-neutral:
  `snaplex/package-credential-smoke`;
- smoke output did not print raw credential values.

Operational evidence:

- tester intake and privacy screen are documented;
- external tester feedback was not supplied, and no report was fabricated;
- real-provider network smoke was skipped without explicit approval;
- artifact transfer, retention, and support escalation policy is documented;
- signing, installer, and updater are deferred outside P17.

## Why Not Merge Into Base

The base package remains the deterministic default because:

- automated and package smoke must not require keyring, credentials, network,
  screen permissions, model downloads, or provider API keys;
- base fake smoke provides a stable regression lane for every phase;
- keyring availability is environment-specific and can be blocked by Windows
  Credential Locker state, remote sessions, enterprise policy, or unsupported
  platforms;
- adding keyring to base would blur the accepted fake smoke and real credential
  boundaries.

## Conditions To Continue The Credentials Lane

The `credentials` lane can continue only when:

- it is built explicitly with `--variant credentials`;
- artifact labels include commit, variant, date, and unsigned/private-trial
  status;
- pre-share source/base/credentials gates pass;
- cleanup returns to PASS or `missing`;
- artifact and secret scans pass;
- testers receive setup, cleanup, failure-mode, and no-secret feedback rules;
- real-provider smoke remains optional/manual and explicitly approved.

## Stop Conditions

Stop or roll back the credential lane if:

- base package begins importing keyring;
- credential smoke prints or requests raw credential values in feedback;
- cleanup cannot be verified safely;
- import/cycle/restart readiness fails on selected tester lanes without a safe
  environment explanation;
- artifact transfer or tester feedback includes secrets, personal data, keyring
  exports, screenshots of credential fields, package outputs, logs with secrets,
  or provider response captures.

## Recommended Next Direction

Recommended next direction after P17:

- keep base package as the deterministic release-smoke baseline;
- continue controlled credential package pilot only if tester feedback remains
  no-secret and cleanup-safe;
- define a later signing/distribution readiness phase before wider sharing;
- collect real tester device evidence for locked Credential Locker,
  enterprise-managed policy, unsupported backend, and remote-session behavior;
- run optional real-provider smoke only with existing local credentials and
  explicit human network approval.

## Round 8 Self-Checks

Debug self-check:

- The decision is explained by the smallest lane workflow: base control,
  credential candidate, cleanup, tester intake, skipped real-provider smoke,
  and signing deferral.
- Success, expected rejection, no feedback, skipped network, cleanup, stop
  condition, and no-secret states are covered.

Architecture self-check:

- The credential package remains explicit and separate from base.
- The base package remains deterministic and keyring-free.
- Credential decisions stay behind credential services/stores, provider setup,
  and trial readiness boundaries.
- Provider calls remain behind provider registry and `TranslationPipeline`.
- No cloud/OAuth/billing/token broker, browser extension, AI summary, global
  hotkey, broad provider rewrite, OCR/capture rewrite, full localization,
  signed installer, updater, or public release is introduced.
