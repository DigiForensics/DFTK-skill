# Ghidra command cheatsheet

## Headless analysis

```bash
# analyzeHeadless lives in Ghidra's support/ directory; resolve the path first
analyzeHeadless /path/to/project Proj -import sample.bin
analyzeHeadless /path/to/project Proj -import sample.bin -postScript ExportDecomp.py
```

## GUI workflow (manual)

1. **New Project** → **Non-Shared Project** (or Shared for team).
2. **File → Import File** the sample.
3. **Double-click** to open; click **Analyze** (accept default analyzers, add
   others like DWARF/Python as needed).
4. In **CodeBrowser**:
   - **Symbol Tree** — functions, classes, imports, exports.
   - **Decompile** window — right-click a function → Decompile.
   - **Window → Defined Strings** — find strings, double-click to jump.
   - **Xref** — right-click an address → References to see callers.
   - Rename (`L`), retype (`T`), and add Plate comments for annotations.

## Scripting

- **Jython / Python (PyGhidra)** scripts under `Window → Script Manager`.
- Useful built-ins: `ExportDecomp.py`, `ExportFunctionInformation.py`.
- For bulk export, write a post-script and run via `analyzeHeadless -postScript`.

## MCP bridge

- Capability name `ghidra-mcp` (when installed). Confirm the listening port from
  your environment before connecting; do not guess.
- Use the bridge to pull decompilations / xrefs programmatically.

## Notes

- Record the resolved `analyzeHeadless` path and Ghidra version in the audit
  ledger for reproducibility.
- For patch diffing, pair with `ghidriff` and hand off to `binary-diff`.
