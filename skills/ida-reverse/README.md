# ida-reverse

IDA Pro decompilation workflow for authorized binary analysis: survey, import
inspection, pseudocode recovery, cross-references, data-flow tracing, and
structured annotation.

- Read-only-first, evidence-preserving; the import table is a hard gate before
  deep analysis.
- Covers the analysis workflow and prompt-engineering discipline for the
  `idalib-mcp` (`idapro_*`) tool surface.
- Hands off to `binary-diff` for cross-version symbol migration and `radare2` for
  quick triage. Commercial IDA Pro required.

## Files

- `SKILL.md` — the methodology.
- `references/tool-index.md` — `idapro_*` tool catalog.
- `CHANGELOG.md`
- `LICENSE` — Apache-2.0.
