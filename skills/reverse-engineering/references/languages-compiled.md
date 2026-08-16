# Compiled-Language Reverse Engineering (curated)

## Go
- Symbols often present (unless stripped): use `GoReSym` for the full metadata map (it recovers `pclntab` even when stripped).
- Recover goroutine semantics, channel ops, and `embed.FS` embedded files.
- `uuid`/C2 enumeration often hides in `go:linkname` or patched bytes — Go binary UUID patching is a known C2 technique.

## Rust
- Demangle with `rustfilt`; recover `Option`/`Result` semantics, `Vec` layouts, panic strings (high-value anchors).
- Trait objects → vtable reconstruction; async state machines leave recognizable shapes.

## Swift
- Demangle with `swift-demangle`; protocol witness tables reveal conformances.

## Kotlin / JVM
- Coroutine state machines compile to recognizable switch dispatchers; `kotlinx.serialization` leaves schema hints.

## C++
- Recover vtables, RTTI (`-dynamic`/`class`）, and STL container patterns (`std::string`/`std::vector` layouts).
- Name mangling: `c++filt` for Itanium ABI.

Tip: when symbols are stripped, lean on string anchors, panic/exception messages, and import clusters rather than guessing.
