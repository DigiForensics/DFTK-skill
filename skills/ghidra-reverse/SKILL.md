---
name: ghidra-reverse
description: >-
  Free / open-source reverse engineering with Ghidra (headless or GUI) — project
  import, auto-analysis, decompilation, cross-references, and optional Ghidra MCP
  workflows when IDA is unavailable. Read-only-first, evidence-preserving. Use for
  open-source / batch / teaching RE, or as the decompiler entry when no IDA
  license exists.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - ghidra
  - decompilation
  - forensics
---

# Ghidra reverse engineering

Methodology for using **Ghidra** (open-source, NSA) to decompile and reason about
binaries. Ghidra is the right entry when IDA is unavailable, when work is
open-source / batch / teaching, or when headless automation (CI) is needed.

This is a **methodology skill**. Ghidra is an external tool; nothing here is
bundled in the `dftk` wheel.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- `dftk hash` is the DFIR-preferred hashing for the binary file.
- Hand off to `ida-reverse` for deeper commercial decompilation, `radare2` for
  quick CLI triage, and `binary-diff` (with ghidriff) for patch diffing.

## Operating contract (read-only, preserve, prove)

1. **Work on a copy.** SHA-256 the original before import.
2. **Record provenance.** Each finding cites function/address, the decompiled
   logic, and the repro path.
3. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE /
   UNRESOLVED / UNSUPPORTED.
4. **Modify only owned artifacts.** Patching in Ghidra is permitted only for
   binaries you are authorized to modify; log every patch in the audit ledger.

## When to use Ghidra vs peers

| Need | Prefer |
|------|--------|
| Existing IDA MCP deep dive | `ida-reverse` |
| Open-source / batch / teaching | **Ghidra** |
| CLI quick triage only | `radare2` |

## Workflow

### 1. Project & auto-analysis

```text
□ New Project -> Import file -> Analyze (default analyzers)
□ Record language / compiler recognition and base address
□ Mark entry, exports, and string xrefs
```

### 2. Key functions

```text
□ Reverse from strings / imported API
□ Decompile window to recover algorithm
□ Rename functions/variables; add Plate comments
□ For dynamic needs, hand off to Frida/GDB (see reverse-engineering dynamic notes)
```

### 3. Headless (batch)

```bash
# analyzeHeadless path varies by install; resolve it from your environment
analyzeHeadless /path/to/project Proj -import sample.bin -postScript ExportDecomp.py
```

### 4. MCP (if configured)

```text
□ Confirm the Ghidra MCP port (commonly 8765; resolve from your environment)
□ Pull decompilations / xrefs via the MCP tools; do not guess ports
```

## Tool chain

| Tool | Use |
|------|-----|
| Ghidra | Decompiler main tool |
| ghidra-mcp | AI bridge (capability name `ghidra-mcp`) |
| ghidriff | Patch diffing (see `binary-diff`) |

## Domain references

- command reference → `references/cheatsheet.md`
- related: `../ida-reverse/`, `../radare2/`, `../binary-diff/`

## Quality bar

A complete Ghidra pass uses real, resolved tool paths, annotates function
addresses and renames, leaves reproducible steps, and records provenance for every
finding.

---

