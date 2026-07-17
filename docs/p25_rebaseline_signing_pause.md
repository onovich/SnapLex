# P25 Rebaseline And Signing Pause State

Date: 2026-07-17
Phase: P25 Non-Signing Private Trial Feedback Watch Pause Closeout Gate
Status: accepted P24 baseline revalidated; signing remains paused

P25 starts from the accepted P24 non-signing private-trial candidate readiness
and feedback watch gate. This document records the accepted baseline, current
HEAD, signing pause state, and assumptions for the P25 pause/closeout decision.

## Accepted Baseline

P24 is the accepted baseline for P25:

- accepted P24 commit:
  `bd4f1da0af33ece2350c3a820d799a094fdff0d9`;
- planner P25 guide commit:
  `ba8d17b435f007e4df01597dba11af06920f7a45`;
- current P25 dispatch HEAD:
  `8e61736fe1098ecb594977c6ad3db3e61438d104`;
- `main` is aligned with `origin/main`;
- P24 recorded no external tester feedback honestly and did not fabricate
  tester reports;
- P24 kept signing PAUSED and did not run signing commands;
- P24 did not create/import/purchase/invent/use certificates, call timestamp
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
present at the start of P25 editing.

## P25 Starting Assumptions

P25 may continue only while these assumptions remain true:

- signing remains PAUSED;
- the lane remains `unsigned-private-trial`;
- fake smoke remains deterministic and visibly fake;
- real-provider paths reject missing provider setup instead of silently falling
  back to fake;
- no tester feedback is recorded unless it is actually supplied and passes the
  privacy screen;
- package outputs and smoke data remain ignored local artifacts;
- no real-provider network smoke runs without existing local credentials and
  explicit human approval.

Round 2 uses this baseline to record the feedback watch disposition.

## Round 1 Self-Checks

Debug self-check:

- The baseline result is explained by the smallest P25 workflow: accept P24,
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
