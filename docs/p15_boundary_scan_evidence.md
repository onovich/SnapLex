# P15 Boundary Scan Evidence

Date: 2026-07-16
Phase: P15 Isolated Credential-Capable Package Spike Design Gate
Status: PASS for deterministic boundary scan

P15 adds an explicit `credentials` package variant, a dedicated credential
smoke CLI, and evidence documents. It preserves the deterministic base package
path, keeps automated validation no-network, and does not commit generated
packages, smoke data, keyring exports, `.env` files, logs, screenshots, OCR
caches, tester personal data, or provider secrets.

## Artifact Boundary

Command:

```cmd
git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs .mypy_cache .ruff_cache screenshots .paddleocr ocr_models
```

Result: PASS. No tracked files were reported.

Generated package outputs, smoke app data, pytest temp data, local env files,
logs, keyring exports, OCR caches, tester personal data, and provider secrets
remain outside git.

## Secret Pattern Scan

Commands:

```cmd
rg -n "sk-[A-Za-z0-9_-]{20,}|Authorization: Bearer [A-Za-z0-9._-]+" . -g "!docs/p11_boundary_scan_evidence.md" -g "!docs/p12_boundary_scan_evidence.md" -g "!docs/p13_boundary_scan_evidence.md" -g "!docs/p14_boundary_scan_evidence.md"
rg -n "api_key=" . -g "!docs/p11_boundary_scan_evidence.md" -g "!docs/p12_boundary_scan_evidence.md" -g "!docs/p13_boundary_scan_evidence.md" -g "!docs/p14_boundary_scan_evidence.md"
rg -n 'API_KEY="' . -g '!docs/p11_boundary_scan_evidence.md' -g '!docs/p12_boundary_scan_evidence.md' -g '!docs/p13_boundary_scan_evidence.md' -g '!docs/p14_boundary_scan_evidence.md'
rg -n "API_KEY='" . -g "!docs/p11_boundary_scan_evidence.md" -g "!docs/p12_boundary_scan_evidence.md" -g "!docs/p13_boundary_scan_evidence.md" -g "!docs/p14_boundary_scan_evidence.md"
```

Results:

- OpenAI-like `sk-...` or bearer-token value shapes: PASS with no matches.
- `api_key=`: PASS with no matches.
- `API_KEY="`: PASS with no matches.
- `API_KEY='`: PASS with placeholder-only `your_trial_key` examples in
  `RequireRealProvider.cmd`.

No real provider key value, bearer token, `.env`, local config/history file,
log, package resource, screenshot, tester personal data, keyring export, or API
response capture was found in tracked content.

## Architecture Boundary Scan

Commands:

```cmd
rg -n "OpenAIProvider|DeepLProvider|LibreTranslateProvider" snaplex\ui
rg -n "requests|urllib|httpx" snaplex\ui
```

Results:

- Concrete provider classes in UI: PASS with no matches.
- Direct HTTP client usage in UI: PASS with no matches.

P15 did not move provider execution, credential persistence, trial readiness,
settings, history, OCR, capture, or packaging rules into UI widgets.

## Variant And Trial Boundary

Commands:

```cmd
python scripts\package_windows.py --dry-run --variant base
python scripts\package_windows.py --dry-run --variant credentials
dist\SnapLex\SnapLex.exe --smoke-credentials --credential-smoke-mode import
python -m snaplex --check-real-provider
```

Results:

- Base dry-run: PASS with `SNAPLEX_PACKAGE_VARIANT=base`.
- Credentials dry-run: PASS with `SNAPLEX_PACKAGE_VARIANT=credentials`.
- Current local base package credential smoke: expected rejection PASS,
  `keyring is not available in this runtime.`
- Real provider readiness: expected rejection PASS,
  `Real translation provider is not configured.`

The explicit `credentials` variant is available, but the base package remains
deterministic and does not silently include keyring.

## Deterministic Tests

Command:

```cmd
python -m pytest tests\test_package_windows.py tests\test_release_smoke.py tests\test_trial_readiness.py tests\test_credentials.py --basetemp tmp\pytest-p15-boundary
```

Result: PASS with 33 tests. Pytest emitted a non-blocking local cache warning
for `.pytest_cache`; no test failed.

## Boundary Decision

P15 remains an isolated package spike design gate. Credential-capable package
evidence is successful enough to recommend later production hardening, but P15
does not ship a production credential-capable package and does not change the
base package into a keyring-capable artifact.

## Round 9 Self-Checks

Debug self-check:

- The current change is explained by boundary scan and hygiene evidence.
- Artifact, secret, UI/provider, variant, fail-closed, deterministic test, and
  no-secret states are covered.
- Generated package outputs and smoke data remain ignored and uncommitted.

Architecture self-check:

- Providers remain behind provider contracts and `TranslationPipeline`.
- Credentials remain behind `CredentialService` and credential stores.
- Packaging remains an explicit variant path and does not own provider,
  credential, settings, history, OCR, capture, or UI business rules.
