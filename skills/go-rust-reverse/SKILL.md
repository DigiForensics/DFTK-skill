---
name: go-rust-reverse
description: >-
  Reverse engineering of stripped Go and Rust binaries — runtime recognition,
  pclntab / module-data recovery, panic strings, and idiomatic decompilation
  recovery. Read-only-first, evidence-preserving. Use for authorized analysis of
  stripped Go/Rust tooling or malicious samples where language metadata is the key
  to recovering function names.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - golang
  - rust
  - forensics
  - malware
---

# Go / Rust binary reverse engineering

Methodology for analyzing **stripped** Go and Rust binaries. Both compilers encode
rich metadata that, once recovered, makes decompilation far more idiomatic — this
module is about recovering that language context rather than generic disassembly
(which `radare2` / `ida-reverse` / `ghidra-reverse` cover).

This is a **methodology skill**. The tools are external; nothing here is bundled in
the `dftk` wheel.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- `dftk hash` is the DFIR-preferred hashing for the binary file.
- Hand off generic disassembly to `ida-reverse` / `ghidra-reverse` / `radare2`;
  hand off a suspicious sample to `malware-analysis`.

## Operating contract (read-only, preserve, prove)

1. **Work on a copy.** SHA-256 the original before analysis.
2. **Record provenance.** Each finding cites the recovered symbol / runtime artifact
   and the tool that produced it.
3. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE /
   UNRESOLVED / UNSUPPORTED.
4. **Modify only owned artifacts.** Patching is permitted only for binaries you are
   authorized to modify; log every change in the audit ledger.

## Confirm the language

```bash
file sample                 # "Go" / "Rust" hints
strings sample | grep -iE "go1\.|rustc|panic|runtime\."
```

Go markers: `go.buildid`, residual `runtime` symbols, `pclntab` (`__gopclntab`);
Rust markers: `rust_begin_unwind`, `panic`, crate paths (`/rustc/...`),
`std::` / `core::` in strings.

## Go workflow

```text
□ Identify go.buildid, residual runtime symbols, pclntab
□ Recover function names with GoReSym / redress / IDA Go plugins
□ Watch for interface / slice / string structure in decompilation
□ Network/crypto paths: crypto/*, net/http
```

- `GoReSym` recovers function names and types from `pclntab` / `moduledata` even
  when stripped.
- Recovering names early turns an anonymous `sub_*` sea into readable call graphs.

## Rust workflow

```text
□ Panic strings, rust_begin_unwind, crate-path hints
□ Generics cause code bloat — locate by string xref first
□ Async / tokio state machines need cross-reference context
```

## Dynamic (optional, authorized)

```text
□ Frida still works; mind Go's stack / scheduler
□ Prefer logging / config-string-driven breakpoints
```

## Tool chain

| Tool | Use |
|------|-----|
| GoReSym | Go metadata recovery |
| IDA / Ghidra + Go/Rust plugins | Decompilation |
| radare2 | Quick strings / triage |
| strings / rabin2 | Initial triage |

## Domain references

- Recovery commands & tool chain → `references/cheatsheet.md`

## Quality bar

A defensible Go/Rust pass recovers key function names (or an equivalent mapping),
labels the language-runtime evidence, records provenance, and leaves reproducible
steps.

---

