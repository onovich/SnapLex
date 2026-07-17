# P24 Unsigned Candidate Readiness

Date: 2026-07-17
Phase: P24 Non-Signing Private Trial Candidate Readiness And Feedback Watch Gate
Status: unsigned private-trial candidate readiness recorded

P24 starts from the accepted P23 private-trial feedback/support loop baseline.
This document records the accepted baseline, current signing pause state, and
the non-signing private-trial candidate assumptions that later P24 rounds will
expand into a full readiness record.

## Accepted Baseline

P23 is the accepted baseline for P24:

- accepted P23 commit:
  `b2b0979b2dc2d2cf23eaea255620ef3e1ab23b60`;
- planner P24 guide commit:
  `d78018e69f2ab972112006f58d73bece520217ab`;
- current P24 dispatch HEAD:
  `a22e8c7b6a04f0b20266c564d2ecb4cbe690070a`;
- `main` is aligned with `origin/main`;
- P23 recorded no external tester feedback honestly and did not fabricate
  tester reports;
- P23 kept signing PAUSED and did not run signing commands;
- P23 did not create/import/purchase/invent/use certificates, call timestamp
  services, create signed artifacts, approve installers/updaters/release feeds,
  or approve public release;
- the `base` package remains deterministic and keyring-free;
- the `credentials` package remains explicit and private-trial only.

## Round 1 Revalidation Results

Commands:

```cmd
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
git diff --check
python -m snaplex --version
python -m snaplex --no-gui
python -m snaplex --check-real-provider
python scripts\package_windows.py --dry-run --variant base
python scripts\package_windows.py --dry-run --variant credentials
git status --short --ignored
```

Results:

- `Validate.cmd` passed with 264 tests.
- `git diff --check` passed.
- `python -m snaplex --version` passed and reported `SnapLex 0.1.0`.
- `python -m snaplex --no-gui` passed.
- `python -m snaplex --check-real-provider` rejected missing real provider
  setup as expected.
- `python scripts\package_windows.py --dry-run --variant base` passed and
  reported `SNAPLEX_PACKAGE_VARIANT=base`.
- `python scripts\package_windows.py --dry-run --variant credentials` passed
  and reported `SNAPLEX_PACKAGE_VARIANT=credentials`.

## Local Ignored Artifact State

`git status --short --ignored` showed only ignored local outputs and caches:

- `.codex/Role.md`
- `.mypy_cache/`
- `.pytest_cache/`
- `.ruff_cache/`
- `build/`
- `dist/`
- `scripts/__pycache__/`
- `snaplex-smoke-data/`
- `snaplex.egg-info/`
- package `__pycache__/` directories
- `tests/__pycache__/`
- `tmp/`

No nonignored package output, signing material, certificate, private key,
signed binary, timestamp response, screenshot, log, `.env`, keyring export,
tester data, local app data, smoke data, OCR cache, or provider secret was
present at the start of P24 editing.

## Round 1 Candidate Position

P24 may continue candidate-readiness work only while these assumptions remain
true:

- signing remains PAUSED;
- the candidate is labeled unsigned/private-trial only;
- fake smoke remains deterministic and visibly fake;
- real-provider paths reject missing provider setup instead of silently falling
  back to fake;
- package outputs and smoke data remain ignored local artifacts;
- tester feedback, if any arrives, must be privacy-screened before repository
  evidence is written;
- no real-provider network smoke runs without existing local credentials and
  explicit human approval.

Round 2 expands this baseline into the full unsigned candidate readiness record.

## Candidate Trust Label

Current trust label: `unsigned-private-trial`.

This label means:

- the candidate is private-trial material only;
- artifacts are unsigned;
- artifacts are not public release, signed archive, installer, updater, release
  feed, or broadly supported production material;
- Windows trust prompts are expected and must be reported with sanitized text,
  not sensitive screenshots;
- signing remains PAUSED until a later planner-approved signing phase receives
  every input listed in `docs/p21_signing_unblock_requirements.md`.

Every candidate artifact or tester-facing instruction must include:

- `SnapLex`;
- source commit prefix;
- package lane: `source`, `base`, or `credentials`;
- date;
- `unsigned-private-trial`.

## Supported Candidate Lanes

| Lane | Candidate use | Required state | Not allowed |
| --- | --- | --- | --- |
| Source checkout | Maintainer/tester source smoke, fake workflow checks, docs/support review. | Local dependencies installed through project instructions; no real provider unless credentials and network approval already exist. | Treating source smoke as signed/public release evidence. |
| Base package | Deterministic fake smoke, no-GUI bootstrap, packaged workflow smoke. | `SNAPLEX_PACKAGE_VARIANT=base`; fake smoke passes; real-provider paths fail closed; credential smoke rejects keyring. | Keyring support, raw credentials, real-provider fallback to fake, public release claims. |
| Credentials package | Controlled private-trial credential smoke with throwaway generated values. | Explicit `SNAPLEX_PACKAGE_VARIANT=credentials`; import/cycle/save/check-delete pass; cleanup passes; output contains no raw credential value. | Silent merge into base, provider secrets, keyring exports, broad distribution, signed/public release claims. |

## Setup Expectations

Default safe path:

- no credentials;
- no network;
- fake smoke mode only;
- synthetic sample text;
- ignored local app data and smoke directories.

Before source or package validation:

- run deterministic validation or use the latest accepted validation evidence;
- keep generated `build/`, `dist/`, `snaplex-smoke-data/`, screenshots, logs,
  `.env`, OCR caches, package archives, keyring exports, and local app data out
  of git;
- use `StartFakeTrial.cmd`, `SmokeTrial.cmd`, and
  `StartPackagedFakeTrial.cmd` for fake package confidence;
- use `StartTrial.cmd` and `StartPackagedTrial.cmd` only to confirm fail-closed
  behavior when no real provider is configured.

Before credentials package smoke:

- build only the explicit `credentials` variant;
- use only runtime-generated throwaway values;
- run `import`, `cycle`, `save`, and `check-delete` in order;
- confirm output reports only backend, reference, mode, and PASS/FAIL status;
- restore the base package afterward and confirm base credential smoke rejects
  keyring.

## Candidate Blockers

Hold the affected candidate lane if any of these occur:

- `Validate.cmd`, no-GUI bootstrap, fake source smoke, or packaged fake smoke
  fails;
- a real-provider path silently falls back to fake as if it were real
  translation;
- the base package imports keyring support or accepts credential smoke;
- the credentials package cannot complete throwaway import/cycle/save/
  check-delete when that lane is being considered;
- feedback intake asks testers to provide secrets, raw logs, sensitive
  screenshots, package outputs, keyring exports, certificates, private keys,
  signed binaries, timestamp responses, or personal data;
- generated package outputs, screenshots, logs, smoke data, local app data,
  OCR caches, `.env`, keyring exports, certificates, private keys, signed
  binaries, timestamp responses, or provider secrets are staged or committed;
- unsigned/private-trial wording suggests the candidate is signed, installer
  ready, updater ready, public release, or production-approved.

## Release-Hold Boundaries

P24 readiness does not approve:

- signing commands;
- certificate creation, import, purchase, invention, or use;
- timestamp service calls;
- signed binaries or signed archives;
- installers, updaters, release feeds, auto-update behavior, or public release;
- SnapLex Cloud, OAuth, billing, hosted token broker, browser extension
  runtime, AI summary runtime, global hotkeys, broad provider/OCR/capture
  rewrites, or full localization.

## Candidate Readiness Decision

Current Round 2 decision: CONDITIONALLY READY FOR NON-SIGNING PRIVATE-TRIAL
WATCH.

Conditions:

- Round 5 must refresh the deterministic base package candidate evidence.
- Round 6 must refresh explicit credentials package candidate evidence.
- Round 7 must record the release-hold/support decision.
- Round 8 must pass boundary, artifact, secret, certificate, private-key,
  package-output, screenshot, log, and signing-material scans.
- Round 10 must pass final validation and produce the P24 final report and P25
  handoff.

This decision does not authorize public release, signing, installer/updater
work, or broader runtime feature expansion.

## Round 2 Self-Checks

Debug self-check:

- The candidate readiness record is explained by the smallest private-trial
  workflow: label the unsigned candidate, define source/base/credentials lanes,
  require expected fail-closed behavior, define blockers, and keep release on
  hold.
- Success, expected rejection, no-feedback, late-feedback, cleanup,
  unsupported, no-network, no-signing, no-artifact, and no-secret states are
  covered.

Architecture self-check:

- Candidate readiness remains documentation/support evidence.
- Provider, credential, settings, packaging, and trial-readiness boundaries stay
  separated.
- The base package remains deterministic and keyring-free.
- The credentials package remains explicit/private-trial.
- No signing, public release, installer, updater, release feed, cloud/account,
  browser, AI summary, hotkey, broad runtime feature, certificate, private key,
  signed artifact, timestamp response, or signing log is introduced.

## Round 1 Self-Checks

Debug self-check:

- The baseline result is explained by the smallest P24 workflow: accept P23,
  confirm current HEAD, run deterministic validation, confirm package dry-runs,
  and record that signing remains PAUSED.
- Success, expected rejection, no-feedback baseline, missing real provider,
  paused signing, ignored local output, no-certificate, no-signing-command,
  no-artifact, and no-secret states are covered.

Architecture self-check:

- Rebaseline work does not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, signing, installer, updater, release feed, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
