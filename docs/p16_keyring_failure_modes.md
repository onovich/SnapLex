# P16 Keyring Failure Modes And Support Policy

Date: 2026-07-17
Phase: P16 Credential-Capable Package Production Hardening
Status: failure modes documented and deterministic failure wrapping tested

P16 keeps credential-capable package support explicit and conservative. Keyring
failures must be understandable, must not print raw credential values, and must
not change the deterministic base package behavior.

## Support Boundary

Supported for P16 private-trial hardening:

- Windows Credential Locker through `keyring.backends.Windows.WinVaultKeyring`;
- explicit `credentials` package variant only;
- credential smoke with runtime-generated throwaway values only;
- local secure credentials stored through `CredentialService` and
  `KeyringCredentialStore`.

Not supported or not promised in P16:

- silent keyring support in the base package;
- exported keyring data;
- real-provider network tests in automated validation;
- enterprise policy bypasses;
- account OAuth, SnapLex Cloud, hosted token broker, billing, or cloud sync;
- signed installer/updater behavior.

## Failure Mode Matrix

| Failure mode | Expected user/maintainer signal | P16 action |
| --- | --- | --- |
| Base package credential smoke | `keyring is not available in this runtime.` | PASS expected rejection; use the explicit `credentials` variant for credential package smoke. |
| Missing optional keyring dependency in source | `Install the optional credentials extra to use local secure storage.` or package smoke unavailable message | Install `.[credentials]` for source smoke, or build the `credentials` package variant. |
| Backend discovery failure | `keyring backend discovery failed.` | Treat as blocker for credential-capable package distribution on that machine. Do not collect backend exception details if they might contain local data. |
| Locked Windows Credential Locker | `credential save/read/cleanup failed: credential source unavailable.` | Ask tester to unlock Windows session, retry once, then record as environment blocker. |
| Enterprise policy disables local credential writes | `credential save failed: credential source unavailable.` | Do not bypass policy. Record blocker and use env-var provider setup if approved. |
| Unsupported platform/backend | `Credential source unsupported` or keyring backend not WinVault | Keep package out of that tester lane until a platform-specific policy is defined. |
| `check-delete` run before `save` | `credential was not ready after restart: Credential missing` | Expected operator-order failure; run `save` first, then `check-delete`. |
| Cleanup fails after save | `credential cleanup failed: credential source unavailable.` | Retry cleanup after unlocking the session. If still unavailable, record blocker and do not distribute that package lane. |
| Credential resolves to empty value | `credential resolved to an empty value after restart.` | Treat as smoke failure; do not proceed with credential-capable package distribution. |
| Real provider not configured | `Real translation provider is not configured.` | Expected fail-closed behavior without local credentials and explicit network approval. |

## Deterministic Test Evidence

Round 4 and Round 6 tests cover no-secret failure behavior:

```cmd
python -m pytest tests\test_release_smoke.py --basetemp tmp\pytest-p16-keyring-failure-modes
```

Expected result: PASS.

The tests cover:

- phase-neutral credential smoke reference;
- phase-neutral keyring service name;
- save/read/delete cleanup without raw value output;
- backend discovery failure wrapping;
- store failure wrapping;
- omission of backend exception text such as local system details.

## Operator Guidance

When a private tester reports a keyring failure:

1. Ask for the exact status line only.
2. Do not ask for a screenshot of credential fields.
3. Do not ask for keyring exports.
4. Confirm whether they used `base` or `credentials`.
5. Confirm whether Windows was locked, remote, or policy-managed.
6. Ask them to run import smoke before cycle smoke.
7. Ask them to run `check-delete` only after `save`, unless they are cleaning
   a known retained smoke credential.
8. If a failure repeats, record it as an environment blocker instead of asking
   the tester to weaken local security policy.

## Distribution Decision Impact

Credential-capable package distribution is blocked for a tester lane when:

- import smoke cannot discover a backend;
- cycle smoke cannot save/read/delete;
- restart readiness cannot clean up;
- the backend is not Windows WinVault in the current Windows private-trial
  lane;
- cleanup status cannot be verified without exposing secrets.

The base package lane remains available because it does not include keyring and
uses deterministic fake smoke.

## No-Secret Policy

Failure reports may include:

- package variant;
- smoke mode;
- status line;
- backend class label;
- whether cleanup ended as `missing`.

Failure reports must not include:

- provider API key values;
- throwaway smoke values;
- keyring exports;
- `.env` contents;
- screenshots of credential dialogs;
- provider account dashboards;
- private source text or translation text.

## Round 6 Self-Checks

Debug self-check:

- The current policy covers success, expected rejection, missing dependency,
  backend discovery failure, unavailable/locked store, unsupported backend,
  operator-order failure, cleanup failure, empty resolve, and real-provider
  fail-closed behavior.
- Deterministic tests cover backend discovery and store failure wrapping
  without leaking backend details.

Architecture self-check:

- Failure handling remains in credential service/store and release smoke
  boundaries.
- Packaging remains an explicit variant gate.
- No UI, provider, OCR, capture, cloud, OAuth, token broker, or network-test
  scope is added.
