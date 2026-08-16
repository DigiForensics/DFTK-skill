# database-security

Authorized database security assessment: exposure, authentication/authorization,
dangerous-feature review (xp_cmdshell, COPY PROGRAM, UDF), and misconfiguration.

- Read-only-first, evidence-preserving; no destructive statements on production unless
  explicitly permitted in scope.
- Covers PostgreSQL / MySQL / MSSQL / Mongo / Redis.

## Files

- `SKILL.md` — the methodology.
- `references/db-misconfig-checklist.md` — misconfiguration checklist.
- `CHANGELOG.md`
- `LICENSE` — Apache-2.0.
