---
name: identity-federation
description: >-
  Authorized assessment of federated identity — SAML, OIDC, OAuth2 flows, SSO
  misconfiguration, and token-confusion issues. Read-only-first, evidence-preserving.
  Use for reviewing an SSO deployment you own or are authorized to assess; map the flow,
  find misconfigurations, and recommend fixes. Never test against accounts you are not
  authorized to use.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - identity
  - sso
  - saml
  - oidc
  - oauth
  - forensics
---

# Identity federation (SAML / OIDC / OAuth)

Methodology for the **defensive** review of federated identity: SAML, OIDC, and OAuth2
SSO flows. The goal is to map the trust chain, find misconfigurations (signature
coverage, redirect/state/nonce handling, issuer confusion), and recommend hardening — not
to attack accounts you are not authorized to test.

This is a **methodology skill**. The tools are external; nothing here is bundled in the
`dftk` wheel. For raw JWT/API token issues, pair with API-security review; for enterprise
Windows IdP, pair with `server-forensics`.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- Record each captured token, metadata URL, and config observation with provenance.

## Operating contract (read-only, preserve, prove)

1. **Authorized scope.** Use only SSO test accounts and IdP/SP ranges you are authorized to
   assess. Never brute-force or lock real user accounts.
2. **Passive-first.** Prefer capture + config review over active mutation; when you do send
   modified assertions, use an authorized test IdP/SP only.
3. **Record provenance.** Each finding cites the flow step, the captured artifact, and the
   observed value.
4. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE / UNRESOLVED /
   UNSUPPORTED.
5. **Remediation-first.** Every finding ends with a concrete hardening recommendation.

## Workflow

```text
□ Map the flow: User -> SP -> IdP -> Token -> SP
□ Collect: /.well-known/openid-configuration, SAML metadata
□ Check: redirect_uri exact match, state binding, PKCE
□ Check: SAML signature coverage, algorithm downgrade
□ Session fixation & logout invalidation
```

## Classic defect patterns

- **SAML**: unsigned assertions / incomplete signature coverage, algorithm downgrade
  (RSA → none), XML comment / canonicalization tricks.
- **OIDC**: implicit flow without `state`/`nonce`, `redirect_uri` not exact-matched,
  `aud`/issuer confusion across tenants.
- **OAuth2**: missing PKCE on public clients, over-broad scopes, `redirect_uri` injection.

## Tool chain

| Tool | Use |
|------|-----|
| Burp + SAML Raider (authorized) | Assertion editing in a test IdP/SP |
| jwt_tool | JWT segment inspection |
| Browser DevTools | Redirect-chain observation |
| IdP admin logs | Audit |

## Quality bar

A defensible identity-federation pass maps the full SSO flow, reproduces each misconfig
with impact, records provenance, and ends with prioritized hardening — never with an
account-compromise recipe against real users.

---

