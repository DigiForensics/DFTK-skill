# idapro_* tool catalog (idalib-mcp)

Condensed catalog of the `idalib-mcp` (`idapro_*`) tool surface. Load when
wiring or using the bridge; do not guess tool names.

## Survey (first step)

| Tool | Purpose |
|------|---------|
| `idapro_survey_binary(detail_level=...)` | Quick overview: function count, strings, segments, entry, import categories |
| `idapro_list_funcs(queries)` | List functions (paginated, name filter) |
| `idapro_list_globals(queries)` | List global variables |
| `idapro_entity_query(kind, filter)` | Unified query: functions / globals / imports / strings / names |

## Decompile & disasm

| Tool | Purpose |
|------|---------|
| `idapro_decompile(addr)` | Decompile to pseudocode |
| `idapro_disasm(addr, max_instructions=N)` | Disassemble |
| `idapro_analyze_function(addr, include_asm=false)` | Combined (pseudo + strings + consts + callers + callees + blocks) |
| `idapro_func_profile(queries)` | Function metrics |

## Cross-references & data flow

| Tool | Purpose |
|------|---------|
| `idapro_xrefs_to(addrs)` | Who references the target address |
| `idapro_xref_query(addr, direction)` | Advanced xref (direction/type filter) |
| `idapro_callees(addrs)` | Sub-function list |
| `idapro_callgraph(roots, max_depth)` | Call graph |
| `idapro_trace_data_flow(addr, direction, max_depth)` | Data-flow trace (forward/backward) |

## Search

| Tool | Purpose |
|------|---------|
| `idapro_find_regex(pattern, limit)` | Regex string search |
| `idapro_search_text(pattern)` | Search in disassembly listing |
| `idapro_find_bytes(patterns, limit)` | Byte-pattern search (supports `??` wildcard) |
| `idapro_find(type, targets)` | Advanced search (immediate / string / reference) |

## Memory & data

| Tool | Purpose |
|------|---------|
| `idapro_get_bytes(addrs)` | Read raw bytes |
| `idapro_get_string(addrs)` | Read string |
| `idapro_get_int(queries)` | Read integer value |
| `idapro_get_global_value(queries)` | Read global variable value |
| `idapro_read_struct(queries)` | Read struct field values |
| `idapro_search_structs(filter)` | Search structs |

## Modification (owned artifacts only)

| Tool | Purpose |
|------|---------|
| `idapro_set_comments(items)` | Add comments (asm + decompile synced) |
| `idapro_append_comments(items)` | Append comments |
| `idapro_rename(batch)` | Batch rename (func/global/local/stack var) |
| `idapro_patch_asm(items)` | Patch assembly |
| `idapro_patch(patches)` | Patch bytes |
| `idapro_define_func(items)` | Define function |
| `idapro_undefine(items)` | Undefine |
| `idapro_define_code(items)` | Convert bytes to code |

## Type system & stack

| Tool | Purpose |
|------|---------|
| `idapro_declare_type(decls)` | Declare C struct/enum/union |
| `idapro_set_type(edits)` | Apply type to func/global/local |
| `idapro_infer_types(addrs)` | Infer types |
| `idapro_type_query(queries)` | Query declared types |
| `idapro_type_inspect(queries)` | Inspect type details |
| `idapro_stack_frame(addrs)` | View stack-frame vars |
| `idapro_declare_stack(items)` | Declare stack var |
| `idapro_delete_stack(items)` | Delete stack var |

## Signatures

| Tool | Purpose |
|------|---------|
| `idapro_make_signature(addrs)` | Byte signature for address |
| `idapro_make_signature_for_function(addrs)` | Signature for a function |
| `idapro_find_xref_signatures(addrs)` | Signatures for referencing code |

## Sessions

| Tool | Purpose |
|------|---------|
| `idapro_idalib_open(input_path)` | Open (prefer the script/HTTP path) |
| `idapro_idalib_list()` / `current()` / `switch(id)` / `close(id)` | Session management |
| `idapro_idalib_save(path)` | Save database |
| `idapro_idalib_health(id)` | Worker health check |

## Other

| Tool | Purpose |
|------|---------|
| `idapro_int_convert(inputs)` | Base conversion (use this, do not compute by hand) |
| `idapro_export_funcs(addrs, format)` | Export functions (json / c_header / prototypes) |
| `idapro_py_eval(code)` | Run Python in IDA context |
| `idapro_server_health()` / `server_warmup()` | Server health / warmup |

> Note: debugger tools are hidden by default and enabled via a URL parameter.
