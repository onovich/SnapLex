# P7 Browser Extension Bridge Design

Date: 2026-06-22
Phase: P7 Expansion Track
Status: design plan

This document designs a future browser extension bridge for SnapLex. P7 does
not implement a production browser extension.

## Goals

- Let a browser selection or page text become a SnapLex desktop translation
  intent.
- Keep browser-origin data separate from desktop provider credentials, settings,
  and local history.
- Preserve the Windows MVP desktop package and deterministic release smoke.
- Define contracts that can be implemented and tested without real network
  providers.
- Make permissions and trust boundaries explicit before any extension runtime
  is built.

## Non-Goals

- No production WebExtension implementation in P7.
- No browser-store packaging.
- No native messaging host installer.
- No cloud sync or remote account system.
- No browser-side provider credentials.
- No direct browser calls to OpenAI, DeepL, LibreTranslate, OCR, or SnapLex
  history storage.

## Candidate User Flows

### Translate Browser Selection

1. User selects text on a web page.
2. Browser extension asks for explicit user action, such as context-menu
   `Translate with SnapLex`.
3. Extension sends selected text and minimal origin metadata to the local
   desktop bridge.
4. SnapLex desktop translates through `TranslationPipeline`.
5. SnapLex shows the existing result view.

### Summarize Browser Selection

This is a future flow that depends on the AI summary capability design.

1. User selects text on a web page.
2. Browser extension sends selected text as a summary intent.
3. SnapLex routes the request to a future `SummaryService`.
4. Summary result is shown in a desktop-owned UI.

### Page OCR Is Rejected

Browser screenshot OCR is rejected for the first bridge pass. It introduces
cross-browser screenshot permissions, image privacy concerns, and overlap with
the accepted desktop screen-capture flow.

## Trust Boundary

The browser extension is an untrusted client. It may provide:

- selected text,
- user-selected intent,
- tab title,
- origin URL or origin host,
- browser locale,
- timestamp,
- request id.

The browser extension must not provide:

- provider credentials,
- local config path,
- local history path,
- package resource path,
- arbitrary filesystem paths,
- executable commands,
- direct provider selection overrides unless explicitly allowed by settings.

SnapLex desktop owns provider selection, fallback order, settings, history, and
all provider credentials.

## Desktop Handoff Options

### Option A: Native Messaging

Browser extension communicates with a registered native messaging host.

Pros:

- Browser-supported security model.
- No localhost port exposure.
- Clear per-extension allowlist.

Cons:

- Requires installer/registration work.
- Harder to smoke inside the current P6 package.
- Browser-specific manifests and policies can vary.

### Option B: Localhost HTTP Bridge

SnapLex desktop starts a loopback-only HTTP endpoint when enabled.

Pros:

- Easier local testing.
- Simple request/response contracts.
- Can be reused by other local tools.

Cons:

- Requires CSRF/origin protections.
- Needs port discovery.
- Must be disabled by default.

### Option C: Clipboard Handoff

Browser extension copies text to clipboard and asks the user to trigger SnapLex.

Pros:

- Minimal desktop changes.
- Reuses existing clipboard flow.

Cons:

- Less smooth.
- Clipboard privacy expectations are weaker.
- Harder to carry origin metadata.

Recommended first implementation: native messaging design if packaging/installer
work is approved; otherwise clipboard handoff as a zero-bridge fallback. Do not
enable a localhost bridge until origin and token protections are designed.

## Intent Contract

Future JSON shape:

```json
{
  "version": 1,
  "request_id": "uuid-or-browser-generated-id",
  "intent": "translate_selection",
  "source": {
    "kind": "browser_selection",
    "text": "selected text",
    "origin_url": "https://example.com/path",
    "origin_title": "Example",
    "browser_locale": "en-US"
  },
  "preferences": {
    "source_lang": "auto",
    "target_lang": "en"
  }
}
```

Rules:

- `text` is required and length-limited.
- `origin_url` is optional and may be reduced to origin host for privacy.
- `preferences` are hints only. Desktop config remains authoritative.
- Unknown fields are ignored.
- Unsupported versions are rejected with a structured error.

## Response Contract

Future JSON shape:

```json
{
  "version": 1,
  "request_id": "same-id",
  "status": "accepted",
  "desktop_action": "result_window_opened"
}
```

Error shape:

```json
{
  "version": 1,
  "request_id": "same-id",
  "status": "rejected",
  "error_code": "text_too_long",
  "message": "The selected browser text is too long for this action."
}
```

Error codes:

- `unsupported_version`
- `unsupported_intent`
- `empty_text`
- `text_too_long`
- `bridge_disabled`
- `desktop_busy`
- `permission_denied`
- `invalid_origin`
- `internal_error`

## Permission Model

Extension permissions should start narrow:

- `contextMenus`
- `activeTab` or selection-only content script access
- native messaging permission only if native messaging is chosen

Avoid broad host permissions in the first implementation. If page content
scripts are needed, prefer user-initiated injection into the active tab.

## Privacy Rules

- Browser-origin text is user data.
- Do not persist browser-origin text by default.
- Do not send browser-origin text to a network provider unless the desktop
  provider settings already allow that provider.
- Do not expose provider API key env var values to the browser.
- Do not store origin URLs in history by default.
- If origin metadata is stored later, offer a clear user setting.
- Logs must not include selected text or provider response bodies.

## Security Rules

- Desktop bridge must be disabled by default.
- Desktop bridge must require explicit user opt-in.
- Native messaging host should allow only known extension ids.
- Localhost bridge, if chosen, must bind only to loopback and use a per-session
  token.
- Reject requests above a configured size limit.
- Validate JSON schema before dispatch.
- Never execute browser-provided commands.
- Never open browser-provided filesystem paths.
- Normalize line endings and control characters before provider calls.

## Desktop Service Boundary

Future desktop module:

```text
snaplex/bridge/
  contracts.py          # browser intent dataclasses and validation
  service.py            # BrowserBridgeService
  native_messaging.py   # optional transport adapter
  localhost.py          # optional loopback transport adapter
```

`BrowserBridgeService` should convert browser intents into existing app-service
calls:

- translation intents call `TranslationPipeline`,
- future summary intents call `SummaryService`,
- history recording remains controlled by `HistoryService` and user settings,
- provider credentials remain desktop-only.

Transport adapters should not own translation, summary, settings, history, or
provider rules.

## No-Network Test Strategy

Initial tests should cover:

- Intent schema validation.
- Empty text rejection.
- Text length rejection.
- Unsupported version rejection.
- Unsupported intent rejection.
- Origin metadata normalization.
- Desktop-disabled rejection.
- Fake-provider translation dispatch.
- No provider credentials in request/response.
- No history persistence by default.

These tests should run without a browser runtime and without network access.

## Packaging Impact

P7 adds no packaging impact. Future implementation must prove:

- `python -m snaplex --no-gui` still works when bridge dependencies are absent.
- Packaged `SnapLex.exe --smoke-package` remains unchanged.
- Native messaging registration, if added, is not part of the base package
  smoke unless planner approves packaging work.
- Browser extension build artifacts are not committed unless explicitly scoped.

## Rejection Criteria

Reject a browser bridge implementation proposal if it requires:

- storing provider secrets in browser storage,
- direct browser-to-provider network calls,
- broad host permissions without user initiation,
- committing browser build outputs,
- changing the accepted translation provider contract,
- making a bridge server mandatory for app startup,
- weakening P6 package smoke or no-GUI bootstrap.

## Open Decisions

- Native messaging vs localhost bridge vs clipboard handoff for first
  implementation.
- Whether origin metadata should be stored at all.
- Maximum selected-text size for bridge intents.
- How the desktop app should surface browser-origin privacy warnings.
- Whether the extension should receive translated text back or only trigger the
  desktop result window.
