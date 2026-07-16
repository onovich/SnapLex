# SnapLex Windows Packaging

P6 uses PyInstaller for the Windows MVP package. Install the packaging toolchain
without enabling heavyweight optional OCR dependencies:

```powershell
python -m pip install -e ".[gui,package]"
```

Build a console-mode package for repeatable launch smoke:

```powershell
python scripts\package_windows.py
```

The default command uses the tracked spec at `packaging\snaplex.spec`. Use
`--no-spec` only when diagnosing PyInstaller option changes locally.

The tracked spec supports dependency variants:

- `base`: GUI package with fake/offline capture and OCR services for smoke.
- `capture`: additionally includes optional `mss` modules when installed.
- `ocr`: additionally includes optional `paddleocr` modules when installed.
- `full`: includes both optional capture and OCR module families when installed.
- `credentials`: explicit P15 spike variant that includes optional local
  keyring modules for credential smoke. This is not the default release smoke
  path.

Use variants explicitly:

```powershell
python scripts\package_windows.py --variant capture
python scripts\package_windows.py --variant full
python scripts\package_windows.py --variant credentials
```

Preview the exact PyInstaller command without building:

```powershell
python scripts\package_windows.py --dry-run
```

The `base` variant is the deterministic release-smoke path. It does not package
PaddleOCR model caches, does not require real provider credentials, and does
not require the optional `keyring` dependency. The `credentials` variant is an
explicit spike/manual validation path for packaged keyring behavior. Generated
output stays under `build\` and `dist\`. Do not commit those folders, packaged
executables, local smoke data, provider secrets, OCR model caches, or
screenshots.

P10 local secure credential support is optional and lazy. Source trials can
install `python -m pip install -e ".[gui,credentials]"` to use the OS keyring.
Do not add keyring secrets, exports, config files, or provider keys to package
resources. If a distributable package is expected to support OS keyring storage,
build it from an environment with the credentials extra installed and run a
manual credential smoke with a throwaway key before distribution.

## Smoke

Run packaged smoke with an explicit local app data directory:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexPackageSmoke"
.\dist\SnapLex\SnapLex.exe --version
.\dist\SnapLex\SnapLex.exe --no-gui
.\dist\SnapLex\SnapLex.exe --smoke-package
```

`--smoke-package` runs inside the packaged executable and checks settings
persistence, fake-provider clipboard translation, fake capture/OCR screen
translation, history record/list/delete/clear, and local data path containment.

For the P11 private-trial release gate, also run the command wrappers:

```cmd
SmokeTrial.cmd
StartPackagedFakeTrial.cmd --no-gui
StartPackagedTrial.cmd --no-gui
```

Expected result:

- Fake trial paths pass and remain visibly labeled as fake smoke mode.
- Real packaged trial fails closed when no real provider credential or accepted
  endpoint exists.
- The deterministic base package remains usable without keyring, real provider
  credentials, network, screen permissions, model downloads, or API keys.

See `docs\p11_private_trial_release_checklist.md` for the full P11 gate.

## Credential Package Spike Smoke

P15 adds an explicit credential-capable spike path. Build it only when you are
validating packaged keyring behavior:

```powershell
python scripts\package_windows.py --variant credentials
```

Run import/backend discovery without saving a credential:

```powershell
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Run save/read/delete with a runtime-generated throwaway value:

```powershell
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
```

Run restart readiness as two separate packaged processes:

```powershell
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Expected result:

- The `credentials` variant reports Windows keyring backend discovery.
- Smoke output never prints the throwaway credential value.
- `cycle` and `check-delete` clean up the smoke credential before exit.
- The base package remains the default deterministic fake smoke path.

See `docs\p15_packaging_spike_design.md`,
`docs\p15_packaged_keyring_import_evidence.md`,
`docs\p15_packaged_credential_smoke_evidence.md`, and
`docs\p15_packaged_restart_readiness.md`.

## Troubleshooting

- `No module named PyInstaller`: run `python -m pip install -e ".[package]"`.
- PySide6 import or Qt plugin failures: rebuild after installing
  `python -m pip install -e ".[gui,package]"`.
- Missing `mss` or PaddleOCR in optional variants: install `.[capture]`,
  `.[ocr]`, or both before using `--variant capture`, `--variant ocr`, or
  `--variant full`.
- Missing keyring support: install `.[credentials]` for source trials, or build
  the explicit `credentials` variant for P15 packaged keyring smoke. The
  deterministic base package smoke path does not depend on keyring.
- Provider credential errors: use fake provider smoke first. Real provider
  smoke depends on local environment variables, local OS keyring state, or a
  self-hosted endpoint and must not put key values into config files, docs,
  logs, screenshots, or package resources.
- History/config smoke writes to `SNAPLEX_APP_DATA_DIR`. Set it to a temporary
  directory before running package smoke.

## Cleanup

```powershell
Remove-Item -Recurse -Force build,dist
Remove-Item -Recurse -Force D:\Temp\SnapLexPackageSmoke
```

Only delete directories you explicitly created for local smoke.
