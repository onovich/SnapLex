# P17 Final Validation Report

Date: 2026-07-17
Phase: P17 Limited Credential Package Pilot And Signing Decision
Status: PASS - ready for planner check
Final commit: final docs commit containing this report; see READY_FOR_CHECK
planner message for hash
Push: PASS after final docs commit
Rounds used: 12 of 12
Buffer consumed: 3 planned hygiene/hardening rounds; 0 repair buffer rounds.

P17 ran a controlled, privacy-safe pilot lane for the explicit unsigned
`credentials` package candidate approved by P16. The deterministic `base`
package remains the default keyring-free package lane. The `credentials`
package remains a separate unsigned/private-trial variant and is not approved
as a public release.

## Main Deliverables

- `docs/p17_pilot_lane_plan.md`
- `docs/p17_package_candidate_gate_evidence.md`
- `docs/p17_tester_feedback_intake.md`
- `docs/p17_real_provider_smoke_record.md`
- `docs/p17_artifact_transfer_retention_support.md`
- `docs/p17_signing_installer_updater_decision.md`
- `docs/p17_credential_package_lane_decision.md`
- `docs/p17_boundary_scan_evidence.md`
- `docs/p17_final_validation_report.md`
- `docs/p17_to_p18_handoff.md`

## Pilot Lane

P17 defined a controlled private tester lane for one to three trusted testers or
maintainer-owned Windows test machines. The candidate artifact must be labeled
with source commit, `credentials` variant, date, and unsigned/private-trial
status.

No public distribution, signed installer, updater, base-package keyring
support, cloud accounts, OAuth, billing, token broker, browser extension, AI
summary, global hotkey, broad provider rewrite, OCR/capture rewrite, or full
localization is approved.

## Package Candidate Gate Evidence

Credential package candidate gate: PASS.

Evidence:

- source validation gate passed;
- `base` and `credentials` dry-runs passed;
- base package build and fake smoke passed;
- base credential smoke rejected keyring as unavailable;
- credentials package build passed;
- credentials build analyzed `keyring.backends.Windows`;
- credential import discovered `keyring.backends.Windows.WinVaultKeyring`;
- credential cycle passed save/read/delete and cleanup;
- credential save/check-delete passed restart readiness and cleanup;
- cleanup status returned to `missing`;
- final local `dist\SnapLex` was restored to the base package lane.

## Tester Feedback

No external tester feedback was supplied in this executor session. P17 does not
fabricate tester reports.

Internal pilot blockers carried forward:

- no real external tester device matrix has exercised locked Windows Credential
  Locker, enterprise keyring policy, unsupported backend, or remote-session
  behavior in P17;
- no real-provider network smoke was approved;
- no external artifact transfer/support loop has been executed.

## Real Provider Smoke

Optional real-provider network smoke was skipped honestly.

Reason:

- no existing local credentials and explicit human network approval were
  supplied in this executor session;
- automated validation must remain deterministic and no-network.

Fail-closed evidence:

- `python -m snaplex --check-real-provider`: expected rejection PASS.
- `cmd /c StartTrial.cmd --no-gui`: expected rejection PASS.
- `cmd /c StartPackagedTrial.cmd --no-gui`: expected rejection PASS.

## Artifact Transfer, Retention, And Support

P17 records private artifact transfer, finite retention, and support escalation
policy in `docs/p17_artifact_transfer_retention_support.md`.

Policy summary:

- transfer only a selected `credentials` artifact after gates pass;
- keep package outputs local/ignored and out of git;
- retain artifacts only until accepted, rejected, or superseded;
- escalate launch, keyring, cleanup, secret-leak, and base keyring regressions;
- reject or request resubmission for reports containing secrets or personal
  data.

## Signing, Installer, And Updater Decision

Decision: defer signing, installer, and updater implementation beyond P17.

The P17 credential package remains unsigned/private-trial only. A later phase
must define signing identity, installer/archive format, update and rollback
policy, artifact retention/revocation, and support communication before wider
distribution.

## Credential Package Lane Decision

Decision: keep credentials as a separate explicit package variant.

The `base` package remains deterministic, keyring-free, and fake-smoke capable.
The `credentials` package may continue only as an explicit
`--variant credentials` private-trial lane under source/base/credential/artifact
and secret gates.

## Validation Commands And Results

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`:
  PASS with ruff, format check, mypy, compileall, and 264 tests.
- `git diff --check`: PASS.
- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS.
- `python -m snaplex --check-real-provider`: expected rejection PASS.
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `python scripts\package_windows.py --dry-run --variant credentials`: PASS.
- `python scripts\package_windows.py --variant credentials`: PASS.
- Credentials package import smoke: PASS.
- Credentials package cycle smoke: PASS.
- Credentials package save/check-delete restart readiness: PASS.
- Credentials package cleanup status: PASS, `missing`.
- `python scripts\package_windows.py --variant base`: PASS after credentials
  smoke, restoring local `dist` to base.
- `cmd /c StartTrial.cmd --no-gui`: expected rejection PASS.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS.
- `cmd /c SmokeTrial.cmd`: PASS.
- `cmd /c StartPackagedFakeTrial.cmd --no-gui`: PASS.
- `cmd /c StartPackagedTrial.cmd --no-gui`: expected rejection PASS.
- Base package credential smoke: expected rejection PASS with keyring
  unavailable.
- `python scripts\p9_gui_smoke.py`: PASS with seven ignored local screenshots.
- `python scripts\p11_visible_gui_smoke.py`: PASS with six ignored local
  screenshots.
- P17 docs link/index check: PASS.
- Artifact boundary scan: PASS.
- Secret pattern scan: PASS.

## Boundary And Secret Scan

Boundary evidence is recorded in `docs/p17_boundary_scan_evidence.md`.

Final scans confirmed:

- no tracked generated package outputs, screenshots, local app data, `.env`,
  logs, OCR caches, keyring exports, smoke data, tester personal data, or
  provider secrets;
- no real provider keys, bearer tokens, private keys, GitHub tokens, keyring
  exports, or API response captures in tracked content;
- only documented `your_trial_key` placeholders appear in provider setup
  examples.

## Known Limitations

- P17 does not produce a public release.
- P17 does not produce a signed installer or updater.
- External tester feedback was not supplied.
- Real-provider network smoke was not run because no existing local credentials
  and explicit human network approval were supplied.
- Locked Credential Locker, enterprise policy, unsupported backend, and
  remote-session behavior still need a tester device matrix.
- Package artifacts under `build\` and `dist\` are local ignored outputs and
  are not committed.

## Recommended Next Phase

Recommended P18: Signing And Distribution Readiness Gate.

Suggested P18 scope:

- decide signing identity, certificate custody, and verification workflow;
- decide archive versus installer and rollback/update policy;
- run a signed or signing-rehearsal package spike only if explicitly approved;
- keep base package deterministic and keyring-free;
- keep the credential package explicit and private-trial until signing/support
  gates pass;
- continue collecting no-secret tester evidence before broader distribution.
