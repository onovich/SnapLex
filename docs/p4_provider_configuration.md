# P4 Provider Configuration

Date: 2026-06-22
Status: P4 local runtime configuration notes

SnapLex keeps fake translation as the deterministic default. Real providers are
available only when local configuration selects them.

## Provider Selection

Set these environment variables before launching the GUI:

```powershell
$env:SNAPLEX_PROVIDER = "libretranslate"
$env:SNAPLEX_PROVIDER_ORDER = "libretranslate,fake"
python -m snaplex
```

Supported provider names:

- `fake`
- `libretranslate`
- `openai`
- `deepl`

`SNAPLEX_PROVIDER_ORDER` controls fallback order. Keep `fake` last when you want
a local offline fallback during development.

## Shared Variables

- `SNAPLEX_PROVIDER`: selected provider when no explicit order is supplied.
- `SNAPLEX_PROVIDER_ORDER`: comma-separated fallback order.
- `SNAPLEX_SOURCE_LANG`: default source language, usually `auto`.
- `SNAPLEX_TARGET_LANG`: default target language.

## LibreTranslate

LibreTranslate is useful for local or self-hosted development:

```powershell
$env:SNAPLEX_PROVIDER = "libretranslate"
$env:SNAPLEX_PROVIDER_ORDER = "libretranslate,fake"
$env:SNAPLEX_LIBRETRANSLATE_BASE_URL = "http://localhost:5000"
python -m snaplex
```

If your instance requires a key, set the env var name and the secret separately:

```powershell
$env:SNAPLEX_LIBRETRANSLATE_API_KEY_ENV = "SNAPLEX_LIBRETRANSLATE_API_KEY"
$env:SNAPLEX_LIBRETRANSLATE_API_KEY = "<local secret>"
```

## OpenAI

OpenAI uses the Responses API endpoint under `SNAPLEX_OPENAI_BASE_URL`.

```powershell
$env:SNAPLEX_PROVIDER = "openai"
$env:SNAPLEX_PROVIDER_ORDER = "openai,fake"
$env:SNAPLEX_OPENAI_API_KEY = "<local secret>"
$env:SNAPLEX_OPENAI_MODEL = "gpt-5.5"
python -m snaplex
```

The runtime config stores `SNAPLEX_OPENAI_API_KEY_ENV`, not the API key value.

## DeepL

DeepL defaults to the free API endpoint. Use `https://api.deepl.com/v2` for Pro:

```powershell
$env:SNAPLEX_PROVIDER = "deepl"
$env:SNAPLEX_PROVIDER_ORDER = "deepl,fake"
$env:SNAPLEX_DEEPL_API_KEY = "<local secret>"
python -m snaplex
```

The runtime config stores `SNAPLEX_DEEPL_API_KEY_ENV`, not the API key value.

## Timeout And Retry

Each real provider supports timeout and retry variables:

- `SNAPLEX_LIBRETRANSLATE_TIMEOUT_SECONDS`
- `SNAPLEX_LIBRETRANSLATE_RETRY_COUNT`
- `SNAPLEX_OPENAI_TIMEOUT_SECONDS`
- `SNAPLEX_OPENAI_RETRY_COUNT`
- `SNAPLEX_DEEPL_TIMEOUT_SECONDS`
- `SNAPLEX_DEEPL_RETRY_COUNT`

Retries happen inside the provider wrapper before `TranslationPipeline` falls
back to the next provider. Missing credentials and unsupported language errors
are not retried.

## Optional Real Provider Smoke

Automated tests must stay mocked and no-network. When local credentials or a
self-hosted LibreTranslate instance are available, use a short manual smoke:

1. Set `SNAPLEX_PROVIDER_ORDER` to the real provider followed by `fake`.
2. Launch `python -m snaplex`.
3. Copy a short phrase and select `Translate Clipboard`.
4. Confirm the result view shows the selected real provider.
5. Temporarily break the credential or base URL and confirm fallback/error state.

Do not commit `.env`, provider keys, request logs containing secrets, or local
provider output captures.
