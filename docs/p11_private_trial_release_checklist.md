# P11 Private Trial Release Checklist

Date: 2026-07-16
Phase: P11 Trial Release Hardening
Status: consolidated private-trial gate

Use this checklist before handing a local Windows SnapLex build to a private
tester. It consolidates the P11 visible GUI, credential, package, provider
onboarding, and no-secret release-hardening evidence.

## 1. Preflight Boundaries

- Confirm the working tree is clean except ignored generated artifacts:

  ```cmd
  git status --short --branch
  ```

- Do not stage or commit `build\`, `dist\`, `snaplex-smoke-data\`, `tmp\`,
  `.pytest_cache\`, `.env`, package binaries, screenshots, local config/history,
  logs, OCR model caches, keyring exports, or provider secrets.
- Keep fake smoke mode visibly fake and deterministic.
- Keep real provider tests optional/manual and credential-backed; real trial
  paths must not silently fall back to fake translation.
- Keep raw keys only in shell environment variables, ignored local launchers, or
  the optional local OS keyring.

## 2. Source Validation Gate

```cmd
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
git diff --check
python -m snaplex --version
python -m snaplex --no-gui
python -m snaplex --check-real-provider
```

Expected result:

- `Validate.cmd` passes with the current deterministic no-network suite.
- `git diff --check` passes.
- Version prints `SnapLex 0.1.0`.
- No-GUI bootstrap exits cleanly.
- `--check-real-provider` rejects missing real-provider configuration when no
  real credential or accepted endpoint is present.

## 3. Visible GUI Gate

```cmd
python scripts\p11_visible_gui_smoke.py
```

Expected result:

- The helper reports PASS on the native Windows Qt platform.
- It writes local screenshots under
  `snaplex-smoke-data\p11-visible-screenshots`.
- Main shell, fake result, long text, Settings, History, and focus states remain
  readable and operable.
- Screenshot artifacts remain ignored local files.

## 4. Credential Gate

Required deterministic evidence:

- `docs/p11_keyring_smoke_evidence.md` records the local keyring availability
  result or exact blocker.
- Source and provider setup tests cover mocked credential stores and no-secret
  config behavior.

Optional manual Windows Credential Locker/keyring smoke:

1. Use only a throwaway fake secret value.
2. Install `python -m pip install -e ".[gui,credentials]"` if keyring support is
   available locally.
3. Save the value through Settings with `Local secure credential`.
4. Confirm readiness shows a non-secret credential reference.
5. Relaunch with the same `SNAPLEX_APP_DATA_DIR` and confirm the value is still
   hidden.
6. Delete the credential through Settings.

## 5. Package Gate

```cmd
python scripts\package_windows.py --dry-run --variant base
SmokeTrial.cmd
StartPackagedFakeTrial.cmd --no-gui
StartPackagedTrial.cmd --no-gui
```

Expected result:

- Base package dry-run prints the deterministic PyInstaller command.
- `SmokeTrial.cmd` passes source bootstrap, package dry-run/build path, and
  packaged fake workflow smoke when `dist\SnapLex\SnapLex.exe` exists.
- `StartPackagedFakeTrial.cmd --no-gui` exits cleanly and labels fake smoke
  mode.
- `StartPackagedTrial.cmd --no-gui` fails closed when no real provider is
  configured.
- The base package does not require keyring, real provider credentials, network,
  screen permissions, OCR model downloads, or API keys.

## 6. Optional Real Provider Trial

Run this only when local credentials already exist and a human intentionally
approves a provider network call:

```cmd
StartTrial.cmd
```

Before launch:

- Configure a separate short-lived private-trial key with low quota/budget.
- Use environment variables or local secure credential references only.
- Run `python -m snaplex --check-real-provider`.
- Use `Test Connection` only when the network call is intentional.

Do not include real-provider network smoke in automated validation.

## 7. Cleanup And Evidence

After smoke, verify repository hygiene:

```cmd
git status --short --branch
git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs
```

Expected result:

- No generated package, screenshot, local data, env file, log, keyring export,
  OCR cache, or secret-bearing file is tracked.
- P11 evidence docs point to local ignored artifacts by path only, not their
  binary contents or secret values.

Evidence references:

- `docs/p11_visible_windows_smoke_evidence.md`
- `docs/p11_keyring_smoke_evidence.md`
- `docs/p11_keyring_packaging_decision.md`
- `docs/p11_packaged_trial_evidence.md`
- `docs/p11_provider_onboarding_notes.md`
- `docs/p11_key_rotation_least_privilege.md`
