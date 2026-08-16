# Local environment rebuild (补环境)

The core of front-end JS reverse: reproduce the target algorithm in Node using
only what the page actually provides. Never invent browser globals.

## Process

1. **Collect evidence first.** From the Observe/Capture phases, record:
   - the exact script that produces the parameter;
   - the functions/ globals it touches (`window`, `document`, `navigator`,
     `crypto`, `localStorage`, `performance`, `Date`, `Math.random`, Web APIs);
   - the runtime values you sampled at the call site.

2. **Build a minimal shim per missing piece.** For each missing global/API:
   - first check whether the page polyfills it inline (search the bundle);
   - only then provide a stub that returns the *observed* value.
   - one patch decision at a time; re-run after each.

3. **Drive by first divergence.** Run the extracted function. On the first error
   or wrong output, fix only that one gap. Do not pre-build a full fake browser.

4. **Verify.** The local script must produce the *same* parameter value as the
   browser for the same inputs. If it diverges, the environment is incomplete —
   return to Capture.

## Common gaps

| Missing | How to handle |
|---------|---------------|
| `window` / `document` | Provide only the properties the code reads; prefer page-supplied values |
| `navigator.userAgent` | Use the exact UA from the captured request |
| `crypto` / `SubtleCrypto` | Use Node `crypto` / `webcrypto` when the algorithm matches |
| `localStorage` / `sessionStorage` | Map to an in-memory object seeded from observed values |
| `performance.now()` / `Date` | Fixed or monotonic stub; note if the value is part of the signature |
| `Math.random` / `Date.now` | If used in the signature, pin to the observed sample |

## Pitfalls

- **Over-shimming** — building a full fake browser hides the real dependency and
  wastes effort. Patch only what the code reaches.
- **Non-determinism** — if the signature uses randomness/time, pin those inputs to
  the captured sample to make the reproduction deterministic for verification.
- **Obfuscation** — if the producer is wrapped in a VM/control-flow flattening,
  do the DeepDive deobfuscation before local rebuild (see `ast-deobf.md`).
