# P11 Boundary Scan Evidence

Date: 2026-07-16
Phase: P11 Trial Release Hardening
Status: PASS for deterministic boundary scan

P11 preserves the P10 no-secret and deterministic no-network boundaries. This
evidence covers tracked artifact hygiene, provider-secret pattern scans, and
focused credential/readiness tests.

## Artifact Boundary

Command:

```cmd
git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs
```

Result: PASS. No tracked files were reported.

Generated packages, screenshots, smoke app data, pytest temp data, local env
files, logs, keyring exports, OCR caches, and provider secrets remain outside
git.

## Secret Pattern Scan

Commands:

```cmd
rg -n 'sk-' . -g '!docs/p11_boundary_scan_evidence.md'
rg -n 'Authorization: Bearer' . -g '!docs/p11_boundary_scan_evidence.md'
rg -n 'api_key=' . -g '!docs/p11_boundary_scan_evidence.md'
rg -n 'API_KEY="' . -g '!docs/p11_boundary_scan_evidence.md'
rg -n "API_KEY='" . -g '!docs/p11_boundary_scan_evidence.md'
```

Results:

- `sk-`: PASS with only historical documentation text saying no OpenAI-like
  placeholders should be committed.
- `Authorization: Bearer`: PASS with only historical documentation text saying
  no bearer values should be committed.
- `api_key=`: PASS with no matches.
- `API_KEY="`: PASS with no matches.
- `API_KEY='`: PASS with placeholder-only `your_trial_key` examples in
  `RequireRealProvider.cmd`.

No real provider key value, bearer token, `.env`, local config/history file, log,
package resource, screenshot, or keyring export was found in tracked content.

## Deterministic Credential And Trial Readiness Tests

Command:

```cmd
python -m pytest tests\test_credentials.py tests\test_trial_readiness.py tests\test_release_smoke.py --basetemp tmp\pytest-p11-boundary
```

Result: PASS, 22 tests.

Command:

```cmd
python -m snaplex --check-real-provider
```

Result: expected rejection PASS when no real provider credential or accepted
endpoint is configured:

```text
Real translation provider is not configured.
```

The check performs readiness validation and does not make a real provider
network call.

## Notes

An initial combined `rg` expression failed because of PowerShell quote parsing.
The scan was rerun with simpler individual patterns and the results above.
