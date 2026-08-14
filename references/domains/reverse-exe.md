# Reverse engineering of executables (static)

Use the separate **`reverse-exe`** skill when the evidence is a **suspected malicious executable** (PE/ELF/Mach-O, loader, packed sample, or an embedded payload) and the task calls for static reverse-engineering: injection-target identification, encrypted memory payloads, cryptography recognition, key recovery, or screenshot/capture exfiltration mechanics.

Hard rule shared by that skill: **never execute the sample on the analysis host.** Static analysis only (PE headers, section entropy, embedded resources, import classification, disassembly, string/XOR probing). Dynamic behavior requires an isolated, snapshot-revertible VM or a sandbox API-trace — never the examiner machine.

Prefer DFTK's read-only tools when the evidence is a **benign local artifact** (disk image, DB, archive, PCAP). DFTK has no dynamic malware execution capability.

The two skills share one reasoning contract (claim → evidence → capability → execution → verification) and the same verification levels (VERIFIED / SUPPORTED / CANDIDATE / UNRESOLVED / UNSUPPORTED). The full `reverse-exe` skill lives in the DFTK repo at `skills/reverse-exe/` (a sibling of `skills/dftk`); it is not bundled in the dftk wheel. Copy that directory into your agent skills path.

Note: the `reverse-exe` skill is **methodology-only**. It deliberately carries no exam questions and no answers — those travel with the exam material, not the shared skill.
