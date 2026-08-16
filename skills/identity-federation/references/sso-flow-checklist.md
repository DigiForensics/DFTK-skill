# SSO flow verification checklist

## Discovery

- [ ] `/.well-known/openid-configuration` retrieved and reviewed.
- [ ] SAML metadata (IdP + SP) retrieved; entityIDs confirmed.
- [ ] Authorization/endpoints and scopes enumerated.

## OIDC / OAuth2

- [ ] `redirect_uri` requires exact match (no substring/wildcard abuse).
- [ ] `state` bound to session and verified on callback.
- [ ] `nonce` present for implicit/hybrid flows.
- [ ] PKCE enforced for public clients.
- [ ] Scopes are least-privilege.

## SAML

- [ ] Entire assertion signed; signature covers the asserted statements.
- [ ] No algorithm downgrade (`<ds:SignatureMethod>` is the expected strong algorithm).
- [ ] `Audience` / `Recipient` / `Destination` validated by the SP.
- [ ] No XML canonicalization / comment injection surface.

## Session & logout

- [ ] Session fixation not possible (new session on auth).
- [ ] Logout invalidates both SP and IdP sessions.
- [ ] Multi-tenant `issuer` confusion not possible (strict `aud`/`iss` checks).

## Output

- Each misconfig → reproduce + impact + hardening recommendation.
- Record in the audit ledger.
