# thick-client

Authorized security review of desktop thick clients: local storage, update
channels, IPC, traffic, and client-side trust boundaries.

- Read-only-first, evidence-preserving; locate where client-side enforcement and
  secrets live, then report — do not bypass third-party controls you are not
  authorized to test.
- Routes to `dotnet-reverse` / `ida-reverse` / `ghidra-reverse` / `js-reverse` /
  `protocol-reverse` / `supply-chain-security`.

## Files

- `SKILL.md` — the methodology.
- `CHANGELOG.md`
- `LICENSE` — Apache-2.0.
