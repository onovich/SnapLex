# P12 Private Trial Release Notes

Date: 2026-07-16
Phase: P12 Private Trial Pilot And Feedback Triage
Status: tester-facing draft ready for first private pilot

These notes are for the first controlled SnapLex private trial. The pilot is
for validating install/run paths, fake smoke mode, provider setup clarity,
Settings, History, package launch, and feedback quality. It is not a public
release and does not add new product features beyond the accepted P11 baseline.

## At A Glance

- Product: SnapLex `0.1.0`.
- Platform focus: Windows desktop.
- Default safe path: fake smoke mode, no credentials, no network.
- Real provider path: optional/manual only, requires a local private-trial
  provider key or accepted endpoint.
- Package path: deterministic `base` package for fake smoke and bootstrap.
- Secure credential path: source checkout plus optional `.[gui,credentials]`
  only; packaged keyring support is not promised in P12.

## Pilot Scope

Use the private pilot to check:

- source launch and no-GUI bootstrap;
- deterministic fake smoke mode from source and package;
- Settings provider setup clarity;
- History enable/list/copy/delete/clear behavior;
- visible desktop readability for shell, result states, Settings, History, long
  text, and focus;
- real-provider setup instructions, only when a tester already has a local
  private-trial provider key and intentionally chooses to run a network test;
- feedback intake quality and triage categories.

Do not use this pilot to validate production account sign-in, SnapLex Cloud,
billing, hosted token broker, browser extension runtime, AI summary runtime,
global hotkeys, full localization, provider rewrites, OCR/capture rewrites, or
packaged keyring support.

## Tester Privacy Rules

Do not paste or attach:

- provider API keys, bearer tokens, `.env` files, keyring exports, or local
  launchers containing secrets;
- screenshots containing private documents, private chats, account dashboards,
  personal data, credentials, or customer data;
- logs or config/history files that contain private text;
- package outputs, OCR model caches, or local app data directories;
- real names, email addresses, or personal contact details unless the tester
  intentionally wants them used for follow-up outside the repo.

When reporting a problem, use short synthetic sample text such as `hello`,
`invoice total`, or `screen hello`.

## Before You Start

Use a clean local checkout or the private package folder provided by the
release owner. Run commands from the repository root unless a packaged artifact
is explicitly provided.

For source-based testing, install the local trial dependencies:

```cmd
SetupTrial.cmd
```

For package-based testing, use the deterministic base package created by the
release owner, or build one locally:

```cmd
BuildTrial.cmd
```

Generated `build\`, `dist\`, `snaplex-smoke-data\`, screenshots, app data,
logs, `.env` files, keyring exports, and OCR caches are local artifacts. Do not
send or commit them.

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
smoke mode. It is not real translation.

Use fake smoke when checking:

- app launch and no-GUI bootstrap;
- main shell layout and focus;
- Settings and History behavior;
- package bootstrap and deterministic workflow smoke;
- feedback template quality.

### Real Provider Trial

Use real provider mode only when a local private-trial provider key or accepted
endpoint already exists:

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

Real provider smoke is optional/manual and may make a network call only when the
tester intentionally approves it.

Use a separate short-lived trial key with the lowest practical quota, budget,
and access. Rotate it after sharing a build or after any suspected exposure. See
`docs/p11_key_rotation_least_privilege.md`.

### Packaged Trial

The deterministic base package supports fake smoke and no-GUI bootstrap. The
base package does not promise local secure credential/keyring support in P12.
Use source checkout plus `.[gui,credentials]` for local secure credential testing
only when the optional `keyring` dependency is installed.

Recommended package checks:

```cmd
StartPackagedFakeTrial.cmd --no-gui
StartPackagedTrial.cmd --no-gui
```

Expected result:

- fake packaged trial exits cleanly and labels fake smoke mode;
- real packaged trial rejects missing real-provider configuration instead of
  silently using fake translation.

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
- Leave `Connect account (future)` disabled; account sign-in is not shipped.

### History

- Enable history with synthetic text only.
- Translate a synthetic item.
- Open `History`, copy an entry, delete an entry, then clear history.
- Disable history if the tester does not want local text stored.

### Package Smoke

- Run `SmokeTrial.cmd`.
- Confirm packaged smoke, when `dist\SnapLex\SnapLex.exe` exists, reports fake
  provider settings, clipboard translation, fake screen capture/OCR translation,
  and history clear PASS.

## Known Limitations

- Manual Windows Credential Locker smoke remains blocked in the executor
  environment because optional `keyring` support is not installed.
- Real provider network smoke has not been run by default.
- Assistive technology, DPI scaling, and multi-monitor checks need manual
  device-specific validation.
- The base package does not include or promise a credential-capable package
  variant.
- Fake mode is for smoke/dev validation only and is not translation quality
  evidence.
- Global hotkeys, browser extension runtime, AI summary runtime, cloud sync,
  accounts, production OAuth, billing, and hosted token broker are not shipped.

## Feedback Instructions

Use `docs/p12_feedback_intake_template.md` once it exists. Until then, include:

- command or workflow attempted;
- expected result;
- actual result;
- whether fake mode, real provider mode, or packaged mode was used;
- whether the issue blocks the first private pilot;
- environment notes such as Windows version, display scaling, monitor count, and
  whether assistive technology was active.

Do not include secrets, private documents, personal data, sensitive screenshots,
raw logs, `.env` files, keyring exports, or package artifacts.

## Round 1 Baseline Revalidation

The accepted P11 baseline was revalidated before preparing private-trial
materials:

- `Validate.cmd`: PASS with 255 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS, PySide6 bootstrap OK.
- `python -m snaplex --check-real-provider`: expected rejection PASS when no
  real provider is configured.
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: expected rejection PASS.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS.
- `cmd /c SmokeTrial.cmd`: PASS, including packaged executable smoke because a
  local `dist\SnapLex\SnapLex.exe` existed.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`: PASS.
- `cmd /c StartPackagedTrial.cmd --no-gui`: expected rejection PASS.
- `python scripts\p9_gui_smoke.py`: PASS with ignored local screenshots.
- `python scripts\p11_visible_gui_smoke.py`: PASS with ignored local
  screenshots.

Generated screenshots and smoke app data remain ignored local artifacts.
