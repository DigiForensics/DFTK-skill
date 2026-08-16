---
name: thick-client
description: >-
  Authorized security review of desktop thick clients — local storage, update
  channels, IPC, traffic, and client-side trust boundaries. Read-only-first,
  evidence-preserving. Use for reviewing an app you own or are authorized to assess
  (C/S clients, Electron/Qt/.NET WinForms/WPF), focusing on where client-side
  enforcement and secrets live rather than bypassing third-party controls.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - thick-client
  - forensics
  - app-security
---

# Thick client security review

Methodology for reviewing a desktop thick client (Windows/macOS/Linux GUI or a
service companion) from a defensive, authorized-assessment standpoint. The goal is
to **map the trust boundary** and locate where local storage, IPC, update channels,
and client-side enforcement live — so the findings can be reported, not exploited
against software you are not authorized to test.

This is a **methodology skill**. The tools are external; nothing here is bundled in
the `dftk` wheel.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- `dftk hash` is the DFIR-preferred hashing for the installer/artifact.
- Hand off: `.NET` → `dotnet-reverse`; native → `ida-reverse` / `ghidra-reverse`;
  Electron → `asar` + `js-reverse`; pure protocol → `protocol-reverse`; update /
  supply-chain → `supply-chain-security`.

## Operating contract (read-only, preserve, prove)

1. **Authorized scope only.** Review apps you own or are authorized to assess. Do not
   bypass third-party license / integrity checks you are not authorized to test.
2. **Work on a copy.** SHA-256 the installer/artifact; analyze a copy.
3. **Record provenance.** Each finding cites the artifact, locator, and the value.
4. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE /
   UNRESOLVED / UNSUPPORTED.
5. **Modify only owned artifacts.** Any patching is permitted only for apps you are
   authorized to modify; log every change in the audit ledger.

## Workflow

### 1. Draw the trust boundary

```text
□ Process tree, child processes, drivers/services
□ Listening ports and outbound domains
□ Sensitive local paths: %APPDATA%, Keychain, registry
```

### 2. Local attack surface

```text
□ Plaintext config, hardcoded keys, debug switches
□ DLL search-order / hijack (Windows)
□ Database files (SQLite) permissions and encryption
□ IPC: who can connect? is it authenticated?
```

### 3. Network surface

```text
□ System proxy / app-specific TLS
□ Certificate pinning -> pair with mobile/js methods or Frida
□ API privilege: hidden admin interfaces the client can reach
```

### 4. Reverse-verify

```text
□ .NET -> dotnet-reverse; native -> ida/ghidra; Electron -> asar + js-reverse
```

## Tool chain

| Tool | Use |
|------|-----|
| Process Monitor / API Monitor | Behavior |
| Burp / mitmproxy | Traffic |
| dnSpy / IDA / Ghidra | Reverse |
| Sysinternals | Windows surface |
| asar / nexe detection | Electron |

## Domain references

- Trust-boundary & tool-chain commands → `references/cheatsheet.md`

## Quality bar

A defensible thick-client review draws the trust boundary, covers both local and
network surfaces, preserves provenance, and separates fact from inference — ending
in findings an engineer can act on, not a bypass recipe for someone else's software.

---

