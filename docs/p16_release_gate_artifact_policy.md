# P16 Release Gate And Artifact Policy

Date: 2026-07-17
Phase: P16 Credential-Capable Package Production Hardening
Status: release gate and artifact policy defined

P16 does not make the credential-capable package a broad public release. This
policy defines the minimum gate for a controlled private-trial credential
package candidate and keeps the deterministic base package path unchanged.

## Package Lanes

| Lane | Variant | Purpose | Credential support |
| --- | --- | --- | --- |
| Base smoke lane | `base` | Deterministic fake package smoke and default package validation | No keyring; credential smoke must fail with keyring unavailable. |
| Credential candidate lane | `credentials` | Controlled private-trial credential package hardening | Explicit keyring support and `--smoke-credentials` only. |

The base lane remains the default. The credential candidate lane must be
requested explicitly.

## Source Gate

Before producing any package candidate:

- work from a clean git status;
- record the source commit;
- run `Validate.cmd`;
- run `git diff --check`;
- run `python -m snaplex --version`;
- run `python -m snaplex --no-gui`;
- run `python -m snaplex --check-real-provider` and expect rejection unless a
  real provider is intentionally configured for a separate manual smoke;
- run base and credentials package dry-runs.

Do not package from uncommitted source changes unless the build is clearly
labeled as local throwaway debugging and never shared.

## Base Lane Gate

Required commands:

```cmd
python scripts\package_windows.py --variant base
cmd /c SmokeTrial.cmd
cmd /c StartPackagedFakeTrial.cmd --no-gui
cmd /c StartPackagedTrial.cmd --no-gui
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
```

Expected results:

- base build exits 0;
- fake package smoke exits 0;
- packaged fake trial exits 0 and is visibly fake;
- packaged real trial rejects missing real-provider setup;
- credential smoke rejects keyring with
  `keyring is not available in this runtime`.

## Credential Candidate Gate

Required commands:

```cmd
python scripts\package_windows.py --variant credentials
dist\SnapLex\SnapLex.exe --version
dist\SnapLex\SnapLex.exe --no-gui
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode cycle
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode save
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode check-delete
```

Expected results:

- credentials build exits 0;
- PyInstaller output includes `keyring.backends.Windows`;
- version and no-gui smoke pass;
- import reports `keyring.backends.Windows.WinVaultKeyring`;
- cycle reports save/read/delete and cleanup PASS;
- save then check-delete reports restart readiness and cleanup PASS;
- output includes `snaplex/package-credential-smoke`;
- output never includes raw credential values.

## Evidence Gate

Every private-trial package candidate must have a short evidence note that
records:

- source commit;
- package lane and variant;
- commands run;
- pass/fail/blocker result;
- keyring backend label when credential smoke runs;
- cleanup status;
- whether real-provider network smoke was skipped or explicitly approved;
- artifact location.

Evidence must not include:

- raw provider keys;
- throwaway smoke values;
- `.env` contents;
- keyring exports;
- screenshots containing secrets;
- local app data, logs, or provider API responses.

## Artifact Handling

Generated package artifacts stay local and ignored by git:

- `build\`
- `dist\`
- `snaplex-smoke-data\`
- `tmp\`
- `.pytest_cache\`

Do not commit package outputs, installers, screenshots, logs, local config or
history, smoke data, OCR caches, or keyring exports.

For a controlled private trial, attach or transfer only the packaged folder
explicitly selected for that tester lane. Name or label the artifact with:

- `SnapLex`
- source commit prefix;
- package lane, such as `base` or `credentials`;
- date;
- unsigned/signed status.

## Signing And Installer Policy

P16 does not create a signed installer or updater. A credential-capable package
candidate is acceptable only as an unsigned controlled private-trial artifact
unless a later phase defines signing and installer gates.

Before broader distribution, a later phase must decide:

- code-signing identity and signing process;
- installer or archive format;
- update and rollback behavior;
- artifact retention policy;
- support contact and escalation path;
- whether credential-capable packaging remains a separate variant.

## Real-Provider Network Smoke Policy

Automated validation must remain no-network. Optional real-provider smoke is
manual only and requires:

- existing local credentials;
- explicit human approval in that executor session;
- no credential values in output, screenshots, docs, commits, logs, or chat;
- clear pass/fail/blocker evidence that omits translated private text.

If those conditions are not met, record real-provider smoke as skipped and rely
on fail-closed readiness checks.

## Release Decision Gate

Credential package candidate distribution is allowed only when:

- base lane gate passes;
- credential candidate gate passes or blockers are accepted for that tester
  lane;
- keyring failure policy is linked;
- tester setup and cleanup guide is linked;
- artifact and secret scans pass;
- final production-hardening decision explicitly approves limited private
  tester distribution.

If any gate fails, do not distribute the credential package candidate. Keep the
base package available for deterministic fake smoke.

## Round 7 Self-Checks

Debug self-check:

- The policy covers source, base, credentials, evidence, artifact, signing,
  real-provider, and release-decision gates.
- Success, expected rejection, blocker, skipped network, cleanup, and no-secret
  states are represented.

Architecture self-check:

- Package lanes stay explicit and do not change provider, credential, settings,
  history, OCR, capture, or UI ownership.
- The base package remains deterministic and keyring-free.
- Signing, installer, updater, cloud, OAuth, and account systems remain outside
  P16 implementation scope.
