# firmware-forensics

Defensive firmware / IoT analysis following the OWASP FSTM stages: information
gathering, acquisition, static analysis, filesystem extraction (binwalk / unblob /
EMBA), and emulation (Firmadyne / QEMU).

- Read-only by default; flaw validation only in an isolated lab, then responsible
  disclosure — never weaponization.
- Complements `reverse-exe` / `ida-reverse` / `radare2` (extracted binaries) and
  `binary-diff` (cross-version migration).

## Files

- `SKILL.md` — the methodology.
- `references/extraction.md` — extraction details and failure fallbacks.
- `CHANGELOG.md`
- `LICENSE` — Apache-2.0.
