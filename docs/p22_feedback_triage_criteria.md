# P22 Feedback Triage And Pass/Fail Criteria

Date: 2026-07-17
Phase: P22 Non-Signing Private Trial Continuity And Tester Support Gate
Status: feedback criteria refreshed for unsigned private trial

Use these criteria to classify private-trial feedback during P22. P22 judges
unsigned private-trial continuity, tester support, and package-lane safety. It
does not judge public-release readiness or signing readiness.

## P22 Pass Definition

P22 can pass when all required gates are true:

- signing remains explicitly PAUSED and the trust label remains
  `unsigned-private-trial`;
- source validation and no-GUI bootstrap pass;
- real-provider readiness rejects missing configuration instead of silently
  falling back to fake translation;
- deterministic fake smoke passes from source and from the base package;
- the base package remains keyring-free and rejects credential smoke with the
  expected unavailable-keyring result;
- the explicit credentials package remains private-trial only and passes
  throwaway import/cycle/save/check-delete smoke;
- tester-facing instructions, support intake, privacy guidance, and triage
  criteria are current and mutually consistent;
- package outputs, screenshots, logs, local app data, smoke data, `.env` files,
  keyring exports, certificates, private keys, signed binaries, timestamp
  responses, OCR caches, tester personal data, and provider secrets are not
  staged or committed.

## Required Gates

### Source And Validation Gate

Required evidence:

```cmd
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
git diff --check
python -m snaplex --version
python -m snaplex --no-gui
python -m snaplex --check-real-provider
```

Expected result:

- validation passes with the current deterministic test suite;
- version reports `SnapLex 0.1.0`;
- no-GUI bootstrap exits cleanly;
- real-provider readiness rejects missing configuration when no provider is
  configured.

### Base Package Continuity Gate

Required evidence:

```cmd
python scripts\package_windows.py --dry-run --variant base
StartTrial.cmd --no-gui
StartFakeTrial.cmd --no-gui
SmokeTrial.cmd
StartPackagedFakeTrial.cmd --no-gui
StartPackagedTrial.cmd --no-gui
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Expected result:

- base dry-run passes;
- fake source, smoke, and packaged fake paths pass;
- real source and packaged real paths reject missing real-provider setup;
- base credential smoke rejects keyring use because the deterministic base
  package is keyring-free.

### Credentials Package Continuity Gate

Required evidence:

```cmd
python scripts\package_windows.py --dry-run --variant credentials
python scripts\package_windows.py --variant credentials
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
python scripts\package_windows.py --variant base
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Expected result:

- credentials dry-run and build pass;
- import reports the Windows keyring backend when available in the explicit
  credentials package;
- cycle/save/check-delete use only runtime-generated throwaway values and do
  not print raw credentials;
- the final base rebuild restores the deterministic keyring-free behavior.

### Support And Privacy Gate

Required evidence:

- `docs/p22_unsigned_private_trial_release_notes.md`
- `docs/p22_tester_support_intake.md`
- this document
- `docs/p22_artifact_transfer_retention.md`, once created
- final boundary scans

Expected result:

- tester materials clearly say unsigned, private trial, not public release;
- reports require synthetic/non-sensitive examples;
- sensitive materials are rejected or resubmitted safely;
- no support path asks for raw credentials, private documents, screenshots with
  sensitive content, logs, package outputs, keyring exports, certificates,
  private keys, signed binaries, timestamp responses, or provider secrets.

## Severity And Disposition Rules

| Severity | Meaning | Default disposition |
| --- | --- | --- |
| S0 Blocker | Secret/privacy leak risk, deterministic validation failure, base package drift, fake/real confusion, unsafe support intake, or public/signed-release confusion. | fix-now |
| S1 Critical | Core private-trial workflow failure in source, base package, credentials package, Settings, History, clipboard, screen, provider readiness, or credential smoke. | fix-now or investigate |
| S2 Major | Realistic trial friction with a safe workaround, such as DPI, multi-monitor, assistive technology, provider setup confusion, or trust-prompt friction. | investigate |
| S3 Minor | Copy, layout, low-risk documentation, or polish issue that does not affect safe trial operation. | defer |
| S4 Question | Needs reproduction details, duplicate review, privacy-safe resubmission, or future product decision. | investigate or reject |

Disposition values:

- `fix-now`: repair before continuing the affected private-trial lane;
- `investigate`: gather privacy-safe reproduction, environment detail, or a
  focused deterministic smoke;
- `defer`: valid but outside the P22 continuity/support gate;
- `reject/resubmit`: sensitive, incomplete, duplicate, or boundary-breaking;
- `accepted limitation`: already disclosed and safe for P22.

## Must-Fix Before Continuing

Stop the affected private-trial lane until fixed if any of these occur:

- `Validate.cmd`, no-GUI bootstrap, fake smoke, or packaged fake smoke fails;
- real-provider readiness or launch silently falls back to fake as if it were
  real translation;
- base package imports keyring support or accepts credential smoke;
- credentials package cannot complete throwaway import/cycle/save/check-delete
  smoke when that lane is being shared;
- tester instructions, support intake, or feedback templates request secrets,
  raw logs, sensitive screenshots, package outputs, certificates, private keys,
  signed artifacts, timestamp responses, or personal data;
- a package, screenshot, log, local app data, smoke data, OCR cache, `.env`,
  keyring export, certificate, private key, signed binary, timestamp response,
  tester data, or provider secret is staged or committed;
- unsigned/private-trial wording suggests the artifact is signed, installer
  ready, updater ready, public release, or production-approved.

## Investigate During Pilot

Continue only with a safe workaround and privacy-safe evidence when:

- Windows trust prompts are confusing but testers understand the
  `unsigned-private-trial` label;
- focus, keyboard, DPI, multi-monitor, or assistive-technology behavior varies
  by device;
- provider setup copy is unclear but readiness still fails closed safely;
- History, Settings, clipboard, or screen flow is confusing but usable;
- credentials package setup works on maintainer machines but needs a tester
  confirmation for a specific Windows environment.

## Accepted P22 Limitations

These are not failures when disclosed:

- signing remains paused;
- artifacts are unsigned private-trial materials, not public release assets;
- no signing commands, certificates, timestamp services, signed archives,
  installer, updater, or release feed are part of P22;
- fake mode is not translation-quality evidence;
- real-provider smoke is optional/manual and requires existing local
  credentials plus explicit human network approval;
- base package is intentionally keyring-free;
- credentials package is explicit, private-trial only, and not silently merged
  into base;
- no SnapLex Cloud, account OAuth, billing, hosted token broker, browser
  extension runtime, AI summary runtime, global hotkeys, broad provider/OCR/
  capture rewrite, or full localization is implemented in P22.

## Reject Or Resubmit

Reject or request a sanitized resubmission when feedback:

- includes provider secrets, passwords, personal data, private documents,
  sensitive screenshots, `.env` files, logs, package outputs, keyring exports,
  local app data, OCR caches, certificates, private keys, signed binaries,
  timestamp responses, or provider dashboard content;
- asks P22 to run signing commands or create/import/purchase/invent/use a
  certificate;
- asks for a public release, installer, updater, release feed, cloud account,
  hosted broker, browser extension runtime, AI summary runtime, global hotkey,
  broad provider/OCR/capture rewrite, or full localization;
- treats fake mode as translation-quality evidence;
- lacks lane, mode, expected result, actual result, and reproduction steps.

## Go/No-Go Summary

- `GO`: all required gates pass, no S0 blockers exist, S1 issues are fixed or
  have safe workarounds, and signing is accurately labeled PAUSED.
- `CONDITIONAL GO`: safety gates pass, but S1/S2 issues need active monitoring
  during the next private-trial session.
- `NO-GO`: any S0 blocker, secret/privacy leak risk, deterministic validation
  failure, fake smoke failure, base package drift, real-provider fail-closed
  regression, unsafe support intake, or signed/public-release confusion exists.

## Round 4 Self-Checks

Debug self-check:

- Criteria distinguish source, base package, credentials package, support,
  privacy, signing pause, and real-provider gates.
- Expected success, expected rejection, accepted limitation, investigation,
  reject/resubmit, and no-go states are covered.

Architecture self-check:

- The criteria preserve provider, credential, settings, history, capture, OCR,
  UI, packaging, and trial-readiness boundaries.
- They do not add signing, certificates, installers, updaters, release feeds,
  public release, or new runtime features to P22.
