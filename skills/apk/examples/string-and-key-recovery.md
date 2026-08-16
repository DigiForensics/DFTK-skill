# String and key recovery from native (.so)

Turn an opaque `libfoo.so` into leads: recover symbols, strings, and any embedded
key material. Pair with `tooling.md` for extraction and `radare2` / `ida-reverse`
for deep analysis.

## Symbol recovery

```bash
# Stripped? C++ mangled names still leak structure
readelf -sW libfoo.so | grep -iE 'encrypt|decrypt|aes|rsa|key|sign|hash'
# Demangle
c++filt < mangled.txt
nm -D libfoo.so            # dynamic symbols
```

## String triage

```bash
strings -n 6 libfoo.so | grep -iE 'aes|rsa|des|base64|key|iv|secret|password|token'
# Recover longer / wide strings
rabin2 -z libfoo.so
```

## Embedded key / IV patterns

```text
□ Fixed 16/24/32-byte blobs near AES S-box references → likely key / IV
□ Hardcoded base64 → decode, check for key-like entropy
□ Concatenated "salt+iterations" near PBKDF2 / OpenSSL EVP markers
□ Weak RNG: srand(time()), rand() instead of CSPRNG
```

## Quality bar
A defensible pass names the algorithm(s) in use, locates the key/IV storage
(`.rodata` offset or `string` literal), and cites the symbol/string that led there.

## Cross-links
- Tooling / extraction → `tooling.md`.
- Deep decompilation → `../../radare2/references/cheatsheet.md`, `../../ida-reverse/`.
