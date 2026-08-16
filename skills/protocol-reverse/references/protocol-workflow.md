# Protocol Workflow Quick Reference

## Frame layout checklist
- [ ] Identify magic / fixed header bytes.
- [ ] Determine length-field endianness and whether it includes the header.
- [ ] Locate checksum/CRC/HMAC (often last 2/4 bytes or a header field).
- [ ] Find sequence/nonce fields (incrementing or random per message).
- [ ] Sketch the state machine (Connect → Auth → Ready → Req/Resp → Close).

## Protobuf recovery
```bash
# Unknown protobuf from a captured blob
python3 -m pbkittool blob.bin            # pbtk
# or
protoc --decode_raw < blob.bin           # needs protoc
# or use blackboxprotobuf in Python to explore fields without a .proto
```
Then reconstruct a `.proto` from observed field numbers/types and re-decode to validate.

## Kaitai / ImHex template
- Start from one well-aligned message; define structs for header + body.
- Validate against 3–5 different messages of the same type before trusting the layout.

## Redaction
Always redact credentials, session tokens, and PII in shared decoders and reports.
