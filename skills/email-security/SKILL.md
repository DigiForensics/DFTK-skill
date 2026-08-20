---
name: email-security
description: >-
  Authorized email-security review — phishing analysis, header authentication
  (SPF/DKIM/DMARC), BEC patterns, and mailbox/OAuth token-abuse research.
  Read-only-first, evidence-preserving. Use for dissecting a sample phishing email,
  assessing a tenant's anti-phishing posture, and building detection IOCs.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - email-security
  - phishing
  - dfir
  - forensics
---

# Email security & phishing analysis

Methodology for the **defensive** review of email: dissecting a suspicious/phishing
sample, evaluating a tenant's header-authentication and anti-phishing posture, and
researching mailbox / OAuth token abuse. The output is findings + detection IOCs, not a
red-team campaign.

This is a **methodology skill**. The tools are external; nothing here is bundled in the
`dftk` wheel. For attachment binaries, hand off to `malware-analysis`; for the tenant
identity side, hand off to `identity-federation`.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- `dftk` can parse saved email files (`.eml`) and extract headers/attachments as
  read-only artifacts.
- Pair with `threat-hunting` to turn IOCs into detections.

## Operating contract (read-only, preserve, prove)

1. **Authorized scope.** Analyze sample emails you are authorized to handle; review
   tenant config only for tenants you own or are authorized to assess.
2. **Never re-deliver malware.** Do not forward live malicious samples to real users.
3. **Record provenance.** Each finding cites the header/artifact and the value.
4. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE / UNRESOLVED /
   UNSUPPORTED.
5. **Detection-first.** End with IOCs and a tenant-control recommendation, not an attack.

## Workflow

```text
□ Full raw headers: Received chain, From / Return-Path consistency
□ SPF / DKIM / DMARC alignment results
□ URL sandbox + attachment static (with malware-analysis)
□ Brand impersonation + reply-to / reply address mismatch
□ Tenant: anti-phishing policy, external tagging, MFA, OAuth app consent
```

## Tool chain

| Tool | Use |
|------|-----|
| Mail client "View source" | Headers |
| dig / nslookup | SPF / DMARC records |
| urlscan / sandbox | Links & attachments |
| Tenant admin center | Policy review |

## Quality bar

A complete email-security pass gives a complete header-authentication verdict, turns
the sample into detectable IOCs, and reviews the tenant's anti-phishing controls —
without re-delivering the malicious content.

---

