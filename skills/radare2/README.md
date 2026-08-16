# radare2

CLI-first binary analysis methodology built on `radare2` (`r2`) and its
companion utilities (`rabin2`, `rasm2`, `radiff2`, `rahash2`, `rax2`).

- Read-only-first, evidence-preserving; import-table inspection is a hard gate
  before deep analysis.
- Covers recon, interactive function analysis, locating main / key logic, hex &
  memory views, non-interactive automation, and light patching (owned artifacts
  only).
- Pairs with DFTK's audit ledger (`--audit`) for process provenance and with
  `ida-reverse` / `ghidra-reverse` for decompiler work.

## Files

- `SKILL.md` — the methodology.
- `references/cheatsheet.md` — command reference.
- `CHANGELOG.md`
- `LICENSE` — Apache-2.0.
