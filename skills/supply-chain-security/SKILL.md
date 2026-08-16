---
name: supply-chain-security
description: >-
  Software supply-chain security assessment — SBOM generation/audit, SCA, CI/CD
  pipeline review, container-image analysis, build integrity, dependency provenance,
  and vulnerability reachability. Defensive, evidence-preserving. Use for open-source
  dependency review, third-party component compliance, container hardening, and
  pipeline security gating. Regulation-aware (SBOM mandates, EU CRA).
version: 1.0.0
author: DyNooob @ DigiForensics
license: Apache-2.0
copyright: Copyright 2026 DyNooob @ DigiForensics
tags:
  - supply-chain
  - sbom
  - sca
  - devsecops
  - forensics
---

# Supply chain security

Methodology for assessing the **software supply chain**: what is in your artifacts
(SBOM), whether those components carry known vulnerabilities (SCA), whether the build
and distribution pipeline is trustworthy, and whether container images and dependencies
are hardened. The goal is assurance and remediation guidance, not attack.

This is a **methodology skill**. The tools are external; nothing here is bundled in the
`dftk` wheel. When the evidence is a saved file/archive, prefer `dftk` for structured
Observation/Evidence output.

## Relationship to DFTK

- Enable DFTK's audit ledger (`--audit <path>` or `DFTK_AUDIT_LOG`) while working.
- `dftk hash` is the DFIR-preferred hashing for any artifact under review.
- Pair with `malware-analysis` when a dependency shows malicious behavior, and with
  `code-audit` for first-party source review.

## Operating contract (evidence-preserving, remediation-focused)

1. **Authorized scope.** Assess projects / pipelines you own or are authorized to review.
2. **Record provenance.** Each finding cites the component, version, source, and the
   scan that produced it.
3. **Separate fact from inference.** VERIFIED / SUPPORTED / CANDIDATE / UNRESOLVED /
   UNSUPPORTED. SCA alert ≠ exploitable — verify reachability before rating severity.
4. **Remediation-first.** Every finding ends with a fix or acceptance path, not just a
   flag.

## Six-layer governance framework

```text
Layer 1: Source trust      -> source repo / maintainer / release-history review
Layer 2: Build pipeline    -> CI/CD security gates, signature verification
Layer 3: Artifact integrity-> signing, checksums, SBOM attachment
Layer 4: Runtime protection-> container scanning, admission control
Layer 5: Continuous monitor-> live CVE tracking, reachability analysis
Layer 6: Incident response -> supply-chain incident, rollback strategy
```

## Workflow

### 1. SBOM generation & audit

```text
CycloneDX : cdxgen -> bom.json
SPDX      : sbom-tool generate
Syft      : syft <image|dir> -o spdx-json
```

Audit points: unknown/unauthorized deps, deprecated/unmaintained packages, license
conflicts, direct vs transitive dependency inventory, per-component release timeline
and maintainer status.

### 2. Software composition analysis (SCA)

```bash
osv-scanner scan -r . --format json          # free, Google-maintained
trivy fs .                                   # filesystem scan
trivy image nginx                            # container image
trivy config .                               # IaC config
# Enterprise continuous monitoring:
#   docker run -p 8080:8080 dependencytrack/apiserver  -> upload SBOM
```

### 3. Vulnerability reachability

```text
SCA alert != real risk — only ~15% of SCA alerts are actually reachable.
1. Pull CVE list (Dependency-Track / Trivy)
2. Filter CVSS >= 7.0
3. Reachability for those with PoC:
   - Code Property Graph slicing: trace user input -> vulnerable function
   - LLM-assisted semantic verification of the path
4. Validate PoC in an isolated environment
5. Prioritize by actual impact
```

### 4. CI/CD pipeline security

```text
Security gates:
  commit      -> pre-commit hook: gitleaks (secret scan)
  PR          -> SCA scan (Trivy / OSV-Scanner)
  build       -> artifact signing (cosign)
  push        -> SBOM attach (syft + attest)
  deploy      -> admission control (OPA / Kyverno + image scan)
  runtime     -> continuous vuln monitoring (Dependency-Track)

Pipeline self-security:
  - Pipeline-as-Code audit (GitHub Actions / GitLab CI injection)
  - Runner isolation (prevent malicious build escape)
  - Secret management (Actions Secrets / Vault, no hardcoding)
  - Third-party Action review (pin commit SHA, not tag)
```

### 5. Container image security

```bash
hadolint Dockerfile
trivy image --severity HIGH,CRITICAL nginx:latest
docker scout quickview nginx:latest
cosign sign --key cosign.key myimage:tag
cosign verify --key cosign.pub myimage:tag
```

Prefer minimal base images: distroless → alpine → slim; avoid `latest`.

### 6. Third-party dependency review

```text
New dependency checklist:
  - Maintenance: commits in last 6 months? maintainer active?
  - Security history: past malicious-code植入?
  - Dependency tree: how many transitive deps added?
  - License: compatible with project license?
  - Alternatives: safer option (Snyk Advisor / Socket.dev score)?
Risk matrix:
  high-maintenance x low-dep-count x compatible-license -> low risk
  low-maintenance x high-dep-count x license-conflict  -> high risk
```

## Tool chain

| Tool | Use |
|------|-----|
| OWASP Dependency-Track | Enterprise continuous SCA |
| OSV-Scanner | Free SCA (OSV.dev) |
| Trivy | Image + dependency + IaC scan |
| Syft / cdxgen | SBOM generation |
| Cosign | Container signing |
| Gitleaks | Secret/credential scan |
| CodeQL | Code query + data-flow |

## Quality bar

A defensible supply-chain assessment produces an SBOM, separates reachable from
unreachable findings, reviews the pipeline's own security, and ends with prioritized
remediation — all with reproducible scan commands recorded.

---

