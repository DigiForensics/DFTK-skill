# Database misconfiguration checklist

## Exposure & transport

- [ ] Bound interface (not `0.0.0.0` unless intended + firewalled).
- [ ] TLS enforced for client connections.
- [ ] Management port not publicly reachable.

## Authentication & authorization

- [ ] No default / empty / weak credentials.
- [ ] Application account is least-privilege (not DBA where read-only suffices).
- [ ] Role/grantee review complete; no orphaned privileged roles.
- [ ] Sensitive tables have explicit access control.

## Dangerous features (flag + recommend disable)

- [ ] MSSQL `xp_cmdshell` disabled.
- [ ] Postgres `COPY PROGRAM` / `pg_read_file` restricted.
- [ ] MySQL `file_priv` / `load_file` limited.
- [ ] UDF load path restricted.
- [ ] Redis `requirepass` set; no write-to-file abuse.

## Mongo / NoSQL

- [ ] No operator-injection exposure in query builders.
- [ ] Auth enabled; no `--noauth` deployments.

## Ops

- [ ] Audit logging enabled and shipped.
- [ ] Backup / snapshot permissions tight (not world-readable).

## Output

- Each item → misconfig vs exploitable-chain distinction.
- Prioritize fixes; record in the audit ledger.
