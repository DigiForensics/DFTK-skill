# Verification

These labels describe your reasoning, not a DFTK runtime state.

## VERIFIED
Use only when the claim itself is sufficiently proven with source-traceable evidence and no material unresolved inference remains.

## SUPPORTED
Strong evidence exists, but a material step is indirect/unavailable. State the gap precisely.

## CANDIDATE
Useful lead; not enough to answer as fact.

## UNRESOLVED
Current evidence does not support a defensible answer.

## UNSUPPORTED
Required capability/parser/artifact support is unavailable in the current environment.

## Verification questions
Before writing VERIFIED, ask:
1. Does the evidence prove the exact noun/verb/time relationship in the question?
2. Am I substituting a proxy (mtime, permission, string, registration IP) for the requested event/behavior?
3. Is the evidence source and locator reproducible?
4. Do warnings materially limit coverage?
5. For a multi-hop claim, is every necessary hop supported?
6. Would an independent examiner reasonably derive the same conclusion from these artifacts?


## Persisted result and conclusion integrity

DFTK 3.6 cases record `artifact_sha256` for new runs, and new findings capture an
`evidence_digest` over each cited evidence item. Use case integrity verification
and the findings report before handoff. A value/locator change can make a citation
stale even if the original source SHA-256 remains unchanged. Older case entries
without stored digests retain limited assurance; preserve that limitation.

Use `custody.ledger_verify` or `dftk audit verify` for the ledger/seal result. For
cross-checking complete Observations against the audit trail, use `case.verify`.
Legacy chains remain readable; an intact chain without an external seal is not
proof against an attacker who can rewrite and recompute the entire ledger.
