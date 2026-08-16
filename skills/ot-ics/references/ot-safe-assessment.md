# OT safe-assessment guidance

## Before any activity

- [ ] Written authorization: site, segment, active-scan / write permission stated.
- [ ] Maintenance window identified for any active step.
- [ ] Rollback / stop-and-report plan agreed with the site owner.

## Passive-first techniques

- SPAN / TAP the OT network; analyze the mirror, never inject.
- Export engineering files / configs and audit them **offline**.
- Record default creds / cleartext protocols as Findings — do not log in and change them.

## Limited active (authorized only)

- Low-rate identification; respect rate limits and time windows.
- Prefer read-only function codes (e.g., Modbus read) over writes.
- Stop immediately on anomaly; report before continuing.

## Firmware / patch

- Map controller firmware to CVEs; do **not** blind-flash.
- Hand firmware images to `firmware-forensics` for offline analysis.

## Reporting

- Every Finding states physical / process impact.
- Distinguish "exposure observed" from "exploitable in this environment".
- Record authorized boundary + evidence in the audit ledger.
