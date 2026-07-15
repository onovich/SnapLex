# SnapLex Trial Commands

Run these commands from the repository root on Windows PowerShell. You can also
double-click the `.cmd` files in Explorer.

## 1. Install Trial Dependencies

```cmd
.\SetupTrial.cmd
```

This installs the GUI and packaging extras needed for local trial runs and the
base Windows package.

## 2. Start From Source With Real Translation

```cmd
.\StartTrial.cmd
```

This starts the PySide6 desktop shell from source with a real translation
provider. Configure at least one provider before launching:

```powershell
$env:SNAPLEX_OPENAI_API_KEY = "your_key"
$env:SNAPLEX_DEEPL_API_KEY = "your_key"
$env:SNAPLEX_LIBRETRANSLATE_BASE_URL = "http://localhost:5000"
```

`StartTrial.cmd` auto-selects OpenAI, DeepL, or LibreTranslate from those
environment variables. The default target language is `zh`. Trial data is
written under `snaplex-smoke-data\trial-real-source`, which is ignored by git.
If none of those real provider settings exists, the command exits with a clear
message instead of falling back to fake translation.

If you already use standard provider variables, `OPENAI_API_KEY` and
`DEEPL_API_KEY` are also detected.

For a bootstrap-only check:

```cmd
.\StartTrial.cmd --no-gui
```

For UI smoke without real translation:

```cmd
.\StartFakeTrial.cmd
```

## 3. Build The Packaged Trial

```cmd
.\BuildTrial.cmd
```

This creates the deterministic base package:

```text
dist\SnapLex\SnapLex.exe
```

Generated `build\` and `dist\` folders are ignored by git.

## 4. Start The Packaged Trial With Real Translation

```cmd
.\StartPackagedTrial.cmd
```

This starts `dist\SnapLex\SnapLex.exe` with a real translation provider. Run
`BuildTrial.cmd` first if the executable does not exist. Configure OpenAI,
DeepL, or LibreTranslate as shown above before launching.
The packaged real trial path also rejects missing real provider configuration.

For a packaged bootstrap-only check:

```cmd
.\StartPackagedTrial.cmd --no-gui
```

For packaged UI smoke without real translation:

```cmd
.\StartPackagedFakeTrial.cmd
```

## 5. Run Trial Smoke Checks

```cmd
.\SmokeTrial.cmd
```

This runs source bootstrap checks, a package dry-run, and packaged executable
smoke checks when `dist\SnapLex\SnapLex.exe` exists.

`SmokeTrial.cmd`, `StartFakeTrial.cmd`, and `StartPackagedFakeTrial.cmd` use the
fake provider by design. Fake mode returns deterministic placeholder text such
as `hello [zh]`; it is only for packaging and UI smoke, not real translation.
The desktop result view labels fake output as fake smoke mode.
