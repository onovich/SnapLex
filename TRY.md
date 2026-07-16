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
provider. Configure at least one provider before launching. SnapLex stores only
environment variable names or keyring identifiers; never paste a provider key
into docs, screenshots, commits, issues, or chat.

```powershell
$env:SNAPLEX_OPENAI_API_KEY = "your_trial_key"
$env:SNAPLEX_DEEPL_API_KEY = "your_trial_key"
$env:SNAPLEX_LIBRETRANSLATE_BASE_URL = "http://localhost:5000"
```

`StartTrial.cmd` auto-selects OpenAI, DeepL, or LibreTranslate from those
environment variables. The default target language is `zh`. Trial data is
written under `snaplex-smoke-data\trial-real-source`, which is ignored by git.
If none of those real provider settings exists, the command exits with a clear
message instead of falling back to fake translation.

Use a separate private-trial provider key with the lowest practical quota,
budget, and access. Rotate it before sharing a build with another tester and
after any suspected exposure.

If you already use standard provider variables, `OPENAI_API_KEY` and
`DEEPL_API_KEY` are also detected.

For local OS keyring setup, install the optional credentials extra and save the
secret through Settings. SnapLex stores only the non-secret keyring identifier:

```powershell
python -m pip install -e ".[gui,credentials]"
$env:SNAPLEX_PROVIDER = "openai"
$env:SNAPLEX_PROVIDER_ORDER = "openai"
$env:SNAPLEX_OPENAI_CREDENTIAL_SOURCE = "keyring"
$env:SNAPLEX_OPENAI_CREDENTIAL_IDENTIFIER = "snaplex/openai/default"
python -m snaplex
```

After saving the credential in Settings, verify readiness without a network
call:

```cmd
python -m snaplex --check-real-provider
```

For a bootstrap-only check:

```cmd
.\StartTrial.cmd --no-gui
```

For UI smoke without real translation:

```cmd
.\StartFakeTrial.cmd
```

Use fake trial commands when you want to test the interface or package without
real translation. Fake output is deterministic placeholder text and is visibly
labeled as fake smoke mode.

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

See `docs\p10_account_strategy.md` for environment-variable, OS keyring,
SnapLex Cloud, token broker, and provider account/OAuth tradeoffs. Do not paste
real provider secrets into docs, screenshots, issues, commits, or chat logs.
See `docs\p11_provider_onboarding_notes.md` for the private-trial provider
setup paths and current packaging decision. See
`docs\p11_key_rotation_least_privilege.md` for key rotation, cleanup, and
least-privilege guidance.

For P12 private pilot testers, see `docs\p12_private_trial_release_notes.md`.
For maintainers collecting reports, use
`docs\p12_feedback_intake_template.md`,
`docs\p12_trial_pass_fail_criteria.md`, and
`docs\p12_trial_triage_workflow.md`.

## 6. Optional Credential Package Spike

P15 introduces an explicit credential-capable package spike. This is for
maintainer validation only and is not the default trial package:

```cmd
python scripts\package_windows.py --variant credentials
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
```

For packaged restart readiness, run two separate processes:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

These commands use only runtime-generated throwaway values and must not print,
log, screenshot, export, or commit credential values. The deterministic base
package remains the normal fake smoke path.

See `docs\p15_credential_cleanup_guidance.md` before and after running package
credential smoke.
