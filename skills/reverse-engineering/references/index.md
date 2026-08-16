# Reverse-Engineering Reference Index

Curated map of reverse-engineering reference topics. The full reference set is broad; here we keep the most reusable entries and port more as needed.

| Topic | Source file | When to use |
|---|---|---|
| Static tools | tools.md | GDB, Ghidra, radare2, IDA, Binary Ninja, RISC-V, Unicorn, Python/Android/.NET/packed |
| Dynamic tools | tools-dynamic.md | Frida (hook/anti-debug/mem-scan), angr, lldb, x64dbg, Qiling, Triton |
| Advanced tools | tools-advanced.md | VMProtect/Themida, BinDiff/Diaphora, deobf (D-810/GOOMBA/Miasm), Rizin/Cutter, RetDec, patching |
| Anti-analysis | anti-analysis.md (ported) | ptrace/PEB/NtQuery/TLS/HW-BP, anti-VM, anti-DBI, self-hash, opaque predicates, MBA |
| Foundational patterns | patterns.md | custom VMs, nanomites, self-modifying, XOR, mixed-mode stagers, LLVM obfuscation |
| CTF patterns 1–3 | patterns-ctf*.md | emulator opcodes, LD_PRELOAD, XOR bitmaps, RC4+VM, kernel mazes, ROPfuscation |
| Language-specific | languages.md | Python bytecode, Pyarmor, DOS, HarmonyOS, esolangs, UEFI |
| Language/platform | languages-platforms.md | Rust serde, Android JNI, DEX patch, Frida Firebase, Electron ASAR, Node runtime |
| Compiled langs | languages-compiled.md (ported) | Go, Rust, Swift, Kotlin/JVM, C++ vtable/RTTI |
| Platform RE | platforms.md | macOS/iOS Mach-O, embedded/IoT firmware, kernel drivers, CAN bus |
| Hardware RE | platforms-hardware.md | LCD GPIO, RISC-V, ARM64/AArch64 ROP, qemu-aarch64 |
| Field notes | field-notes.md | quick binary types, anti-debug, CTF case notes |

Use this index to decide which specialist reference to load; do not load everything for every task.
