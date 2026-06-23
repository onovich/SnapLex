# SnapLex Trial Commands

Run these commands from the repository root on Windows PowerShell. You can also
double-click the `.cmd` files in Explorer.

## 1. Install Trial Dependencies

```cmd
.\SetupTrial.cmd
```

This installs the GUI and packaging extras needed for local trial runs and the
base Windows package.

## 2. Start From Source

```cmd
.\StartTrial.cmd
```

This starts the PySide6 desktop shell from source with the fake provider by
default. Trial data is written under `snaplex-smoke-data\trial-source`, which
is ignored by git.

For a bootstrap-only check:

```cmd
.\StartTrial.cmd --no-gui
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

## 4. Start The Packaged Trial

```cmd
.\StartPackagedTrial.cmd
```

This starts `dist\SnapLex\SnapLex.exe` with the fake provider by default. Run
`BuildTrial.cmd` first if the executable does not exist.

For a packaged bootstrap-only check:

```cmd
.\StartPackagedTrial.cmd --no-gui
```

## 5. Run Trial Smoke Checks

```cmd
.\SmokeTrial.cmd
```

This runs source bootstrap checks, a package dry-run, and packaged executable
smoke checks when `dist\SnapLex\SnapLex.exe` exists.
