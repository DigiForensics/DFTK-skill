# SAST Review Checklist

A structured pass for white-box source review. Automated scanners produce *candidates*; the auditor produces *verified findings*. Manual verification is mandatory for every hit.

## 0. Setup

- Confirm authorized access to the repo and the review scope (path / service / PR diff).
- Enable the DFTK 3.3.0 audit ledger for any local scans so commands + results are reproducible.
- Pick the right scanner per language: Semgrep (multi), CodeQL (deep data-flow), Bandit (Py), gosec/staticcheck (Go), SpotBugs+FindSecBugs (Java).

## 1. Triage every scanner hit

| Question | Action if no | Action if yes |
|---|---|---|
| Reachable from an untrusted boundary? | downgrade / close | keep |
| Exploitable with realistic preconditions? | mark FP, note why | keep |
| Within authorized scope? | drop | keep |

Do not report a finding you have not manually traced to a reachable sink.

## 2. Category sweep (cover all, don't skip)

- **Injection** — SQL / command / template / LDAP / XPath; check parameterized queries and ORM usage.
- **Auth & access control** — IDOR, missing authz checks, privilege escalation, broken multi-tenant isolation, JWT/token flaws.
- **Cryptography** — hardcoded keys, ECB mode, custom crypto, weak RNG (`Math.random`, `rand()`), missing TLS verification.
- **Deserialization** — unsafe `pickle`/`yaml.load`/`ObjectInputStream`/`.NET BinaryFormatter`.
- **SSRF / file** — unvalidated URLs, path traversal, `eval`/`exec` on tainted input.
- **Secrets** — tokens/keys in source or VCS history (cross-link `supply-chain-security/`).

## 3. Verify with evidence

For each kept finding capture: file:line, the tainted-data path (source → sink), a minimal repro or reasoning, and confidence (high/med/low).

## 4. Report & verify the fix

- Finding = location + data flow + impact + remediation + (optional) CWE / ATT&CK id.
- Re-run the scanner on the patched diff to confirm the hit is gone and no new ones appeared.
- State confidence per finding; never present unverified scanner output as fact.

## Quality bar

A defensible audit verifies findings manually, includes remediation, stays within authorized scope, and states confidence per finding. When only a compiled binary is available, hand off to `reverse-exe/`.
