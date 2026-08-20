---
name: web-forensics
description: Offline web-application forensics for configuration exports, access logs, deployment trees, and request evidence. Use for authorized review of saved web artifacts; route live hosts to server-forensics and source review to code-audit.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
tags: [forensics, web, logs, configuration, incident-response]
---

# Web Forensics

For an extracted application or web root, run `web.webshell_hunt` before manual
review when the scope includes compromise assessment. It identifies source-linked
request-input, execution, and obfuscation pattern combinations across PHP, JSP,
ASP/ASPX, Node, and Python files. Scores are triage leads only; validate the code
path and deployment context before calling a file a WebShell.

Use this skill for a saved web root, configuration export, access-log collection, or
deployment artifact. It is an offline, evidence-preserving workflow. For a running
server, use `server-forensics`; for source-level security review, use `code-audit`.

## Scope

- Work from an authorized copy of the application tree, logs, or exported container
  filesystem.
- Do not send requests, scan a live target, replay traffic, rotate credentials, or
  modify the deployment.
- Keep configuration values redacted unless the investigation specifically requires
  an authorized disclosure.

## Workflow

1. **Inventory the artifact.** Record source path, hash, apparent framework, web
   server files, deployment manifests, and log date range.
2. **Locate configuration.** Use `web.config_candidates` on an offline root, then
   inspect only the selected file with `web.config_extract`. Keep
   `include_values=false` unless the approved question needs the value.
3. **Summarize requests.** Run `web.access_log_summary` on the relevant log tree.
   Preserve the time range, parser limits, client addresses, methods, status codes,
   and requested URIs.
4. **Correlate.** Join configuration, request, and deployment evidence through a
   concrete key such as timestamp, URI, virtual host, container ID, or release ID.
5. **Report.** Separate configured behavior from observed requests. State missing
   logs, reverse-proxy limitations, and time-zone assumptions.

## DFTK capability loop

```text
dftk_search_capabilities(query="web configuration access log")
dftk_describe(name="web.config_candidates")
dftk_run(name="web.config_candidates", params={"root":"<offline-root>"}, case_id="<case>")
dftk_run(name="web.access_log_summary", params={"root":"<offline-root>"}, case_id="<case>")
```

Confirm parameter names with `dftk_describe`; do not infer a request or exposure from
a configuration string alone.

## Output

Record the artifact hash and root, selected configuration files, log coverage, request
summary, correlation keys, findings, and limitations. Treat credentials, tokens, and
personal data as sensitive case material.

## References

- [Evidence sources and correlation](references/evidence-sources.md)
- [DFTK MCP setup](../../references/mcp-setup.md)
- [Server forensics](../server-forensics/SKILL.md)
- [Source code audit](../code-audit/SKILL.md)
- [Case orchestrator](../case-orchestrator/SKILL.md)
