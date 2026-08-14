# APK / Android application static analysis

Use the separate **`apk`** skill when the evidence is an **Android APK** and the
task calls for static analysis: locating the launcher (main) activity and
background-running capability from `AndroidManifest.xml`, identifying the native
library loaded via `System.loadLibrary`, recovering hardcoded keys and crypto
algorithms from the `.so`, or detecting encrypted secondary dex (`.ccb`) payloads
unpacked by a native `decrypt()`.

Hard rule shared by that skill: **never install or execute the app.** Unzip,
manifest-parse, DEX-decompile (jadx/apktool/androguard), native-library
string/constant scan, entropy checks. Dynamic unpacking needs an isolated,
snapshot-revertible VM or a sandbox trace — never the examiner machine.

Prefer DFTK's read-only tools when the evidence is a **benign local artifact**
(disk image, DB, archive). DFTK has no Android execution capability.

The two skills share one reasoning contract (claim → evidence → capability →
execution → verification) and the same verification levels (VERIFIED / SUPPORTED
/ CANDIDATE / UNRESOLVED / UNSUPPORTED). The full `apk` skill lives in the DFTK
repo at `skills/apk/` (a sibling of `skills/dftk`); it is not bundled in the
dftk wheel. Copy that directory into your agent skills path.

Note: the `apk` skill is **methodology-only**. It deliberately carries no exam
questions and no answers — those travel with the exam material, not the shared
skill.
