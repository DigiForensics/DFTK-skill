---
name: code-audit
description: Authorized source-code security review and SAST workflows — Semgrep, CodeQL, dangerous-API hunting, auth/access-control review, crypto misuse, and fix verification. Use for white-box review of code you are authorized to assess.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - forensics
  - security
  - code-audit
  - sast
  - semgrep
  - codeql
  - appsec
---

# Source Code Security Audit

White-box security review of source code you are authorized to assess. Combines automated SAST with mandatory manual verification and fix guidance. This is defensive review, not exploitation.

## Operating contract

- Confirm you have authorized access to the source/repo and the review scope (directory / service / PR diff).
- Never widen scope beyond what was authorized.
- Record findings with reproducible evidence; enable the DFTK 3.4.0 audit ledger for any local tooling runs.

## When this skill applies

- White-box audit, PR/diff security review.
- Semgrep / CodeQL / Bandit / gosec / SpotBugs / FindSecBugs.
- Dangerous API, injection points, broken auth/access control, crypto misuse.
- Pairs with `supply-chain-security/` (dependencies & pipelines) — this skill focuses on first-party logic.

## Workflow

### 1. Scope & threat model
```text
□ Trust boundaries: user input, files, deserialization, SSRF, auth middleware.
□ High-value assets: auth, payments, admin, key handling.
```

### 2. Automated scan
```bash
semgrep --config p/owasp-top-ten .
# or language-specific: bandit (py), gosec (go), SpotBugs+FindSecBugs (java)
```

### 3. Manual verification (MANDATORY)
```text
□ Every SAST hit: reachable? exploitable? false positive?
□ Auth: IDOR / privilege escalation, missing checks, broken multi-tenant isolation.
□ Injection: SQL / command / template / LDAP.
□ Crypto: hardcoded keys, ECB, custom crypto, weak RNG.
```

### 4. Output
```text
Finding: location + data flow + PoC + remediation.
Optional: ATT&CK / CWE id.
```

## Tooling
| Tool | Language / use |
|---|---|
| Semgrep | multi-language fast rules |
| CodeQL | deep data-flow (GitHub) |
| Bandit | Python |
| gosec / staticcheck | Go |
| SpotBugs / FindSecBugs | Java |

## Domain references
- SAST review checklist → `references/sast-review-checklist.md`
- related: `../supply-chain-security/`, `../reverse-exe/` (when only a binary is available)

## Quality bar
A complete audit verifies findings manually (not just scanner output), includes remediation, stays within authorized scope, and states confidence per finding.

---

