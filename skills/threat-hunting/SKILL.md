---
name: threat-hunting
description: Blue-team threat hunting and detection engineering — hypothesis-driven hunting, Sigma/YARA detection authoring, SIEM query design, and incident-detection validation. Use for authorized defensive hunting and detection work only.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - forensics
  - dfir
  - blue-team
  - threat-hunting
  - detection
  - sigma
  - yara
---

# Threat Hunting & Detection Engineering

Defensive, blue-team discipline: form a hypothesis, hunt the data, validate, and turn findings into durable detections. Never run attack simulation against an unauthorized production environment.

## Operating contract

- Confirm blue-team authorization and the data-source scope (SIEM, EDR exports, logs).
- Hunt the hypothesis; do not blindly sweep alerts.
- Declassify IOCs by sensitivity before sharing.
- Record queries and results; enable the DFTK 3.3.0 audit ledger where commands run locally.

## When this skill applies

- Hypothesis-driven threat hunting.
- Sigma / YARA detection engineering.
- Alert tuning and false-positive analysis.
- Pairs with `malware-analysis/` (sample IOC → detections) and `digital-forensics/` (case artifacts → lateral hunting).

## Workflow

### 1. Form a hypothesis
```text
Example: attacker used living-off-the-land for lateral movement.
→ Data sources: Sysmon 1/3/10, Windows Security 4624/4648.
→ Success criterion: anomalous parent process or rare account logon source.
```

### 2. Query & stack
```text
□ Baseline: normal admin behavior (time window, hosts).
□ Anomaly: new services, encoded PowerShell, anomalous egress.
□ Correlate: same account across many hosts in a short window.
```

### 3. Operationalize into rules
- Author Sigma (see `../malware-analysis/references/yara-sigma-rules.md`) with explicit `falsepositives` and data-source field mapping.
- Author YARA for file/memory IOCs.
- Link each rule to a response playbook.

### 4. Validate
```text
□ Atomic tests (Atomic Red Team) only in an authorized lab.
□ Replay historical logs to confirm recall.
```

## Tooling
| Tool | Use |
|---|---|
| Sigma CLI / sigmac | rule conversion |
| YARA | file/memory matching |
| SIEM (ELK/Splunk) | querying |
| osquery | endpoint hunting |
| Atomic Red Team | detection validation (lab only) |

## Domain references
- hunting loop → `references/hunting-loop.md`
- YARA/Sigma authoring → `../malware-analysis/references/yara-sigma-rules.md`
- related: `../digital-forensics/`, `../malware-analysis/`

## Quality bar
A defensible hunt states a clear hypothesis and conclusion, documents queries and data sources, and ships detections that name their false-positive surface. It never validates detections against an unauthorized production environment.

---

