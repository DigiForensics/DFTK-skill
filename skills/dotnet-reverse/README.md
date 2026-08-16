# dotnet-reverse

.NET / C# reverse-engineering methodology: managed-assembly identification,
deobfuscation with `de4dot`, dnSpyEx / ILSpy static analysis, and IL-level
inspection.

- Read-only-first, evidence-preserving; deobfuscate packed samples before deep
  analysis.
- IL view is authoritative for key decisions (C# view can distort async/state
  machines).
- Covers ConfuserEx / SmartAssembly / Babel / Eazfuscator / .NET Reactor and
  authorized .NET malware-loader analysis.

## Files

- `SKILL.md` — the methodology.
- `references/obfuscators.md` — per-protector deobfuscation behavior.
- `references/common-workflow.md` — full workflow, IL-patch reliability, string
  decryptor extraction.
- `CHANGELOG.md`
- `LICENSE` — Apache-2.0.
