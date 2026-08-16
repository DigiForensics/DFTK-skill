# DFIR Case Report — {{ case_id }}

## Scope
- Authorization: {{ who / what / window }}
- Evidence type: memory / disk / pcap / host export
- Analyst / time zone:

## Acquisition & preservation
| Artifact | SHA-256 | Acquisition command | Time (UTC) |
|---|---|---|---|
| {{ name }} | {{ hash }} | {{ cmd }} | {{ ts }} |

## Timeline (key events)
- {{ ts }} — {{ event / source }}

## Findings
### F-001 — {{ title }}
- Claim: {{ exact claim addressed }}
- Evidence: {{ source + locator + value }}
- Method/hash: {{ command / artifact hash }}
- Status: VERIFIED / SUPPORTED / CANDIDATE / UNRESOLVED / UNSUPPORTED

## IOCs (declassified by tier)
- Network: {{ ip / domain / url }}
- Host: {{ path / registry / mutex }}
- Hash: {{ sha256 }}

## Audit ledger
- DFTK audit log: {{ path }} (process provenance with evidence hashes)
