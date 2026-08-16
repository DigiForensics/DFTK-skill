# Go / Rust recovery cheatsheet

Command and tool reference for `go-rust-reverse`. The point is to recover the
language metadata (function names, types, runtime layout) that makes decompilation
idiomatic — generic disassembly is `radare2` / `ida-reverse` / `ghidra-reverse`'s job.
Work on a copy; `dftk hash` the original first.

## Identify the language

```bash
file sample
strings -n 6 sample | grep -iE 'go1\.|rustc|panic|runtime\.|/rustc/'
# Go tell-tales: go.buildid, __gopclntab, residual runtime.* symbols
# Rust tell-tales: rust_begin_unwind, std::/core::, /rustc/<hash>/ paths
dftk hash sample
```

## Go: recover pclntab / moduledata

```text
□ GoReSym        — parses pclntab + moduledata, emits IDA/Ghidra symbols + types
□ redress        — older Go version name recovery
□ golang_loader_assist (IDA) / go-fortune (Ghidra) — symbol + string recovery
□ After recovery: rename sub_* sea, then follow crypto/* and net/http xrefs
```

- Stripped Go is **not** "no symbols" — `GoReSym` usually recovers most names
  automatically. Do this before manual renaming.
- Interface tables, slice headers, and string structs need care in decompilation;
  recover the type map first.

## Rust: locate by string, then symbol

```text
□ Panic strings + rust_begin_unwind anchor the unwind path
□ Generics bloat code — xref from the string first, then walk the monomorphized fn
□ Async / tokio state machines need cross-reference context (poll fns)
□ rust-demangle (binutils) for mangled symbols; cargo metadata for crate graph
```

## Quick triage tool chain

| Tool | Use |
|------|-----|
| GoReSym | Go metadata → symbols + types |
| redress / golang_loader_assist | Legacy Go name recovery |
| IDA / Ghidra + Go/Rust plugins | Decompilation |
| radare2 / rabin2 / strings | First-pass triage |
| rust-demangle | Demangle Rust symbol names |

## Cross-links
- DFTK MCP: `../../../references/mcp-setup.md`.
- Generic disassembly: `../../radare2/references/cheatsheet.md`, `../../ida-reverse/`, `../../ghidra-reverse/`.
- Suspicious sample: `../../malware-analysis/`.
