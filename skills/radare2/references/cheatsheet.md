# radare2 command cheatsheet

Quick-reference for the most-used `r2` / `rabin2` / `rasm2` / `radiff2` /
`rahash2` / `rax2` commands. Reach for this when you need the exact flag, not
from memory.

## Information (rabin2)

```bash
rabin2 -I file        # basic info: arch, bits, os, entry, pic, canary...
rabin2 -S file        # sections
rabin2 -z file        # strings (small)
rabin2 -zz file       # strings (all)
rabin2 -s file        # symbols
rabin2 -i file        # imports          (record as evidence)
rabin2 -E file        # exports (DLL/SYS)
rabin2 -l file        # linked libraries
rabin2 -H file        # headers
```

## Disassembly & analysis (r2 interactive)

```text
aaa           # auto-analyze (functions, refs, etc.)
aaaa          # deeper auto-analysis (slower)
afl           # list functions
afl~main      # filter function list
pdf           # disassemble current function
pdf @ main    # disassemble main
s main        # seek to symbol/address
s 0x401000    # seek to address
iz            # strings in current seek context
iS            # sections
is            # symbols
axt <addr>    # xrefs to address
axf <addr>    # xrefs from address
```

## Hex / data

```text
px 64         # hex dump 64 bytes
pxa          # annotated hex
psz          # string at current address
psz~http     # filter strings
pd 20         # disassemble 20 instructions
```

## Patch (write mode only)

```text
r2 -w file        # open in write mode
oo+               # reopen in write mode from session
wa nop            # write "nop" assembly
wa jmp 0x401050   # write jump
wx 9090           # write raw bytes
wq                # write & quit
```

## Assemble / convert

```bash
rasm2 -d "9090"                    # disassemble bytes
rasm2 -a x86 -b 64 "xor eax,eax"   # assemble
rax2 0x401000                      # hex -> dec
rax2 4198400                       # dec -> hex
rax2 -s hello                      # string -> hex
```

## Diff & hash

```bash
radiff2 a.bin b.bin        # unified diff
radiff2 -C a.bin b.bin     # code diff (similar functions)
rahash2 -a sha256 file     # hash
rahash2 -a md5 file
```

## One-shot automation

```bash
r2 -A -q -c "afl;iz;ii;q" file
```

- `-A` analyze on start, `-q` quiet, `-c` commands. Keep the command list
  readable; chain with `;` and end with `q`.
