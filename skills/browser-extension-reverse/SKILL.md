---
name: browser-extension-reverse
description: >-
  Authorized reverse engineering of browser extensions (Chrome/Edge MV2/MV3,
  Firefox) — manifest analysis, background-worker / service-worker recovery, content
  script injection, and extension-based credential / traffic logic recovery.
  Read-only-first, evidence-preserving. Use for authorized analysis, malicious-extension
  IOC extraction, and supply-chain extension-poisoning investigation.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - browser-extension
  - forensics
  - supply-chain
  - malware
---

# Browser extension reverse engineering

Methodology for analyzing a browser extension package (`crx` / `xpi` / unpacked
directory). Covers manifest capability review, background / service-worker recovery,
content-script injection points, and the credential / network logic an extension
implements. Also applies to authorized analysis of malicious extensions and
supply-chain extension-poisoning investigations.

This is a **methodology skill**. The tools are external; nothing here is bundled in
the `dftk` wheel. For plain web-page JS (not an extension), use `js-reverse`.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- `dftk hash` is the DFIR-preferred hashing for the extension package. YARA rules for
  malicious extensions pair with `malware-analysis`.
- Hand off heavy JS obfuscation to `js-reverse`; hand off poisoning investigation to
  `supply-chain-security` / `malware-analysis`.

## Operating contract (read-only, preserve, prove)

1. **Work on a copy.** SHA-256 the package; analyze a copy.
2. **Authorized scope only.** Analyze extensions you own or are authorized to assess;
   for a malicious extension found in the wild, treat it as a forensic sample.
3. **Record provenance.** Each finding cites file, line, and the observed behavior.
4. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE /
   UNRESOLVED / UNSUPPORTED.
5. **Modify only owned artifacts.** Patching is permitted only for extensions you are
   authorized to modify; log every change in the audit ledger.

## Workflow

### 1. Package & manifest

```text
□ Unpack the crx / xpi, or load the unpacked directory from the profile
□ Read manifest.json: permissions, host_permissions, background, content_scripts
□ Flag over-broad permissions: <all_urls>, webRequest, debugger
```

### 2. Logic

```text
□ service_worker / background entry point
□ content_script injection points and isolated world
□ chrome.storage / IndexedDB keys
□ Same as js-reverse: observe network and message passing (runtime.sendMessage)
```

### 3. Dynamic (authorized, isolated)

```text
□ Load unpacked in developer mode
□ Inspect chrome://extensions for errors
□ Attach DevTools to the service worker
□ If needed, Frida / browser CDP (js-reverse tooling)
```

## Tool chain

| Tool | Use |
|------|-----|
| unpack / jq | manifest inspection |
| Chrome DevTools | service-worker debugging |
| js-reverse tooling | deep JS analysis |
| YARA | malicious-extension rules |

## Domain references

- Triage commands & permission risk matrix → `references/cheatsheet.md`

## Quality bar

A complete extension pass lists the permission surface and entry scripts, recovers
the key data flows, preserves provenance, and separates fact from inference.

---

