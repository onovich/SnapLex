# P12 Private Trial Pass/Fail Criteria

Date: 2026-07-16
Phase: P12 Private Trial Pilot And Feedback Triage
Status: ready for first pilot gate

Use these criteria before inviting or continuing the first controlled private
trial. They intentionally judge pilot readiness, not public release readiness.

## Pilot Pass Definition

The first private pilot can continue when all required gates pass:

- deterministic validation remains green;
- fake smoke mode launches from source;
- packaged fake smoke launches when a package exists;
- real trial paths fail closed when no real provider is configured;
- tester-facing release notes and feedback template are available;
- feedback instructions warn testers not to share secrets, personal data,
  sensitive screenshots, logs, `.env` files, keyring exports, package outputs,
  or local app data;
- no raw provider key value is stored in config, history, docs, tests, logs,
  screenshots, package resources, or git;
- known limitations are documented and do not contradict the shipped behavior.

## Required Gates

### Source And Test Gate

Required pass evidence:

```cmd
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
git diff --check
python -m snaplex --version
python -m snaplex --no-gui
python -m snaplex --check-real-provider
```

Expected result:

- validation passes;
- version prints `SnapLex 0.1.0`;
- no-GUI bootstrap exits cleanly;
- real-provider readiness rejects missing configuration when no real provider
  is configured.

### Trial Command Gate

Required pass evidence:

```cmd
StartTrial.cmd --no-gui
StartFakeTrial.cmd --no-gui
SmokeTrial.cmd
StartPackagedFakeTrial.cmd --no-gui
StartPackagedTrial.cmd --no-gui
```

Expected result:

- fake source and packaged fake paths pass and label fake smoke mode;
- real source and packaged real paths reject missing real-provider setup;
- `SmokeTrial.cmd` passes deterministic bootstrap/package smoke checks.

### GUI Gate

Required pass evidence:

```cmd
python scripts\p9_gui_smoke.py
python scripts\p11_visible_gui_smoke.py
```

Expected result:

- screenshot helpers report PASS;
- generated screenshots remain ignored local artifacts;
- shell, Settings, History, long text, fake warnings, and focus states are
  smoke-validated.

### Privacy Gate

Required pass evidence:

```cmd
git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs
```

Expected result:

- no generated package output, smoke app data, screenshots, logs, `.env`,
  keyring exports, OCR caches, or tester personal data is tracked.

## Severity And Disposition Rules

Use `docs/p12_feedback_intake_template.md` as the intake shape. Then classify:

| Severity | Meaning | Default disposition |
| --- | --- | --- |
| S0 Blocker | Prevents launch, deterministic validation, fake smoke, feedback safety, or fail-closed real trial behavior. | fix-now |
| S1 Critical | Breaks clipboard, Settings, History, packaged fake smoke, or no-secret credential handling. | fix-now or investigate |
| S2 Major | Confusing or unreliable, but workaround exists and pilot can continue safely. | investigate |
| S3 Minor | Copy, layout, low-risk documentation, or polish issue. | defer |
| S4 Question | Needs clarification, duplicate review, or future product decision. | investigate or reject |

## Must-Fix Before Continuing

Stop the private pilot until fixed if any of these occur:

- app cannot launch from source with current dependencies;
- `Validate.cmd` fails;
- fake smoke commands fail;
- packaged fake smoke fails when a package exists and is part of the pilot;
- real trial silently falls back to fake when no real provider is configured;
- credential readiness, Settings, logs, screenshots, or feedback echo a raw
  provider secret;
- feedback template or release notes encourage sharing API keys, private
  documents, sensitive screenshots, logs, `.env`, keyring exports, or package
  outputs;
- package or smoke data is accidentally tracked by git;
- tester cannot provide privacy-safe feedback.

## Investigate During Pilot

Continue only if there is a safe workaround and the report uses privacy-safe
evidence:

- visible focus is hard to follow but mouse flow works;
- Settings copy confuses one tester but provider readiness still behaves
  correctly;
- History behavior is unclear but data can be deleted and cleared;
- fake screen flow is confusing as OCR evidence;
- DPI, multi-monitor, or assistive technology behavior varies by device;
- package startup works but troubleshooting copy is incomplete.

## Accept As Known Limitation For P12

These are allowed in the first private pilot if they are disclosed:

- fake mode is not translation quality evidence;
- real provider smoke is optional/manual and skipped unless credentials already
  exist and a human approves network use;
- packaged keyring support is not promised;
- local secure credential testing uses source checkout plus `.[gui,credentials]`;
- Windows Credential Locker smoke is blocked when optional `keyring` is not
  installed;
- assistive technology, DPI scaling, and multi-monitor checks may be recorded as
  manual results or blockers;
- global hotkeys, browser extension runtime, AI summary runtime, account OAuth,
  SnapLex Cloud, billing, hosted token broker, full localization, provider
  rewrites, and OCR/capture rewrites are out of scope.

## Reject Or Resubmit

Reject or ask for a safe resubmission when feedback:

- includes provider secrets, personal data, private documents, sensitive
  screenshots, `.env` files, logs, package outputs, keyring exports, or local
  app data;
- requests a P12 non-scope feature as a blocker;
- treats fake mode as translation quality evidence;
- lacks mode, command/workflow, expected result, or actual result;
- cannot be reproduced without secrets or private content.

## Go/No-Go Summary

Pilot state is:

- `GO`: all required gates pass, no S0 blockers, and S1 issues have safe
  workarounds or clear fixes underway.
- `CONDITIONAL GO`: all safety gates pass, but S1/S2 issues need active
  monitoring during the next tester session.
- `NO-GO`: any S0 blocker, secret/privacy leak risk, deterministic validation
  failure, fake smoke failure, or real-trial fail-closed regression exists.
