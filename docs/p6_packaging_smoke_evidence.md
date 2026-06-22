# P6 Packaging Smoke Evidence

Date: 2026-06-22
Phase: P6 Packaging and Release Readiness
Variant: `base`

## Build Environment

- Python: 3.14.3
- PyInstaller: 6.21.0
- PySide6: available
- Package command:

```powershell
python scripts\package_windows.py --variant base
```

Generated output:

```text
dist\SnapLex\SnapLex.exe
```

Generated build/work output:

```text
build\pyinstaller\
dist\SnapLex\
```

Both locations are ignored and must not be committed.

## Build Result

Status: PASS

PyInstaller completed successfully and reported:

```text
Build complete! The results are available in: D:\ToolProjects\SnapLex\dist
```

An initial package smoke failed because PyInstaller executed
`snaplex\__main__.py` without package context. P6 fixed the bootstrap entry by
using an absolute `snaplex.app` import. Source bootstrap and packaged bootstrap
then both passed.

## Packaged Bootstrap Smoke

Command:

```powershell
$env:SNAPLEX_APP_DATA_DIR='D:\ToolProjects\SnapLex\snaplex-smoke-data\round4'
.\dist\SnapLex\SnapLex.exe --version
.\dist\SnapLex\SnapLex.exe --no-gui
```

Result:

```text
SnapLex 0.1.0
SnapLex bootstrap OK (PySide6 available).
```

Status: PASS

## Packaged GUI Launch Smoke

Command:

```powershell
$env:SNAPLEX_APP_DATA_DIR='D:\ToolProjects\SnapLex\snaplex-smoke-data\round4-gui'
$env:SNAPLEX_PROVIDER='fake'
$p = Start-Process -FilePath '.\dist\SnapLex\SnapLex.exe' -PassThru
Start-Sleep -Seconds 5
if ($p.HasExited) { throw "GUI launch exited early with code $($p.ExitCode)" } else {
  Stop-Process -Id $p.Id
  'Packaged GUI launch smoke PASS'
}
```

Result:

```text
Packaged GUI launch smoke PASS
```

Status: PASS

## Packaged Workflow Smoke

Command:

```powershell
$env:SNAPLEX_APP_DATA_DIR='D:\ToolProjects\SnapLex\snaplex-smoke-data\round5-packaged'
.\dist\SnapLex\SnapLex.exe --smoke-package
```

Result:

```text
SnapLex packaged workflow smoke PASS
- app data: D:\ToolProjects\SnapLex\snaplex-smoke-data\round5-packaged
- settings persistence: fake provider, history enabled
- clipboard translation: hello -> hello [en]
- screen fake capture/OCR translation: screen hello -> screen hello [en]
- history record/list/delete/clear: PASS
```

Status: PASS

This smoke runs inside the packaged executable and exercises existing service
boundaries:

- `SettingsService -> JsonFileConfigStore`
- `InMemoryClipboardService -> TranslationPipeline`
- `HistoryService -> JsonFileHistoryStore`
- `FakeCaptureService -> FakeOcrService -> TranslationPipeline`

Real `mss` capture and PaddleOCR packaging remain optional variant/manual smoke
paths. The default `base` package intentionally avoids bundling OCR model caches
or requiring screen permissions, model downloads, provider network calls, or API
keys.

## Cleanup

Smoke data and package artifacts are local generated outputs. They are ignored
by git and can be removed after release validation:

```powershell
Remove-Item -Recurse -Force build,dist,snaplex-smoke-data
```
