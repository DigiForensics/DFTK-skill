# js-reverse

Front-end JavaScript reverse-engineering methodology: signature/encryption-chain
location, request-flow observation, runtime sampling, and local (Node)
reconstruction for evidence-based reproduction.

- Read-only-first, evidence-first; build the local environment only from observed
  page evidence.
- Five-phase workflow: Observe → Capture → Rebuild → Patch → DeepDive.
- Complements `protocol-reverse` (raw bytes) and `browser-extension-reverse`.

## Files

- `SKILL.md` — the methodology.
- `references/env-rebuild.md` — local Node reconstruction / environment-patching.
- `references/ast-deobf.md` — AST deobfuscation notes.
- `CHANGELOG.md`
- `LICENSE` — Apache-2.0.
