# P15 Final Validation Report

Date: 2026-07-16
Phase: P15 Isolated Credential-Capable Package Spike Design Gate
Status: PASS - ready for planner acceptance

P15 completed the isolated credential-capable package spike design gate without
turning credential support into the deterministic base package. The spike added
an explicit `credentials` package variant and explicit credential smoke CLI,
proved packaged keyring import/backend discovery, proved packaged
save/read/delete/cleanup with runtime-generated throwaway values, proved
packaged restart readiness across two processes, preserved base package fake
smoke and real-trial fail-closed behavior, and decided to promote the work to a
later production hardening phase.

P15 is feasibility and design-gate evidence, not a production release promise.

## Rounds Used

- Round 1: rebaseline and package spike boundary.
- Round 2: packaging optional dependency audit and explicit `credentials`
  variant.
- Round 3: packaged keyring import/backend evidence.
- Round 4: packaged credential save/read/delete/cleanup smoke.
- Round 5: packaged restart readiness.
- Round 6: base package preservation.
- Round 7: cleanup guidance.
- Round 8: spike decision.
- Round 9: boundary scan evidence.
- Round 10: packaging and trial docs hardening.
- Round 11: Windows smoke checklist hardening.
- Round 12: final validation, report, and P16 handoff.

Buffer consumed: 0 repair buffer rounds. Rounds 9-11 were used for planned
hardening and hygiene rather than failed-round repair.

## Main Deliverables

- `docs/p15_packaging_spike_design.md`
- `docs/p15_packaged_keyring_import_evidence.md`
- `docs/p15_packaged_credential_smoke_evidence.md`
- `docs/p15_packaged_restart_readiness.md`
- `docs/p15_credential_cleanup_guidance.md`
- `docs/p15_package_spike_decision.md`
- `docs/p15_boundary_scan_evidence.md`
- `docs/p15_final_validation_report.md`
- `docs/p15_to_p16_handoff.md`

## Package Spike Design

P15 selected an explicit `credentials` package variant and `--smoke-credentials`
CLI. The base package remains the default deterministic fake smoke path and
explicitly excludes keyring support.

The `credentials` variant is invoked with:

```cmd
python scripts\package_windows.py --variant credentials
```

The smoke CLI supports:

- `--credential-smoke-mode import`
- `--credential-smoke-mode cycle`
- `--credential-smoke-mode save`
- `--credential-smoke-mode check-delete`

## Packaged Keyring Evidence

Credential variant build: PASS.

Observed PyInstaller evidence:

```text
Analyzing hidden import 'keyring.backends.Windows'
Processing standard module hook 'hook-keyring.py'
Processing standard module hook 'hook-pywintypes.py'
SNAPLEX_PACKAGE_VARIANT=credentials
```

Packaged import/backend discovery:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Result: PASS with `keyring.backends.Windows.WinVaultKeyring`.

## Packaged Credential Smoke

Packaged save/read/delete:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
```

Result: PASS.

```text
credential save/read/delete: PASS
credential cleanup: PASS
```

Packaged restart readiness:

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Result: PASS.

```text
credential restart readiness: PASS
credential cleanup: PASS
```

The smoke uses runtime-generated throwaway values and never prints them.

## Base Package Preservation

Base package dry-run: PASS.

```cmd
python scripts\package_windows.py --dry-run --variant base
```

Base build and fake package smoke: PASS.

```cmd
python scripts\package_windows.py --variant base
cmd /c SmokeTrial.cmd
cmd /c StartPackagedFakeTrial.cmd --no-gui
```

Base packaged real trial: expected rejection PASS.

```cmd
cmd /c StartPackagedTrial.cmd --no-gui
```

Base packaged credential smoke: expected rejection PASS.

```cmd
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

```text
SnapLex packaged credential smoke FAIL: keyring is not available in this runtime.
```

This confirms keyring was not silently added to the base package.

## Validation Commands And Results

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`:
  PASS with ruff, format check, mypy, compileall, and 261 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS, PySide6 bootstrap OK.
- `python -m snaplex --check-real-provider`: expected rejection PASS.
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `python scripts\package_windows.py --dry-run --variant credentials`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: expected rejection PASS.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS with visible fake smoke label.
- `cmd /c SmokeTrial.cmd`: PASS.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`: PASS.
- `cmd /c StartPackagedTrial.cmd --no-gui`: expected rejection PASS.
- `python scripts\p9_gui_smoke.py`: PASS with seven ignored local screenshots.
- `python scripts\p11_visible_gui_smoke.py`: PASS with six ignored local
  screenshots.
- Current base package credential smoke: expected rejection PASS.
- P15 docs link/index check: PASS.
- Artifact scan: PASS; no tracked `build`, `dist`, `snaplex-smoke-data`, `tmp`,
  `.pytest_cache`, `.env`, logs, caches, screenshots, OCR model caches, or
  smoke data.
- Secret pattern scan: PASS; no real provider keys, bearer tokens, `.env`,
  keyring exports, logs, screenshots, package resources, tester data, or API
  response captures found in tracked content.

## Package Spike Decision

Decision: promote to later production hardening phase, but do not ship P15 as a
production credential-capable package release.

Reasons to promote:

- packaged keyring import/backend discovery passed;
- packaged save/read/delete/cleanup passed;
- packaged restart readiness passed;
- base package remained deterministic and excluded keyring;
- real trial paths remained fail-closed without real provider configuration.

Reasons not to ship yet:

- tester-facing credential package UX and release notes need hardening;
- unavailable/locked keyring backend failure paths need release polish;
- installer/updater and support policy are not defined;
- no real-provider network smoke was run in P15;
- P15 did not define a signed distributable or rollout plan.

## Credential And Privacy Handling

- Raw provider key values were not used, printed, stored, logged, screenshotted,
  packaged, or committed.
- Throwaway credential values were generated at runtime and cleaned up.
- Keyring evidence records only non-secret reference identifiers.
- Package outputs and smoke data remain ignored local artifacts.
- Real-provider network smoke remains optional and requires existing local
  credentials plus explicit human network approval.

## Architecture Notes

Providers remain behind `TranslationProvider`, provider registry, and
`TranslationPipeline`. Credential behavior remains behind `CredentialService`,
credential stores, SettingsService/SettingsPresenter, provider setup, and trial
readiness. Packaging remains a thin explicit variant/hidden-import wrapper and
does not own provider, credential, settings, history, OCR, capture, or UI
business rules.

## Known Limitations

- P15 does not ship a production credential-capable package.
- The current base package intentionally rejects credential smoke because
  keyring is absent.
- P15 did not run real-provider network smoke.
- P15 did not test enterprise keyring restrictions, locked credential stores,
  signed installer behavior, or updater behavior.
- Package outputs under `build\` and `dist\` are local ignored artifacts and are
  not committed.

## Commit Hashes

- `ee68bb7` docs: record P15 dispatch
- `1825a53` p15: define package spike boundary
- `0e5a626` p15: add explicit credentials package variant
- `2b0d8a5` p15: prove packaged keyring import
- `817f048` p15: prove packaged credential cycle
- `1e193f2` p15: prove packaged restart readiness
- `ff771e6` p15: preserve base package path
- `a8b2e89` p15: document credential cleanup
- `35e3805` p15: decide package hardening path
- `a68403c` p15: record boundary scan evidence
- `1117607` p15: document credential package smoke
- `3a34955` p15: harden smoke checklist

## Request For Acceptance

P15 is ready for planner/architect review. Recommended P16:
Credential-Capable Package Production Hardening.
