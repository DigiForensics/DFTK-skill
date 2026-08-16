# .NET obfuscators — de4dot behavior

Identify the protector first (DIE / `file` / dnSpyEx), then choose `de4dot`
flags. Keep the original sample; `de4dot` emits a `-clean` copy.

| Protector | Traits | de4dot handling |
|-----------|--------|-----------------|
| ConfuserEx (1.0.0 / 2.x) | `<module>` anti-tamper, control-flow flattening, string encryption | `de4dot target.exe` usually auto-detects |
| SmartAssembly | `circular` / string encoding, resource compression | `de4dot target.exe` |
| Babel.NET | method-body encryption, control flow | `de4dot target.exe` |
| Eazfuscator.NET | string / resource encryption | `de4dot`; some versions need manual work |
| .NET Reactor | anti-tamper + necrobit | `de4dot`; newer versions may fail → manual |

## Common commands

```bash
de4dot target.exe -o target-clean.exe     # auto-detect
de4dot --type cfze target.exe             # force ConfuserEx
de4dot --type sa target.exe               # force SmartAssembly
de4dot --detect target.exe                # show what it detects
```

## Anti-tamper

Some protectors crash or misbehave if their anti-tamper is intact. If `de4dot`
fails or the cleaned binary won't load, you may need to neutralize the
anti-tamper check (in an authorized context) before deobfuscation. Document the
step and keep the pre-patch original.

## Notes

- Always compare the cleaned binary's behavior/strings against the original to
  confirm deobfuscation succeeded.
- For layered / unknown protectors, run `--detect` and read the log before
  forcing a type.
