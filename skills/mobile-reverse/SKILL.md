---
name: mobile-reverse
description: Authorized Android and iOS application reverse engineering and security analysis — APK/IPA inspection, runtime instrumentation, SSL pinning and root/jailbreak detection review, and mobile crypto extraction. Use for lawful analysis and security testing of mobile apps you are authorized to examine.
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - forensics
  - mobile
  - android
  - ios
  - frida
  - ssl-pinning
  - reverse-engineering
---

# Mobile Reverse Engineering (Android + iOS)

Authorized analysis and security review of mobile applications. Covers static inspection (APK/IPA), dynamic instrumentation (Frida/Objection), protection-mechanism review (SSL pinning, root/jailbreak/anti-debug detection), and extraction of on-device crypto for characterization.

## Operating contract

- Only analyze apps you are authorized to examine (your own, a client's with written scope, or a sanctioned training target).
- Prefer non-invasive analysis; instrumentation is for authorized testing only.
- Work on copies/decrypted binaries; record SHA-256 and reproducible commands.
- Redact API keys, tokens, and PII in any shared output.

## When this skill applies

- Android APK / iOS IPA inspection and security review.
- Runtime dynamic instrumentation and method tracing.
- SSL pinning / root / jailbreak / anti-debug detection review.
- Mobile crypto extraction (AES/RSA/HMAC keys) for characterization.
- Mobile app security assessment (OWASP MASTG aligned).

For static APK artifact parsing (permissions, resources, strings), DFTK already covers much of it — use `dftk` first, then this skill for dynamic/in-depth work.

## Four-phase workflow

### Phase 1 — Information gathering
```text
Android:
□ Obtain APK (Play / APKMirror / adb pull); record SHA-256.
□ Manifest: permissions, exported components, intent filters, backup flag.
□ androguard analyze → components/permissions/signatures.
□ APKLeaks: hardcoded API keys / tokens / secrets.
□ Packer detection (360/Tencent/Bangcle/ijiami).
iOS:
□ Obtain IPA (App Store / ipatool); decrypt with frida-ios-dump / Clutch.
□ Info.plist: ATS, URL schemes, query schemes.
□ class-dump: ObjC class structure; swift-demangle for Swift.
```

### Phase 2 — Static analysis
```text
Cross-platform: JADX (APK → Java), Ghidra/Hopper (.so / Mach-O), radare2/Cutter (CLI).
Android: apktool d app.apk (smali + resources); dex2jar → JD-GUI; smali/baksmali.
iOS: class-dump headers; otool -L (libs); jtool2 (Mach-O); dsymutil (symbols).
```

### Phase 3 — Dynamic analysis (authorized only)
```text
Frida: frida-ps -U; frida-trace -U -i "open*" com.app; custom hooks for params/returns.
Objection: objection -g "com.app" explore → android/ios sslpinning disable, root/jailbreak disable,
          keystore list / keychain dump, env/ls/sqlite connect.
Frida Gadget (no root/jailbreak): inject frida-gadget.so/.dylib, re-sign, install.
```

### Phase 4 — Network analysis
```text
Burp Suite / mitmproxy for HTTP(S) interception; Wireshark for PCAP.
Install CA cert as system cert (Magisk + MoveCert) on Android.
WebSocket / gRPC traffic analysis.
```

## Common protection-mechanism reviews (analysis context)

### SSL pinning
```bash
objection -g "com.app" explore
android sslpinning disable        # or ios sslpinning disable
# Frida generic: frida -U -l ssl_pinning_bypass.js -f com.app
```

### Root / jailbreak detection
```javascript
Java.perform(function() {
  var RootBeer = Java.use("com.scottyab.rootbeer.RootBeer");
  RootBeer.isRooted.implementation = function() { return false; };
});
// iOS: bypass PT_DENY_ATTACH / sysctl kern.proc.pid; Android: ptrace/TracerPid, /proc/self/status
```

### Mobile crypto extraction (characterization)
```javascript
// Android — hook Cipher to capture algorithm + key
Java.perform(function() {
  var Cipher = Java.use("javax.crypto.Cipher");
  Cipher.init.overload('int','java.security.Key').implementation = function(m,k){
    console.log("[Cipher] Key: " + bytesToHex(k.getEncoded())); return this.init(m,k);
  };
});
// iOS — hook CCCrypt
Interceptor.attach(Module.findExportByName("libcommonCrypto.dylib","CCCrypt"), {
  onEnter: function(a){ console.log("CCCrypt op:"+a[0]+" alg:"+a[1]+" key:"+hexdump(a[3],{length:a[4].toInt32()})); }
});
```

## Tooling
| Tool | Platform | Use |
|---|:--:|---|
| JADX | A | Java decompile |
| apktool | A | unpack/rebuild |
| Ghidra | A+I | multi-arch decompile |
| Frida / Objection | A+I | dynamic instrumentation |
| MobSF | A+I | automated SAST+DAST |
| class-dump / jtool2 | I | Mach-O analysis |
| Burp / mitmproxy | A+I | proxy |

A=Android, I=iOS

## Domain references
- Frida + Objection deep usage → `references/frida-objection-deep.md`
- iOS specifics → `references/ios-reverse-guide.md`
- protection bypass review → `references/anti-detection-bypass.md`

## Quality bar
A defensible mobile pass records the app hash, assesses static structure, reviews protection mechanisms (not just bypasses them), extracts/characterizes crypto where authorized, and redacts secrets. It respects scope and device authorization.

---

