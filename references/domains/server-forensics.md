# Live server forensics

Use the separate **`server-forensics`** skill when the evidence is a **running server** reached over SSH (or a local shell on the host): partition identity, listening services and exposed ports, web-app config and embedded credentials, live databases (MySQL/MariaDB/PostgreSQL), OpenSSL-encrypted archives, and containerized evidence.

Prefer DFTK's 68 read-only tools when the evidence is a **local file or disk image** (APK, PCAP, SQLite/SQL dump, registry, E01, browser export). DFTK has no tooling for a live host.

The two skills share one reasoning contract (claim → evidence → capability → execution → verification) and the same verification levels (VERIFIED / SUPPORTED / CANDIDATE / UNRESOLVED / UNSUPPORTED). The full `server-forensics` skill lives in the DFTK repo at `skills/server-forensics/` (a sibling of `skills/dftk`); it is not bundled in the dftk wheel. Copy that directory into your agent skills path.
