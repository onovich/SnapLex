# P24 Unsigned Candidate Readiness

Date: 2026-07-17
Phase: P24 Non-Signing Private Trial Candidate Readiness And Feedback Watch Gate
Status: baseline revalidated; candidate readiness details pending

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

Round 2 will expand this baseline into the full unsigned candidate readiness
record.

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
