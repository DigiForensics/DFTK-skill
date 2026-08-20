---
name: database-security
description: >-
  Authorized database security assessment — PostgreSQL/MySQL/MSSQL/Mongo/Redis
  exposure, authentication/authorization, dangerous-feature review (xp_cmdshell,
  COPY PROGRAM, UDF), and misconfiguration. Read-only-first, evidence-preserving. Use for
  reviewing an instance you own or are authorized to assess; never run destructive
  statements on production unless explicitly permitted in scope.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - database
  - misconfig
  - dfir
  - forensics
---

# Database security assessment

Methodology for the **defensive** review of databases: exposure, authentication,
authorization, dangerous-feature surface, and misconfiguration. The goal is to find and
fix weak posture (open binds, weak/default creds, over-privileged roles, risky functions)
— not to escalate or exfiltrate.

This is a **methodology skill**. The tools are external; nothing here is bundled in the
`dftk` wheel. When the evidence is a database export/file, prefer `dftk` for structured
Observation/Evidence output.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- `dftk hash` is the DFIR-preferred hashing for any exported artifact.
- Pair with `supply-chain-security` for the application's data-access layer and with
  `server-forensics` for the host.

## Operating contract (read-only, preserve, prove)

1. **Authorized scope.** Review instances you own or are authorized to assess. Write the
   instance, account privilege, and whether write/delete is permitted **in scope** before
   acting.
2. **No destructive statements on production** unless explicitly allowed. Prefer read-only
   enumeration; never `DROP` / `TRUNCATE` / `DELETE` outside an approved change window.
3. **Record provenance.** Each finding cites the instance, the query/config, and the value.
4. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE / UNRESOLVED /
   UNSUPPORTED. Distinguish a misconfiguration from an exploitable chain.
5. **Remediation-first.** End with prioritized fixes, not an attack path.

## Workflow

```text
□ Network exposure & TLS (is it bound to 0.0.0.0? is TLS enforced?)
□ Account roles & grantee (default/weak creds? over-privileged app account?)
□ Sensitive-table access control
□ Dangerous config: file_priv, xp_cmdshell, load_file, COPY PROGRAM, UDF
□ Audit logging enabled?
□ Backup / snapshot permissions
```

## Classic findings

- Unauthenticated / weak-credential access; bind to all interfaces.
- Over-privileged application account (DBA where read-only suffices).
- Risky functions enabled: `xp_cmdshell` (MSSQL), `COPY PROGRAM` (Postgres), UDF load,
  `file_priv` / `load_file` (MySQL).
- NoSQL injection surface (Mongo operator injection), Redis write-to-file / no `requirepass`.

## Tool chain

| Tool | Use |
|------|-----|
| Vendor CLI | Connect & enumerate (read-only) |
| sqlmap | Injection verification (authorized only) |
| nuclei | Known-exposure templates |
| Cloud RDS console | Config audit |

## Quality bar

A complete database-security pass avoids unauthorized writes/deletes, separates
misconfiguration from an exploitable chain, records provenance, and ends with prioritized
hardening — not an escalation recipe.

---

