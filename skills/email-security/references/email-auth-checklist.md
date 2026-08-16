# Email authentication checklist

## Header collection

- [ ] Full raw headers captured (not just the preview).
- [ ] `Received` chain intact and ordered.
- [ ] `From` matches `Return-Path` (envelope sender)?
- [ ] `Reply-To` differs from `From`?

## SPF / DKIM / DMARC

- [ ] `Received-SPF` result (pass / fail / softfail / none).
- [ ] `DKIM-Signature`: domain, selector, `d=` aligned with `From`? Signature valid?
- [ ] `DMARC` result: `dkim=` / `spf=` alignment, `p=` policy (none / quarantine / reject).
- [ ] If all three fail/pass inconsistently, note the alignment gap as the key finding.

## Content / brand

- [ ] Display name impersonates a known brand but domain does not?
- [ ] URLs point to look-alike / newly-registered domains?
- [ ] Urgency / credential-harvest language present?

## Tenant posture (authorized review)

- [ ] Anti-phishing policy enforced?
- [ ] External sender tagging enabled?
- [ ] MFA enforced for all users?
- [ ] OAuth app consent restricted / admin-approved?

## Output

- Summarize as IOCs: sender domains, URL patterns, attachment hashes.
- Map to a detection rule (with `threat-hunting`).
- Record everything in the audit ledger.
