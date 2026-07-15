# P12 Private Trial Release Notes

Date: 2026-07-16
Phase: P12 Private Trial Pilot And Feedback Triage
Status: draft outline after baseline revalidation

These notes are for the first controlled SnapLex private trial. The pilot is
for validating install/run paths, fake smoke mode, provider setup clarity,
Settings, History, package launch, and feedback quality. It is not a public
release and does not add new product features beyond the accepted P11 baseline.

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

### Packaged Trial

The deterministic base package supports fake smoke and no-GUI bootstrap. The
base package does not promise local secure credential/keyring support in P12.
Use source checkout plus `.[gui,credentials]` for local secure credential testing
only when the optional `keyring` dependency is installed.

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

## Feedback Linkage

Use `docs/p12_feedback_intake_template.md` once it exists. Until then, record
only synthetic sample text, the command or workflow attempted, expected result,
actual result, environment notes, and whether the issue blocks the first private
pilot.
