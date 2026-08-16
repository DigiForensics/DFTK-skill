# binary-diff

Cross-version symbol migration and binary diffing: propagate an existing
reverse-engineering result (symbols / function names) from a prior binary version
to a new, un-symbolicated one.

- Read-only-first, evidence-preserving; the LLM only compares paired
  disassembly + pseudocode and returns fixed-format YAML.
- Pairs with `ida-reverse` / `radare2` for export and applying renames.

## Files

- `SKILL.md` — the methodology.
- `references/prompt-template.md` — the structured comparison prompt + variable map.
- `CHANGELOG.md`
- `LICENSE` — Apache-2.0.
