# Engagement Playbooks

Each playbook is a concrete ordering of the orchestrator loop for one engagement type.
Capabilities named below are examples — always confirm the exact name with
`dftk_search_capabilities` (the registry grows), then `dftk_describe` it before
running. All runs go through one `case_id`.

## 1. Mobile compromise (Android)

Goal: determine what an app or device did with user data.

1. `dftk_case(action="new", name="mobile-<subject>")` → capture `case_id`.
2. **After every `dftk_run`/`dftk_describe`, check the reply's top-level `ok`** (see the
   *Result verification (mandatory)* section in `../SKILL.md`). `ok: true` means a real
   result (`observation.status` `ok`/`partial`); `ok: false` means `unsupported`/
   `error`/`blocked` — read `observation.status` and fix-and-rerun on `unsupported`/`error`.
3. Static app triage:
   - `dftk_search_capabilities(query="apk endpoints")` → `android.apk_endpoints`
     (extract URL/domain/IP candidates from DEX strings).
   - `dftk_describe(name="android.apk_endpoints")` → needs `path` (APK) + optional `limit`.
   - `dftk_run(name="android.apk_endpoints", params={"path":"<apk>"}, case_id=…)` → `seq=1`.
3. Data inventory:
   - `recipe.android.appdata_triage` — inventory extracted app data + permissions.
4. Comms reconstruction (Chinese alias proves routing):
   - `dftk_search_capabilities(query="短信")` → SMS/contact extraction capability.
   - run it, then `dftk_read_case_run(case_id, seq)` to page rows.
5. Suspicious behaviour: route to `../../malware-analysis/` + `../../mobile-reverse/`
   (Frida/objection recipes) for dynamic checks.
6. Handoff: `dftk_case(action="timeline", …)` then `export format="md"`.

## 2. Host intrusion (Windows / Linux)

Goal: establish timeline, persistence, and blast radius.

1. `dftk_case(action="new", name="host-<hostname>")`.
2. Acquisition order from `../../digital-forensics/` (triage checklist).
3. Windows: `windows.registry_inventory`, `windows.evtx_summary`, `windows.prefetch`,
   `windows.mft`, `windows.lnk`, `windows.usb_artifacts`, `windows.recyclebin` (confirm via search).
   Linux: `linux.auth_events`, `linux.persistence_inventory`, `linux.offline_inventory`.
4. Persistence: `reverse-exe` + `malware-analysis` for dropped binaries; `server-forensics`
   for scheduled tasks / services.
5. Network: `protocol-reverse` + `threat-hunting` for `pcap` / `dns` / `tls` evidence.
6. Handoff with timeline + export.

## 3. Phishing / email authentication

Goal: attribute and prove spoofing or auth failure.

1. `dftk_case(action="new", name="phish-<id>")`.
2. `dftk_search_capabilities(query="邮件")` → email auth / MIME capabilities.
3. `email-security` references/email-auth-checklist.md drives DKIM/SPF/DMARC checks.
4. `digital-forensics` for attachment hash + detonation referral.
5. Export md for the abuse/report.

## 4. Network / protocol / TLS

`protocol-reverse` + `threat-hunting`: `dftk_search_capabilities(query="流量"|"tls")`,
describe, run, page with `value_limit` raised for large captures.

## 5. Web app / thick client / browser extension

`thick-client` (trust boundary) + `browser-extension-reverse` (permission surface) +
`web-forensics`. Search seeds: `browser`, `url`, `cookie`, `storage`.

## 6. Malware / unpacking

`malware-analysis` worked-triage example is the canonical 6-stage flow; `reverse-engineering`
cheatsheet selects the disassembler; `reverse-exe` covers obfuscation/sandbox. Confirm
`sandbox.detonate` safety=`STATEFUL` + `network=true` **before** requesting it.

## 7. Supply chain / SBOM

`supply-chain-security` references/sbom-sca.md; `firmware-forensics` for embedded
extraction. Search `sbom`, `dependency`, `firmware`.

## 8. Identity / SSO

`identity-federation` references/sso-flow-checklist.md; `email-security` for IdP mail.
Search `sso`, `saml`, `oidc`.

---

### Paging large results

When a `dftk_run` result is large:
- `dftk_read_case_run(case_id, seq, evidence_offset=20, evidence_limit=20)` walks evidence
  entries in pages of 20 (max 100).
- `value_offset` / `value_limit` page individual fact values (max 50).

### Safety ceiling

The server enforces `--max-safety` at launch. With `READ_ONLY` (the default in the
shipped `mcp.json`), `STATEFUL` / network capabilities are rejected at call time. To use
them, relaunch the server with `--max-safety STATEFUL` and/or `--allow-network` — never
try to bypass the gate from the agent side.
