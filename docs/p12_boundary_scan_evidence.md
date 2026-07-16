# P12 Boundary Scan Evidence

Date: 2026-07-16
Phase: P12 Private Trial Pilot And Feedback Triage
Status: PASS for deterministic boundary scan

P12 preserves the accepted P11/P10 release boundaries. The private pilot adds
tester operations, feedback intake, triage, and decision documents; it does not
add production cloud accounts, provider rewrites, network-required validation,
raw secret storage, or package artifacts.

## Artifact Boundary

Command:

```cmd
git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs
```

Result: PASS. No tracked files were reported.

Generated packages, screenshots, smoke app data, pytest temp data, local env
files, logs, keyring exports, OCR caches, tester personal data, and provider
secrets remain outside git.

## Secret Pattern Scan

Commands:

```cmd
rg -n "sk-[A-Za-z0-9_-]{20,}|Authorization: Bearer [A-Za-z0-9._-]+" . -g "!docs/p12_boundary_scan_evidence.md" -g "!docs/p11_boundary_scan_evidence.md"
rg -n "sk-" . -g "!docs/p12_boundary_scan_evidence.md" -g "!docs/p11_boundary_scan_evidence.md"
rg -n "Authorization: Bearer" . -g "!docs/p12_boundary_scan_evidence.md" -g "!docs/p11_boundary_scan_evidence.md"
rg -n "api_key=" . -g "!docs/p12_boundary_scan_evidence.md" -g "!docs/p11_boundary_scan_evidence.md"
rg -n 'API_KEY="' . -g '!docs/p12_boundary_scan_evidence.md' -g '!docs/p11_boundary_scan_evidence.md'
rg -n "API_KEY='" . -g "!docs/p12_boundary_scan_evidence.md" -g "!docs/p11_boundary_scan_evidence.md"
```

Results:

- OpenAI-like `sk-...` or bearer-token value shapes: PASS with no matches.
- `sk-`: PASS with only historical documentation text in
  `docs/p9_hardening_notes.md` saying no OpenAI-like placeholders should be
  committed.
- `Authorization: Bearer`: PASS with only historical documentation text in
  `docs/p9_hardening_notes.md` saying no bearer values should be committed.
- `api_key=`: PASS with no matches.
- `API_KEY="`: PASS with no matches.
- `API_KEY='`: PASS with placeholder-only `your_trial_key` examples in
  `RequireRealProvider.cmd`.

No real provider key value, bearer token, `.env`, local config/history file, log,
package resource, screenshot, tester personal data, or keyring export was found
in tracked content.

## Deterministic Credential And Trial Readiness Tests

Command:

```cmd
python -m pytest tests\test_credentials.py tests\test_trial_readiness.py tests\test_release_smoke.py --basetemp tmp\pytest-p12-boundary
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

The readiness check does not perform a real provider network call and does not
print a secret value.

## Boundary Decision

P12 remains documentation and operations focused. Private-trial feedback must be
screened through `docs/p12_feedback_intake_template.md` and
`docs/p12_trial_triage_workflow.md`; reports containing secrets, personal data,
private documents, sensitive screenshots, logs with secrets, keyring exports, or
ignored local artifacts must be rejected or resubmitted after sanitization.
