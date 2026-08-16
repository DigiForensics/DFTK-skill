# AST deobfuscation notes

When the producer function is heavily obfuscated, static reading is not enough.
Use an AST-based approach rather than hand-editing.

## When to use

- Control-flow flattening (switch-dispatch over a state variable).
- String-array encryption with an index resolver.
- Proxy / reflective property access hiding the real call targets.
- A JS "VM" (JSVMP) dispatching opcodes.

## Approach

1. Parse the script to an AST (e.g. `acorn` / `babel-parser`).
2. Write small transforms:
   - **string-array resolver** — fold the index expression and inline the literal;
   - **control-flow unflattening** — reconstruct the natural order from the state
     variable;
   - **dead-code elimination** — drop branches that can never execute;
   - **simplify** — constant-fold, inline single-use vars.
3. Re-emit readable JS, then resume the normal Observe/Rebuild flow.

## Notes

- Transform incrementally; verify the deobfuscated output still produces the same
  behavior as the original before relying on it.
- Keep the original and each transform stage; record them in the audit ledger so
  the process is reproducible.
- For an app you do not own, only do this in an authorized assessment context and
  never ship a modified client.
