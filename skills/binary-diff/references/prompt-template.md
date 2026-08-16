# Comparison prompt template

Fill the four code blocks from IDA exports (old = symbolicated, new = not), plus the
symbol list to locate. Output **only** the YAML below — no prose.

```text
I have disassembly outputs and procedure code of the same function.

This is the function for reference:

**Disassembly for Reference**
```c
{disasm_for_reference}
```

**Procedure code for Reference**
```c
{procedure_for_reference}
```

This is the function you need to reverse-engineering:

**Disassembly to reverse-engineering**
```c
{disasm_code}
```

**Procedure code to reverse-engineering**
```c
{procedure}
```

What you need to do is to collect all references to "{symbol_name_list}" in the
function you need to reverse-engineering and output those references as YAML.

Example:
```yaml
found_vcall: # indirect call to virtual function / vfunc pointer fetch
  - insn_va: '0x180777700'
    insn_disasm: call [rax+68h]
    vfunc_offset: '0x68'
    func_name: ILoopMode_OnLoopActivate
  - insn_va: '0x180777778'
    insn_disasm: mov rax, [rax+80h]
    vfunc_offset: '0x80'
    func_name: INetworkMessages_GetNetworkGroupCount

found_call: # direct call to a non-virtual regular function
  - insn_va: '0x180888800'
    insn_disasm: call sub_180999900
    func_name: CLoopMode_RegisterEventMapInternal
  - insn_va: '0x180888880'
    insn_disasm: call sub_180555500
    func_name: CLoopMode_SetSystemState

found_funcptr: # non-virtual regular function pointer
  - insn_va: '0x180666600'
    insn_disasm: lea rdx, sub_15BC910
    funcptr_name: CLoopMode_OnClientPollNetworking

found_gv: # global variable reference
  - insn_va: '0x180444400'
    insn_disasm: mov rcx, cs:qword_180666600
    gv_name: g_pNetworkMessages
  - insn_va: '0x180333300'
    insn_disasm: lea rax, unk_180222200
    gv_name: s_EventManager

found_struct_offset: # struct offset reference (NOT virtual pointers)
  - insn_va: '0x1801BA12A'
    insn_disasm: mov rcx, [r14+58h]
    offset: '0x58'
    size: 8
    struct_name: CResourceService
    member_name: m_pEntitySystem
```

If nothing found, output an empty YAML. DO NOT output anything other than the desired
YAML. DO NOT collect unrelated symbols.
```

## Variable map

| Variable | Source | Note |
|----------|--------|------|
| `{disasm_for_reference}` | OLD IDA export | symbolicated disassembly |
| `{procedure_for_reference}` | OLD IDA export | symbolicated pseudocode |
| `{disasm_code}` | NEW IDA export | un-symbolicated disassembly |
| `{procedure}` | NEW IDA export | un-symbolicated pseudocode |
| `{symbol_name_list}` | extracted from OLD | symbols to locate in NEW |

## Notes

- One function per call; never batch the whole binary.
- Parse the YAML programmatically; apply via rename / comment in the NEW IDB.
- Cache results; spot-check key symbols before trusting the bulk mapping.
