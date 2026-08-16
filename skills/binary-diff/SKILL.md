---
name: binary-diff
description: >-
  Cross-version symbol migration and binary diffing — use when you already have a
  prior version's reverse-engineering results (symbols / function names) and need
  to quickly propagate them to a new, un-symbolicated version. Read-only-first,
  evidence-preserving. Core method: structured LLM comparison of paired
  disassembly + pseudocode, with programmatic YAML output. Pairs with ida-reverse /
  radare2 for export and application.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - reverse-engineering
  - binary-diff
  - symbol-migration
  - forensics
---

# Cross-version symbol migration (binary diff)

Methodology for migrating an existing reverse-engineering result from one binary
version to a newer, un-symbolicated version. Typical cases:

1. **Kernel/driver missing PDB** — you have symbols for an old `ntoskrnl.exe`; the
   new PDB was pulled; derive the new non-exported function addresses from the old.
2. **Program updated** — you reverse-engineered v1.0 (200+ named functions); v1.1
   lost all symbols; migrate the names in bulk.
3. **Protection changed** — you need the new offset of a known function fast.
4. **Any "old symbols + new un-symbolicated binary" comparison.**

This is a **methodology skill**. The LLM comparison is external; nothing here is
bundled in the `dftk` wheel. For a from-scratch analysis, use `ida-reverse` /
`radare2`; for two fully unrelated binaries, use BinDiff / Diaphora.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working so
  the migration process (inputs, anchors, applied renames) is recorded with hashes.
- Use `ida-reverse` / `radare2` for the export (disassembly + pseudocode) and for
  applying the resulting renames.

## Operating contract (read-only, preserve, prove)

1. **Authorized scope.** Migrate symbols for binaries you own or are authorized to
   analyze; do not apply to third-party binaries you are not cleared to modify.
2. **Anchor reliability is everything.** A wrong anchor poisons every downstream
   mapping — verify anchors before bulk application.
3. **Human spot-check.** The LLM is not 100% accurate; verify key symbols.
4. **Cache intermediate results** to avoid repeated calls.
5. **Record provenance.** Log each applied rename (address + source symbol) in the
   audit ledger.

## Why this method

| Approach | ~200 functions | Time | Accuracy |
|----------|----------------|------|----------|
| Two IDA windows by hand | free but exhausting | hours | high |
| BinDiff auto-match | free | fast | medium (fails on big structural change) |
| Full agent (CC/Codex) | ¥50–100 | slow | high |
| **This (LLM batch compare)** | **~¥1** | **~10s/func** | **high** |

The LLM only does one thing: look at two code listings and find the correspondence.
Inputs/outputs are fixed-format and parsed programmatically.

## Workflow

```text
Step 1: Prepare data
  - Load the OLD binary (has PDB/symbols) in IDA
  - Load the NEW binary (no symbols) in IDA
  - Find shared anchor functions (exports, string refs) in BOTH

Step 2: Batch export
  - From OLD: disassembly + pseudocode of anchor function (with symbols)
  - From NEW: disassembly + pseudocode of the SAME anchor (no symbols)

Step 3: LLM compare
  - Fill the prompt template (see references/prompt-template.md)
  - Call an LLM API; parse the returned YAML

Step 4: Apply
  - Map YAML symbols onto the NEW IDB via rename / comments

Step 5: Iterate
  - Migrated functions become new anchors; descend into their calls; repeat
```

## Anchor selection

| Anchor type | Reliability | Note |
|-------------|-------------|------|
| Exported function | highest | name stable, address may move |
| String reference | high | string stable, reference site may move |
| Constant / magic number | medium | feature stable |
| Code pattern | medium | structure similar, addresses all move |

## YAML symbol types (output contract)

| Type | Meaning | Key fields |
|------|---------|-----------|
| `found_vcall` | virtual call (indirect) | `vfunc_offset`, `func_name` |
| `found_call` | direct call | `insn_va`, `func_name` |
| `found_funcptr` | function-pointer ref | `insn_va`, `funcptr_name` |
| `found_gv` | global-var ref | `insn_va`, `gv_name` |
| `found_struct_offset` | struct-offset ref | `offset`, `struct_name`, `member_name` |

## Application mapping

```text
found_call          -> rename(addr=call_target, name=func_name)
found_vcall         -> comment(addr=insn_va, "vcall: {func_name} @ +{offset}")
found_funcptr       -> rename(addr=funcptr_target, name=funcptr_name)
found_gv            -> rename(addr=gv_addr, name=gv_name)
found_struct_offset -> comment(addr=insn_va, "{struct_name}.{member_name}")
```

## Notes

- Compare **one function at a time**; never dump the whole binary into the LLM.
- Medium functions (<200 lines): cheap general model. Very large (>500 lines): a
  stronger model, or split.
- Concurrency (10–20 parallel) speeds bulk migration; cache results.
- Watch context limits: huge functions (>1000 lines disasm) need splitting or a
  large-context model.

## Quality bar

A defensible migration uses reliable anchors, spot-checks key symbols, caches
intermediate results, and records every applied rename in the audit ledger.

---

