# P16 Boundary Scan Evidence

Date: 2026-07-17
Phase: P16 Credential-Capable Package Production Hardening
Status: boundary, artifact, secret, and no-network scans PASS

P16 Round 9 confirms that credential-capable package hardening preserved the
accepted architecture boundaries and repository hygiene.

## Artifact Boundary Scan

Command:

```cmd
git ls-files -- build dist snaplex-smoke-data tmp .pytest_cache .env logs .mypy_cache .ruff_cache screenshots .paddleocr ocr_models
```

Result: PASS, no tracked generated artifacts.

Local `build\`, `dist\`, `snaplex-smoke-data\`, `tmp\`, and `.pytest_cache\`
may exist from smoke runs, but they remain ignored local artifacts.

## Secret Pattern Scan

Commands:

```cmd
rg -n "sk-[A-Za-z0-9_-]{20,}|Authorization: Bearer [A-Za-z0-9._-]+" .
rg -n "api_key=" .
rg -n 'API_KEY="' .
rg -n "API_KEY='" .
rg -n -- '-----BEGIN (RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----|xox[baprs]-|ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}' .
```

Result: PASS.

Findings:

- no OpenAI-like `sk-...` key or bearer token matches;
- no `api_key=` matches;
- no double-quoted `API_KEY="` matches;
- only documented `your_trial_key` placeholders in `RequireRealProvider.cmd`
  match `API_KEY='`;
- no private-key, Slack token, GitHub classic token, or GitHub fine-grained
  token matches.

## Runtime Smoke Reference Scan

Command:

```cmd
rg -n "snaplex/p15/package-spike|SnapLexP15PackageSmoke" snaplex tests scripts packaging
```

Result: PASS, no matches.

Historical P15 docs still record the old spike reference. P16 runtime code and
tests now use the phase-neutral `snaplex/package-credential-smoke` reference
and `SnapLexPackageCredentialSmoke` service.

## UI And Provider Boundary Scan

Command:

```cmd
rg -n "requests|httpx|urllib|OpenAIProvider|DeepLProvider|LibreTranslateProvider|set_password|get_password|delete_password|keyring" snaplex\ui
```

Result: PASS with expected UI-only keyring text/control matches.

Observed matches are limited to Settings labels, source selection, and control
enablement in `snaplex\ui\app_shell.py`. UI code does not call provider
classes, HTTP clients, or direct keyring `set_password`, `get_password`, or
`delete_password` APIs.

Command:

```cmd
rg -n "requests|httpx|urllib" snaplex\ui snaplex\services snaplex\storage
```

Result: PASS, no matches.

Provider HTTP behavior remains isolated to provider/transport boundaries.

## Fail-Closed And No-Network Evidence

Command:

```cmd
python -m snaplex --check-real-provider
```

Result: expected rejection PASS.

```text
Real translation provider is not configured.
```

Command:

```cmd
cmd /c StartTrial.cmd --no-gui
```

Result: expected rejection PASS.

Real-provider network smoke was not run in P16 because no existing local
credentials and explicit human network approval were supplied.

## Focused Test Evidence

Command:

```cmd
python -m pytest tests\test_release_smoke.py tests\test_trial_readiness.py tests\test_credentials.py --basetemp tmp\pytest-p16-boundary
```

Result: PASS with 29 tests. Pytest emitted a non-blocking local cache warning;
no test failed.

The focused tests cover:

- credential service/store behavior;
- no-secret serialization boundaries;
- real-provider readiness fail-closed behavior;
- phase-neutral credential package smoke;
- backend and store failure wrapping without raw value leakage.

## Round 9 Self-Checks

Debug self-check:

- The scan covers generated artifacts, key/token patterns, old P15 smoke names,
  UI/provider boundaries, real-provider expected rejection, and focused
  credential/readiness/release-smoke tests.
- Expected placeholder matches are documented and are not secrets.

Architecture self-check:

- Providers remain behind provider registry, HTTP transport, and
  `TranslationPipeline`.
- Credentials remain behind `CredentialService`, stores, provider setup, and
  trial readiness.
- UI does not own provider, HTTP, or keyring business rules.
- No generated outputs, screenshots, local data, keyring exports, `.env`, logs,
  OCR caches, smoke data, tester personal data, or secrets are committed.
