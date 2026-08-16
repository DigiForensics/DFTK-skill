---
name: case-orchestrator
description: Plan and run a defensible, evidence-preserving digital-forensics engagement end to end. Routes the engagement goal to the right specialist sub-skills and drives them through the verified DFTK MCP tool loop (case → search → describe → run → read → handoff).
version: 3.3.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags: [orchestration, workflow, case-management, forensics, triage, mcp, agentic]
---

# Case Orchestrator

You are the engagement lead. Given a forensic goal (a compromised phone, a suspect
host, a phishing email, an intruded server, a tampered binary), you turn it into a
**defensible, evidence-preserving workflow** — never a single ad-hoc command.

This skill does not reimplement forensics. It *composes* the specialist sub-skills in
this Skill and executes them through the **DFTK MCP server** (preferred) or the DFTK
CLI (fallback). All evidence is written to one CaseSession so the chain of custody is
continuous and auditable.

## The non-negotiable loop (verified against `dftk` 3.3.0)

Every capability is exercised through this exact sequence. The contract below was
confirmed by a live stdio MCP handshake — the argument names are authoritative.

1. **Open the case** — `dftk_case(action="new", name="<engagement>")`
   → returns `case.case_id`, e.g. `case-20260816T034157Z-ea679b`.
   ⚠️ Subsequent `show` / `timeline` / `export` calls need this **generated case_id**,
   *not* the friendly `name`.
2. **Discover the capability** — `dftk_search_capabilities(query="…", limit=…)`
   Supports natural-language and **Chinese aliases** (`短信`→SMS, `通讯录`→contacts,
   `流量`→pcap, `注册表`→registry, `邮件`→email, …). Returns capability names like
   `android.apk_endpoints`, `binary.pe_inventory`, `recipe.android.appdata_triage`.
3. **Read the contract** — `dftk_describe(name="<capability>")`
   ⚠️ `name` is a **DFTK capability name from step 2** (e.g. `android.apk_endpoints`),
   *never* an MCP tool name like `dftk_doctor`. The result gives exact `parameters`,
   `safety`, `network`, `produces`, and `requires`.
4. **Execute** — `dftk_run(name="<capability>", params={…}, case_id="<case_id>")`
   Persists the run as `seq=1,2,…` inside the case. The server enforces the root,
   safety ceiling, and network gate — you cannot exceed them.
4.5. **Verify the result — NON-NEGOTIABLE** — `dftk_run` returns an honest
   top-level `ok`: `true` when `observation.status` is `ok` / `partial`, `false`
   when `unsupported` / `error` / `blocked`. You may branch on `ok`. When `ok` is
   `false`, read `observation.status` for the reason (and `observation.errors[]`
   for detail) and follow *Result verification (mandatory)* below.
5. **Page the result** — `dftk_read_case_run(case_id="<case_id>", seq=<n>)`
   Reads an already-persisted Observation **without re-running** the tool. Use
   `evidence_offset` / `evidence_limit` / `value_offset` / `value_limit` to walk large
   outputs (512 KB server-side truncation is per-call, not per-evidence).
6. **Hand off** — `dftk_case(action="timeline", case_id="<case_id>")` to review the
   evidence graph, then `dftk_case(action="export", case_id="<case_id>", format="md")`
   for the report.

Doctor / capability inventory: `dftk_doctor()` returns toolkit version, environment,
and safety posture — call it first when onboarding an unfamiliar evidence host.

## Result verification (mandatory)

`dftk_run` returns an honest top-level `ok` that mirrors `observation.status`:
`ok: true` for `ok` / `partial`, `ok: false` for `unsupported` / `error` /
`blocked`. Branch on `ok`; when it is `false`, read `observation.status` for the
reason and `observation.errors[]` for detail:

```
ok = reply.get("ok")
status = reply.get("observation", {}).get("status")
if ok:
    result = reply["observation"]          # safe to consume evidence / facts
elif status == "unsupported":
    # input was not the expected type for this capability
    # -> choose a different capability, or supply real evidence of the right kind
elif status == "error":
    # capability raised: missing param / bad type / missing dependency
    # -> read reply["observation"]["errors"] and correct the call, then re-run (new seq)
elif status == "blocked":
    # server policy refused (safety ceiling / network gate)
    # -> adjust launch policy or choose a permitted capability
```

Re-running to fix a failed call is safe: correcting params produces a **new** `seq`
inside the same case — the earlier failed `seq` stays for the audit trail. Do **not**
declare a finding from a run whose top-level `ok` is `false`.

## Scenario routing

Pick the playbook, then follow the loop. Full steps in `references/playbooks.md`.

| Engagement | Lead sub-skills | Seed queries |
|------------|----------------|--------------|
| Mobile compromise (Android/iOS) | `mobile-reverse`, `apk`, `apk-reverse`, `malware-analysis`, `digital-forensics` | `android`, `短信`, `apk`, `appdata` |
| Host intrusion (Win/Linux) | `digital-forensics`, `server-forensics`, `reverse-exe`, `malware-analysis`, `threat-hunting` | `registry`, `pcap`, `eventlog`, `进程` |
| Phishing / email auth | `email-security`, `digital-forensics` | `邮件`, `email`, `dkim`, `spf` |
| Network / protocol / TLS | `protocol-reverse`, `threat-hunting`, `digital-forensics` | `流量`, `tls`, `dns` |
| Web app / thick client / extension | `thick-client`, `browser-extension-reverse`, `web-forensics` | `browser`, `url`, `cookie` |
| Malware / unpacking | `malware-analysis`, `reverse-engineering`, `reverse-exe` | `pe`, `shellcode`, `yara` |
| Supply chain / SBOM | `supply-chain-security`, `firmware-forensics` | `sbom`, `dependency`, `firmware` |
| Identity / SSO | `identity-federation`, `email-security` | `sso`, `saml`, `oidc` |

## Quality bar

A defensible engagement:
- Opens **one case** and funnels every tool through it (continuous chain of custody).
- Uses `READ_ONLY` / `STATEFUL` only as the server allows; never requests destructive
  or network capability the case does not justify.
- Records **fact vs inference** separately; distinguishes what the tool proved from
  what the analyst suspects.
- Closes with `dftk_case(action="export", format="md")` so the work is reviewable and
  portable.
- Falls back to the CLI (`../../references/direct-cli.md`) only when MCP is unavailable —
  there, root/safety are **not** server-enforced and must be respected manually.

## Domain references — load only when needed

- Scenario steps → `references/playbooks.md`
- MCP launch + tool contract → `../../references/mcp-setup.md`
- Skill ↔ `dftk_*` tool map → `../../references/skill-router.md`
- CLI fallback → `../../references/direct-cli.md`
- Worked transcript → `examples/worked-engagement.md`
- Related specialists: `../malware-analysis/`, `../digital-forensics/`,
  `../mobile-reverse/`, `../reverse-engineering/`, `../threat-hunting/`.
