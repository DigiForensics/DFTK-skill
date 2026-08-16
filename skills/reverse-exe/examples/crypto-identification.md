# Crypto identification reference

Identify the algorithm a binary uses by its constants and structure — before you
read a single line of disassembly. Read-only-first; `dftk hash` the sample.

## By constant

| Constant | Algorithm |
|----------|-----------|
| AES S-box `637C777B…` (the 256-byte substitution table) | AES (any mode) |
| `0x67452301` / `0xEFCDAB89` (MD init vectors) | MD5 |
| `0x6A09E667` / `0xBB67AE85` | SHA-2 family |
| Large odd modulus + `0x10001` public exponent | RSA |
| Weierstrass / Edwards curve params | ECC (name the curve if visible) |

## By structure

```text
□ Fixed 16-byte IV present → AES-CBC / CTR (random IV ⇒ CBC; counter ⇒ CTR)
□ Key length 16/24/32 bytes → AES-128/192/256
□ Fixed IV reused across runs → note the weakness explicitly
□ PBKDF2 / OpenSSL EVP markers → look for "salt:iterations" near the call
□ Custom RNG or srand(time()) → flag weak randomness
```

## Practical steps

```bash
# Locate the AES S-box / SHA init constants in the binary
rabin2 -z sample | grep -iE 'aes|sha|encrypt'
# Entropy per section — high entropy often means packed crypto
rabin2 -S sample
```

## Quality bar
State the algorithm, the key/IV handling (fixed vs random), and the exact
constant or string that let you identify it. Flag reuse / weak RNG as findings.

## Cross-links
- Obfuscation / sandbox → `obfuscation-and-sandbox.md`.
- Deep decompilation → `../../radare2/references/cheatsheet.md`, `../../ida-reverse/`.
