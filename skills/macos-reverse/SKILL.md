---
name: macos-reverse
description: >-
  Authorized macOS and Mach-O reverse engineering — codesign / notarization
  inspection, Objective-C / Swift symbol and runtime recovery, endpoint-security
  surface review, and Apple-platform malware analysis. Read-only-first,
  evidence-preserving. iOS/IPA analysis routes to mobile-reverse.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - macos
  - mach-o
  - forensics
  - malware
---

# macOS / Mach-O reverse engineering

Methodology for analyzing macOS binaries: Mach-O executables / dylibs / frameworks,
`.app` bundles, LaunchAgents / LaunchDaemons, Objective-C / Swift symbols and
runtime, and notarization / Hardened Runtime / TCC behaviors. Also covers
authorized analysis of macOS malware (hand off to `malware-analysis`).

This is a **methodology skill**. The tools are external; nothing here is bundled in
the `dftk` wheel. For iOS/IPA, use `mobile-reverse`.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- `dftk hash` is the DFIR-preferred hashing for the binary/file.
- Hand off a suspicious sample to `malware-analysis`; hand off deep decompilation to
  `ghidra-reverse` / `ida-reverse`.

## Operating contract (read-only, preserve, prove)

1. **Work on a copy.** SHA-256 the original before analysis.
2. **Record provenance.** Each finding cites the tool, the locator (path/address),
   and the value.
3. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE /
   UNRESOLVED / UNSUPPORTED.
4. **Authorized scope only.** Analyze software you own or are authorized to assess;
   do not bypass TCC / Hardened Runtime controls on systems you are not authorized
   to test.
5. **Modify only owned artifacts.** Patching is permitted only for binaries you are
   authorized to modify; log every change in the audit ledger.

## Workflow

### 1. Bundle & signature

```bash
file target
codesign -dv --verbose=4 target
spctl -a -vv target 2>&1
otool -L target
```

Record: code-signing identity, notarization status, Hardened Runtime flags, and
linked dylibs / rpath.

### 2. Static

```text
□ class-dump / swift-demangle / Hopper / Ghidra / IDA
□ Strings + XPC service names + TCC-sensitive API usage
□ LC_LOAD_DYLIB dependencies and rpath
```

### 3. Dynamic (authorized, isolated)

```text
□ lldb / Frida
□ fs_usage / log stream to observe file/network behavior
□ Network: pair with protocol-reverse or a proxy
```

## Tool chain

| Tool | Use |
|------|-----|
| otool / nm / codesign | System-provided |
| Hopper / Ghidra / IDA | Decompilation |
| class-dump / dsdump | Objective-C |
| Frida / lldb | Dynamic |
| jtool2 | Mach-O internals |

## Domain references

- Codesign / TCC / Hardened Runtime commands → `references/cheatsheet.md`

## Quality bar

A defensible macOS pass records signing / Hardened Runtime status, produces
address-level or symbol-level conclusions, and preserves provenance for every
finding.

---

