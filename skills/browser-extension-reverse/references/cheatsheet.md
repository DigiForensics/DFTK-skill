# Browser extension triage cheatsheet

Quick commands and decision tables for the `browser-extension-reverse` workflow.
All work is read-only-first and evidence-preserving — SHA-256 the package before you
open it, and run the analysis on a copy. Pair with `js-reverse` for deep JS work and
`supply-chain-security` / `malware-analysis` for poisoning / malicious-extension cases.

## Unpack & hash

```bash
# CRX (Chrome) — header is "Cr24" + version(4) + pubkey_len(4) + sig_len(4), then ZIP
file extension.crx
dftk hash extension.crx                 # DFIR-preferred fixity

# XPI (Firefox) is a plain ZIP
unzip -l extension.xpi

# MV3 service-worker vs MV2 background-page split
jq '.manifest_version, .background, .permissions, .host_permissions' manifest.json
```

## Permission risk matrix

| Permission | Why it matters | Flag when |
|------------|----------------|-----------|
| `<all_urls>` | Can read/inject into every site the user visits | Always review |
| `webRequest` / `webRequestBlocking` | Sees full request/response bodies | Paired with host perms |
| `debugger` | Attaches to any tab, bypasses CSP | Almost never needed legitimately |
| `scripting` + `content_scripts` | Arbitrary page injection | Check `matches` scope |
| `storage` / `management` / `proxy` | Persists state, controls other extensions, reroutes traffic | Ties to exfil path |
| `clipboardRead` / `downloads` | Credential / payload capture | Correlate with network findings |

## Logic recovery checklist

```text
□ service_worker / background.js entry — the persistent process
□ content_scripts matches + run_at (document_idle / start) + isolated world
□ chrome.storage.local / IndexedDB keys (where harvested data lands)
□ runtime.sendMessage / onMessage handlers (message-passing surface)
□ fetch/XHR endpoints — hand to protocol-reverse if the scheme is unknown
□ Obfuscated background bundle → beautify with js-reverse, then re-triage
```

## Dynamic (authorized, isolated)

```text
□ Load unpacked in chrome://extensions (Developer mode)
□ Inspect for load-time errors / unexpected permissions warnings
□ Attach DevTools to the service worker
□ Frida / CDP for runtime behavior (see js-reverse tooling)
```

## Cross-links
- DFTK MCP: `../../../references/mcp-setup.md` (run under server policy).
- Deep JS: `../../js-reverse/references/` (env-rebuild, ast-deobf).
- Malicious-extension IOCs: `../../malware-analysis/` + YARA.
