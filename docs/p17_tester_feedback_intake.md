# P17 Tester Instructions And Feedback Intake

Date: 2026-07-17
Phase: P17 Limited Credential Package Pilot And Signing Decision
Status: no-secret tester instructions and intake template ready

Use this document for controlled private testers who receive the explicit
unsigned `credentials` package candidate. This is not a public release channel.
It is an intake guardrail for package, keyring, cleanup, and optional
real-provider readiness evidence.

## Before Sending To A Tester

Maintainer checklist:

- Confirm the package candidate passed
  `docs/p17_package_candidate_gate_evidence.md`.
- Label the package with source commit, `credentials` variant, date, and
  unsigned private-trial status.
- Send or link:
  - `docs/p16_tester_setup_cleanup_guide.md`;
  - `docs/p16_keyring_failure_modes.md`;
  - this P17 intake document.
- Confirm the tester understands not to send provider secrets, keyring exports,
  `.env` files, screenshots of credential fields, private documents, package
  outputs, local app data, logs with secrets, or personal data.
- Keep artifact transfer private and record the artifact label in the pilot
  evidence.

Do not send the credential candidate when the base control lane, credential
candidate lane, cleanup status, artifact scan, or secret scan has failed.

## Tester Setup Instructions

Ask the tester to:

1. Extract the provided `SnapLex` folder into a local trial folder outside any
   git repository or synced project workspace.
2. Keep the artifact label in their notes.
3. Run `SnapLex.exe --version`.
4. Run `SnapLex.exe --no-gui`.
5. Run:

   ```cmd
   SnapLex.exe --smoke-credentials --credential-smoke-mode import
   ```

6. If the maintainer explicitly requests credential smoke, run:

   ```cmd
   SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
   ```

7. If asked to test restart readiness, run `save` first and `check-delete`
   after relaunching a new command session:

   ```cmd
   SnapLex.exe --smoke-credentials --credential-smoke-mode save
   SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
   ```

Expected safe result:

- version and no-gui pass;
- import reports a keyring backend;
- cycle reports save/read/delete and cleanup PASS;
- save/check-delete reports restart readiness and cleanup PASS;
- output includes `snaplex/package-credential-smoke`;
- output never asks the tester to paste a provider key into feedback.

## Real-Provider Smoke Rule

Do not ask a tester to run real translation by default.

Real-provider smoke is allowed only when all are true:

- the tester already has their own local provider credential;
- the tester intentionally agrees to network use for that run;
- the maintainer asks for a specific provider smoke;
- the report omits provider key values, `.env` content, provider dashboard
  screenshots, private text, raw API responses, and logs with secrets.

Fake smoke and credential smoke remain sufficient for automated and package
gate evidence when no real-provider approval exists.

## Feedback Report Template

Copy this block for each P17 credential package report:

```text
Title:

Artifact label:
SnapLex-<commit>-credentials-<date>-unsigned-private-trial

Package variant:
- [ ] credentials
- [ ] base control
- [ ] unsure

Mode:
- [ ] version/no-gui
- [ ] credential import smoke
- [ ] credential cycle smoke
- [ ] credential save/check-delete restart readiness
- [ ] fake package smoke
- [ ] real-provider smoke approved by tester and maintainer
- [ ] cleanup
- [ ] documentation/setup
- [ ] other:

Environment:
- Windows version:
- Windows account type: local / Microsoft / domain / unknown
- Credential Locker policy: normal / locked / enterprise-managed / unknown
- Display scaling:
- Monitor count:
- Assistive technology active? yes/no/unknown

Command used:

Expected result:

Actual result:

Status lines copied from SnapLex output:

Backend label if shown:

Cleanup status:
- [ ] PASS
- [ ] missing
- [ ] failed
- [ ] not run

Does this block the credential package pilot?
- [ ] Yes, cannot continue on this tester lane
- [ ] No, but should investigate before wider trial
- [ ] No, can defer
- [ ] Unsure

Privacy check:
- [ ] No API keys, bearer tokens, `.env` files, keyring exports, provider
      dashboard screenshots, or credential field screenshots are included.
- [ ] No private documents, private chats, customer data, or sensitive
      screenshots are included.
- [ ] No package outputs, local app data, raw logs, config/history files, OCR
      caches, or API response captures are included.
- [ ] Any text sample is synthetic/non-sensitive.
```

## Triage Categories

Use one primary category:

- `package-artifact`: extraction, version, no-gui, launch, or artifact labeling.
- `base-control`: deterministic base smoke or base credential expected
  rejection.
- `credential-import`: keyring import/backend discovery.
- `credential-cycle`: save/read/delete in one run.
- `credential-restart`: save then check-delete restart readiness.
- `credential-cleanup`: cleanup did not return to PASS or `missing`.
- `real-provider-optional`: approved manual real-provider smoke only.
- `docs-setup`: tester instructions are unclear.
- `environment-blocker`: locked session, enterprise policy, unsupported
  backend, or device-specific blocker.

## Severity And Disposition

Severity:

- `S0 Blocker`: package cannot launch, credential smoke leaks a secret, cleanup
  cannot be verified, or real trial runs without explicit approval.
- `S1 Critical`: credential import/cycle/restart fails on a selected tester
  lane without a safe workaround.
- `S2 Major`: confusing setup or environment-specific blocker with a workaround.
- `S3 Minor`: copy, labeling, or documentation issue.
- `S4 Question`: unclear, duplicate, or needs a privacy-safe reproduction.

Disposition:

- `fix-now`: repair before sharing further.
- `investigate`: needs focused deterministic or manual evidence.
- `defer`: valid but outside P17.
- `reject/resubmit`: contains sensitive material or asks for forbidden scope.
- `accepted limitation`: already covered by P16/P17 support policy.

## Privacy Screen

Reject or request a sanitized resubmission when a report includes:

- provider API keys, bearer tokens, `.env` contents, launchers containing
  secrets, keyring exports, or smoke credential values;
- private source text, translated private text, private documents, account
  dashboards, customer data, personal data, or sensitive screenshots;
- raw package outputs, local app data directories, logs with secrets,
  config/history files, OCR caches, provider API responses, or binaries.

## Round 3 Self-Checks

Debug self-check:

- The current result is explained by the smallest tester workflow: artifact
  label, version/no-gui, import, cycle, save/check-delete, cleanup, optional
  real-provider approval, and privacy screen.
- Success, expected rejection, unavailable backend, no feedback yet, skipped
  network, cleanup, and resubmit states are covered.

Architecture self-check:

- Tester instructions keep credentials behind credential smoke and
  `CredentialService`; no UI or packaging script owns provider secrets.
- Provider execution remains optional/manual and behind the accepted provider
  and `TranslationPipeline` boundaries.
- The base package remains the deterministic control lane.
- The document avoids cloud, OAuth, billing, token broker, browser extension,
  AI summary, global hotkey, broad provider/OCR/capture rewrite, and full
  localization scope.
