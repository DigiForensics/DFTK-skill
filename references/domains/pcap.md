# Network capture (PCAP) analysis

Use the separate **`pcap`** skill when the evidence is a **packet capture**
(`.pcap` / `.pcapng`) and the task calls for static analysis: filtering HTTP
requests (e.g. all POST methods), following a request's stream, and extracting
URL-encoded parameters (`sign` / `token` / `key`) from request bodies.

Hard rule shared by that skill: **never replay or re-inject the traffic.**
Dissect only (tshark / scapy). Replaying packets can trigger live side effects
on a target — keep it read-only.

Prefer DFTK's read-only tools when the evidence is a **benign local artifact**
(disk image, DB, archive) — DFTK can hash/type the capture *file* but has no
traffic-dissection capability.

The two skills share one reasoning contract (claim → evidence → capability →
execution → verification) and the same verification levels (VERIFIED / SUPPORTED
/ CANDIDATE / UNRESOLVED / UNSUPPORTED). The full `pcap` skill lives in the DFTK
repo at `skills/pcap/` (a sibling of `skills/dftk`); it is not bundled in the
dftk wheel. Copy that directory into your agent skills path.

Note: the `pcap` skill is **methodology-only**. It deliberately carries no exam
questions and no answers — those travel with the exam material, not the shared
skill.
