# P20 Validation Precheck Evidence

Date: 2026-07-17
Phase: P20 Approved Signing Path Acquisition And Rehearsal Setup Gate
Status: PASS

P20 round 11 rechecked final-round prerequisites after signing was recorded as
BLOCKED/SKIPPED, package lanes were validated, and boundary evidence was
committed.

## Docs And Diff Checks

Command:

```powershell
python -c "from pathlib import Path; files=['docs/p20_approved_signing_path_acquisition_rehearsal_setup_gate_goal_guide.md','docs/p20_todo.md','docs/p20_signing_path_approval_record.md','docs/p20_rehearsal_artifact_directory_policy.md','docs/p20_signing_command_discovery.md','docs/p20_isolated_rehearsal_evidence.md','docs/p20_signature_verification_evidence_policy.md','docs/p20_base_package_control_evidence.md','docs/p20_credentials_package_control_evidence.md','docs/p20_boundary_scan_evidence.md']; missing=[f for f in files if not Path(f).exists()]; assert not missing, missing; readme=Path('README.md').read_text(encoding='utf-8'); agents=Path('AGENTS.md').read_text(encoding='utf-8'); smoke=Path('docs/windows_smoke_checklist.md').read_text(encoding='utf-8'); required=files[2:]; assert all(s in readme for s in required), 'README missing'; assert all(s in agents for s in required), 'AGENTS missing'; assert all(s in smoke for s in required), 'smoke missing'; print('P20 docs link/index check PASS')"
```

Result: PASS.

Command:

```powershell
git diff --check
```

Result: PASS.

## CLI Checks

Command:

```powershell
python -m snaplex --version
```

Result: PASS, `SnapLex 0.1.0`.

Command:

```powershell
python -m snaplex --no-gui
```

Result: PASS.

Command:

```powershell
python -m snaplex --check-real-provider
```

Result: PASS as expected rejection. Missing real provider setup was rejected.

## Package Dry-Runs

Command:

```powershell
python scripts\package_windows.py --dry-run --variant base
```

Result: PASS.

Command:

```powershell
python scripts\package_windows.py --dry-run --variant credentials
```

Result: PASS.

## Trial Launchers

Command:

```powershell
cmd /c StartTrial.cmd --no-gui
```

Result: PASS as expected rejection. Missing real provider setup was rejected.

Command:

```powershell
cmd /c StartFakeTrial.cmd --no-gui
```

Result: PASS.

Command:

```powershell
cmd /c StartPackagedFakeTrial.cmd --no-gui
```

Result: PASS.

Command:

```powershell
cmd /c StartPackagedTrial.cmd --no-gui
```

Result: PASS as expected rejection. Missing real provider setup was rejected.

Command:

```powershell
cmd /c SmokeTrial.cmd
```

Result: PASS. Base packaged workflow smoke passed with fake provider.

Command:

```powershell
.\dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS as expected rejection. Output reported:
`keyring is not available in this runtime`.

## GUI Smoke

Command:

```powershell
python scripts\p9_gui_smoke.py
```

Result: PASS. Screenshots were written under ignored
`snaplex-smoke-data\p9-screenshots`.

Command:

```powershell
python scripts\p11_visible_gui_smoke.py
```

Result: PASS. Screenshots were written under ignored
`snaplex-smoke-data\p11-visible-screenshots`.

## Round 11 Self-Checks

Debug self-check:

- The evidence is explained by the smallest final-precheck workflow: docs
  exist and are indexed, diff is clean, CLI works, real provider paths fail
  closed, dry-runs pass, fake/package smoke remains green, base remains
  keyring-free, and GUI smoke remains green.
- Success, expected rejection, skipped signing, no certificate, no signed
  artifact, no timestamp response, screenshot under ignored path, and
  no-secret states are covered.

Architecture self-check:

- Precheck validation does not change provider, credential, settings, history,
  capture, OCR, UI, package specification, or trial readiness behavior.
- Providers remain behind provider registry and `TranslationPipeline`.
- Credentials remain behind credential services, stores, settings, provider
  setup, and trial readiness.
- The base package remains deterministic and keyring-free.
- The `credentials` package remains explicit and private-trial.
- No public release, production signing, installer, updater, cloud, OAuth,
  browser extension, AI summary, global hotkey, provider rewrite, OCR/capture
  rewrite, full localization, certificate, private key, signed artifact,
  timestamp response, or signing log is introduced.
