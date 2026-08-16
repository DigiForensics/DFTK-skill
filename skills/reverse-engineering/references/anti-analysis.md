# Anti-Analysis: Detection & Bypass (curated)

Detection categories and the signals to record as Evidence. Bypass is for authorized analysis only.

## Linux anti-debug
- `ptrace` self-attach (TracerPid), `/proc/self/status` `State`, `/proc/self/maps` scanner.
- Timing: `clock_gettime`/`rdtsc` deltas around work.
- Signals: SIGTRAP/SIGSEGV based control flow.
- Direct syscalls to bypass ptrace/API hooks.

## Windows anti-debug
- PEB `BeingDebugged`, `NtQueryInformationProcess` (ProcessDebugPort/Flags), Heap Flags.
- TLS callbacks run before the debugger breaks.
- HW/SW breakpoint detection, exception-based control flow.
- Thread hiding, parent-process checks (`explorer.exe` vs `cmd.exe`).

## Anti-VM / sandbox
- `CPUID` hypervisor bit, MAC/OEM vendor strings, tiny disk/RAM/CPU.
- Timing and artifact checks; resource availability.

## Anti-DBI (Frida)
- `frida-gadget`/agent module scans, `/proc/self/maps` `frida` strings, port/task-name probes.

## Code integrity / anti-disassembly
- Self-hashing (CRC/SHA over `.text`); opaque predicates; junk bytes; MBA simplification.

## Bypass strategy
- Record each detection point as Evidence with the triggering API.
- Prefer hardware breakpoints / patch-the-check / higher-fidelity host over fighting every probe.
- If a bypass fails, record it — never conclude "benign" from a failed analysis.
