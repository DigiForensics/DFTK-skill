# Hunting Loop

The threat-hunting loop turns a hypothesis into validated detections. Run it as a repeatable cycle; every iteration ships something durable (a query, a rule, or a closed hypothesis).

## The five steps

1. **Hypothesis** — state what you believe an adversary is doing and why.
   - Good: "An attacker is using LOLBins for lateral movement via `wmic`/`powershell`."
   - Bad: "Check everything for anomalies."
   - Bind the hypothesis to data sources and a success criterion before touching a console.

2. **Data sourcing** — confirm the telemetry exists and is trustworthy.
   - Enumerate available sources (Sysmon, EDR, firewall, proxy, auth logs, DNS).
   - Note coverage gaps explicitly — a hunt on missing telemetry is invalid.
   - Record the time window and host/identity scope.

3. **Analytics** — baseline, then find deviation.
   - Baseline normal behaviour first (who/what/when is typical).
   - Stack, cluster, and rank: rare accounts, new services, anomalous egress, encoded commands.
   - Correlate across sources (same account on many hosts in a short window).

4. **Validation** — prove the signal, not just suspect it.
   - Atomic tests (e.g. Atomic Red Team) **only in an authorized lab**, never against production.
   - Replay historical logs to confirm recall (does the rule fire on known-good incidents?).
   - Label false positives and capture the reason.

5. **Operationalize** — turn the finding into a durable control.
   - Author Sigma (data-source mapped, `falsepositives` stated) or YARA.
   - Link each rule to a response playbook and an owner.
   - Feed confirmed IOCs back to `malware-analysis/` and lateral leads to `digital-forensics/`.

## Output of a loop iteration

| Artifact | Owner | Notes |
|---|---|---|
| Hypothesis note | hunter | what + why + success criterion |
| Queries + results | hunter | with data-source coverage stated |
| Detection (Sigma/YARA) | detection eng | names its false-positive surface |
| Validation evidence | hunter | lab-only, reproducible |

## Quality bar

A loop iteration is complete only when the hypothesis is either supported by evidence or explicitly disproven, and any detection ships with stated false positives. Never validate detections against an unauthorized production environment, and enable the DFTK 3.4.0 audit ledger for any local tooling runs so the hunt is reproducible.
