# P5 Privacy And Local Storage

Date: 2026-06-22
Status: P5 local storage notes

SnapLex stores local settings and optional text translation history on the local
machine. It does not store provider API key values.

## Local Data Path

Default data directory:

- Windows with `%APPDATA%`: `%APPDATA%\SnapLex`
- Fallback: `<user home>\.snaplex`

Tests and local smoke can override the data directory:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexSmoke"
python -m snaplex
```

Automated tests use temporary directories and do not write to real user app data.

## Config File

The default config file is:

```text
config.json
```

Stored fields include:

- config schema version
- source and target language
- provider name and fallback order
- provider base URLs
- provider API-key environment variable names
- provider timeout and retry settings
- OpenAI and DeepL model options
- history enabled/disabled preference
- history max-entry limit
- UI preferences

Provider API key values are not stored. SnapLex persists env var names such as
`SNAPLEX_OPENAI_API_KEY`, then providers read the actual secret from the process
environment at request time.

## History File

The default history file is:

```text
history.json
```

History entries store text metadata only:

- stable entry id
- source text
- translated text
- provider name
- source and target language
- flow, such as `clipboard` or `screen`
- creation timestamp

History does not store screenshots, OCR image data, provider request payloads,
provider response payloads, or API key values.

## History Controls

History defaults to disabled. Enable it in the settings dialog by checking
`History` and setting `History Max`.

When history is enabled:

1. Successful clipboard and screen translations are recorded.
2. The `History` dialog can copy an entry result.
3. The `History` dialog can delete one entry.
4. The `History` dialog can clear all entries.
5. Retention keeps only the latest configured number of entries.

When history is disabled, future successful translations are not recorded. Clear
existing history separately if you want to remove already stored entries.

## Manual Cleanup

To fully remove local SnapLex data, close the app and delete the configured data
directory. Do not delete shared folders outside the SnapLex data directory.
