# P22 Unsigned Private Trial Release Notes

Date: 2026-07-17
Phase: P22 Non-Signing Private Trial Continuity And Tester Support Gate
Status: tester-facing unsigned/private-trial instructions ready

These notes are for continuing controlled SnapLex private-trial validation
while signing remains paused. P22 is not a public release, signing rehearsal,
installer, updater, release feed, or runtime feature phase.

## At A Glance

- Product: SnapLex `0.1.0`.
- Platform focus: Windows desktop.
- Current trust label: `unsigned-private-trial`.
- Signing state: PAUSED.
- Default safe path: fake smoke mode, no credentials, no network.
- Base package path: deterministic fake smoke and bootstrap only.
- Credentials package path: explicit `credentials` variant for controlled
  private-trial credential smoke only.
- Real provider path: optional/manual only, requires existing local credentials
  and explicit human approval for network use.

## Trust Label

Current trust label: `unsigned-private-trial`.

All P22 trial artifacts are unsigned private-trial artifacts. Signing remains
PAUSED until a later planner-approved signing phase receives every input listed
in `docs/p21_signing_unblock_requirements.md`.

Do not run signing commands in P22. Do not create, import, purchase, invent, or
use certificates. Do not call timestamp services. Do not produce signed
binaries or signed archives.

If Windows displays an unsigned-app trust prompt, report the trust label and
the command you were trying to run. Do not attach screenshots that contain
private files, account names, credentials, provider dashboards, personal data,
or sensitive desktop content. Reproduce with a clean test folder and synthetic
text when a screenshot is truly needed.

## What Testers Receive

A private tester may receive one of these lanes:

- source checkout instructions;
- a deterministic unsigned `base` package folder for fake smoke;
- an explicit unsigned `credentials` package folder for credential smoke.

Each artifact should be labeled with:

- `SnapLex`;
- source commit prefix;
- package lane: `base` or `credentials`;
- date;
- `unsigned-private-trial`.

Do not treat any P22 artifact as a signed archive, installer, updater, public
release, or broadly supported package.

## Tester Privacy Rules

Do not paste or attach:

- provider API keys, bearer tokens, `.env` files, keyring exports, or launchers
  containing secrets;
- screenshots containing private documents, private chats, account dashboards,
  credential fields, personal data, or customer data;
- raw logs, package outputs, local app data, config/history files, OCR caches,
  or API response captures;
- real names, email addresses, phone numbers, or other personal data unless the
  tester intentionally provides them outside the repository for follow-up.

Use synthetic sample text such as `hello`, `invoice total`, or `screen hello`.
If a report needs a screenshot, reproduce the issue with non-sensitive text
first.

## Before You Start

Use a clean source checkout or a private package folder supplied by the release
owner. Keep any package folder outside git-tracked directories and synced
repositories.

For source-based testing, install local trial dependencies:

```cmd
SetupTrial.cmd
```

For deterministic package testing, use the supplied `base` package or build one
locally:

```cmd
BuildTrial.cmd
```

Generated `build\`, `dist\`, `snaplex-smoke-data\`, screenshots, app data,
logs, `.env` files, keyring exports, OCR caches, and package archives are local
artifacts. Do not send or commit them.

## Trial Paths

### Fake Smoke Mode

Use fake mode to validate the interface and package without credentials or
network access:

```cmd
StartFakeTrial.cmd
StartPackagedFakeTrial.cmd
SmokeTrial.cmd
```

Fake output is deterministic placeholder text and is visibly labeled as fake
smoke mode. It is not real translation quality evidence.

Use fake smoke when checking:

- app launch and no-GUI bootstrap;
- main shell layout and focus;
- Settings and History behavior;
- package bootstrap and deterministic workflow smoke;
- feedback template quality.

### Real Provider Trial

Use real provider mode only when a local private-trial provider key or accepted
endpoint already exists and a human explicitly approves network use for that
session:

```cmd
StartTrial.cmd
```

Run readiness first:

```cmd
python -m snaplex --check-real-provider
```

If no real provider is configured, SnapLex should reject launch with:

```text
Real translation provider is not configured.
```

Use a separate short-lived trial key with the lowest practical quota, budget,
and access. Rotate it after sharing a build or after any suspected exposure. Do
not paste the key into feedback.

### Packaged Base Trial

The deterministic unsigned `base` package supports fake smoke and no-GUI
bootstrap. It intentionally does not include keyring support.

Recommended package checks:

```cmd
StartPackagedFakeTrial.cmd --no-gui
StartPackagedTrial.cmd --no-gui
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Expected result:

- fake packaged trial exits cleanly and labels fake smoke mode;
- real packaged trial rejects missing real-provider configuration;
- base credential smoke rejects keyring as unavailable.

### Credentials Package Trial

The unsigned `credentials` package is explicit and private-trial only. Use it
only when the maintainer asks for credential-capable package smoke:

```cmd
python scripts\package_windows.py --variant credentials
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Expected result:

- `import` reports `keyring.backends.Windows.WinVaultKeyring`;
- `cycle` reports save/read/delete and cleanup PASS;
- `save` reports the credential is retained for restart check;
- `check-delete` reports restart readiness and cleanup PASS;
- output includes `snaplex/package-credential-smoke`;
- output never includes a raw credential value.

Run `save` and `check-delete` as separate commands, in that order.

## What To Verify

### Launch And Navigation

- The main SnapLex window opens and closes cleanly.
- Primary actions are clear: `Translate Clipboard` and `Translate Screen`.
- Secondary actions are clear: `Settings` and `History`.
- Focus is visible enough to follow keyboard navigation.

### Clipboard Flow

- Copy synthetic text such as `hello`.
- Select `Translate Clipboard`.
- Confirm a result appears.
- Confirm fake results are labeled as fake smoke mode when fake mode is active.
- Use `Copy Result`, `Retry`, and `Close Result`.

### Screen Flow

- Select `Translate Screen`.
- Test a non-sensitive region only.
- Cancel with `Esc` and confirm the app recovers cleanly.
- If using fake/default capture behavior, treat the result as smoke evidence,
  not real OCR quality evidence.

### Settings And Provider Setup

- Open `Settings`.
- Confirm provider fields are understandable.
- Confirm credential source/readiness text does not show a secret value.
- Use `Test Connection` only when intentionally approving a real provider
  network call.
- Leave account/cloud flows out of scope; account sign-in is not shipped.

### History

- Enable history with synthetic text only.
- Translate a synthetic item.
- Open `History`, copy an entry, delete an entry, then clear history.
- Disable history if the tester does not want local text stored.

### Trust Prompt Or Unsigned-App Warning

When Windows shows an unsigned-app warning:

- record the exact package lane and artifact label;
- record whether the warning happened on launch, no-GUI bootstrap, or smoke;
- report the visible trust label in words;
- do not attach sensitive screenshots;
- do not change Windows security policy unless a maintainer explicitly approves
  a safe local test step.

## Known Limitations

- Signing is paused; artifacts are unsigned private-trial artifacts.
- No signed archive, installer, updater, release feed, or public release exists.
- Real provider network smoke is optional/manual and skipped unless credentials
  already exist and a human approves network use.
- Fake mode is not translation quality evidence.
- The deterministic `base` package is keyring-free.
- The `credentials` package is explicit and private-trial only.
- Broader Credential Locker/keyring behavior can vary by tester device,
  enterprise policy, lock state, and remote-session behavior.
- Assistive technology, DPI scaling, and multi-monitor checks remain
  device-specific.
- Global hotkeys, browser extension runtime, AI summary runtime, cloud sync,
  accounts, production OAuth, billing, hosted token broker, full localization,
  provider rewrites, and OCR/capture rewrites are not shipped.

## Accepted Baseline Revalidated

P21 remains the accepted baseline for P22:

- accepted P21 commit:
  `96b193e9c6dfbdae3f89c59d4bea76c500846a30`;
- planner P22 guide commit:
  `b85bda0918da4d6fc6e30ce239871f95b6e1eb8d`;
- current P22 dispatch HEAD:
  `38655382adb59b08e37ca251947d0800cd93e88c`;
- `main` is aligned with `origin/main`;
- P21 recorded signing state as PAUSED because no explicit safe
  throwaway/test signing path approval was supplied after P20;
- P21 did not run signing commands, create/import/purchase/invent/use
  certificates, call timestamp services, create signed artifacts, or approve
  public release;
- `base` remains the deterministic, keyring-free package lane;
- `credentials` remains explicit and private-trial only.

Round 1 revalidation results:

- `Validate.cmd` passed with 264 tests.
- `git diff --check` passed.
- `python -m snaplex --version` passed and reported `SnapLex 0.1.0`.
- `python -m snaplex --no-gui` passed.
- `python -m snaplex --check-real-provider` rejected missing real provider
  setup as expected.
- `python scripts\package_windows.py --dry-run --variant base` passed.
- `python scripts\package_windows.py --dry-run --variant credentials` passed.

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
present at the start of P22 editing.

## P22 Continuity Position

P22 continues private-trial operations only when these boundaries hold:

- fake smoke mode remains deterministic and visibly fake;
- real-provider paths fail closed when no real provider is configured;
- provider secrets stay out of docs, logs, screenshots, tests, package
  resources, config/history files, and git;
- package outputs and smoke data remain ignored local artifacts;
- tester feedback must use synthetic or non-sensitive text;
- screenshots and logs are not accepted when they contain sensitive content;
- `base` and `credentials` package lanes remain separate.

These notes supersede the P12 first-pilot release notes for the current P22
unsigned/private-trial continuity lane.

## Round 1 Self-Checks

Debug self-check:

- The result is explained by the smallest P22 starting workflow: accept P21,
  confirm current HEAD, confirm deterministic validation, confirm package
  dry-runs, and record that signing remains PAUSED.
- Success, expected rejection, missing real provider, paused signing, ignored
  local output, no-certificate, no-signing-command, no-artifact, and no-secret
  states are covered.

Architecture self-check:

- Rebaseline work does not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, release feed,
  cloud, OAuth, browser extension, AI summary, global hotkey, provider rewrite,
  OCR/capture rewrite, full localization, certificate, private key, signed
  artifact, timestamp response, or signing log is introduced.

## Round 2 Self-Checks

Debug self-check:

- The tester instructions are explained by the smallest P22 workflow: fake
  source/package smoke, fail-closed real-provider paths, explicit credentials
  smoke, unsigned trust label, and privacy-safe reporting.
- Success, expected rejection, missing real provider, paused signing, unsigned
  trust prompt, cleanup, no raw credential, no-artifact, and no-secret states
  are covered.

Architecture self-check:

- Tester instructions do not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, release feed,
  cloud, OAuth, browser extension, AI summary, global hotkey, provider rewrite,
  OCR/capture rewrite, full localization, certificate, private key, signed
  artifact, timestamp response, or signing log is introduced.
