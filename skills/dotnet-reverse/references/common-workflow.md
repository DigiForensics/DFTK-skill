# .NET common workflow (detail)

Expanded notes for the six-phase workflow in `../SKILL.md`.

## IL patch reliability

- **C# patch** recompiles the method. It fails when references are missing, the
  method uses features the C# decompiler can't re-emit, or there are version
  mismatches. Use it only for trivial, self-contained edits.
- **IL patch** edits the bytecode directly via dnSpyEx's IL editor. It almost never
  distorts because no recompilation occurs. Prefer it for:
  - flipping a boolean decision (`ldc.i4.0` → `ldc.i4.1`);
  - editing a constant (string / number);
  - `nop`-ing out a check block.

## String decryptor extraction

Many protectors encrypt strings and decrypt them at runtime via a static method.
To recover them in bulk:

1. Locate the decryptor (cross-reference encrypted-looking strings; look for a
   method called from many string loads).
2. Reimplement the decryptor in a small C# script using `dnlib`, or invoke it
   directly if it is pure/managable.
3. Walk the metadata, call the decryptor per encrypted operand, and emit a map of
   `token -> plaintext`.

This is far more reliable than dynamic-only recovery and gives a static artifact
you can re-examine.

## State-machine recognition

`async/await`, `yield`, and compiler-generated enumerators produce state machines
that the C# view flattens confusingly. When a decision seems missing in C#, open
the IL view — the real branch often lives in the state-machine's `MoveNext`.

## Checklist

- [ ] Confirmed managed identity (or routed to native RE)?
- [ ] Packed sample deobfuscated before deep analysis?
- [ ] Key logic verified in IL view (not just C#)?
- [ ] Original + cleaned + (if patched) patched artifacts kept and reproducible?
- [ ] Provenance recorded in the audit ledger?
