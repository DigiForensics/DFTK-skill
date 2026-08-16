# SBOM + SCA methodology

## SBOM formats

| Format | Generator | Notes |
|--------|-----------|-------|
| CycloneDX | `cdxgen` | Rich, tooling-friendly |
| SPDX | `sbom-tool`, `syft -o spdx-json` | Standard, license-focused |

## Audit checklist

- [ ] Unknown / unauthorized dependencies present?
- [ ] Deprecated / unmaintained packages?
- [ ] License conflicts vs project license?
- [ ] Direct vs transitive inventory complete?
- [ ] Per-component release timeline + maintainer status recorded?
- [ ] Hashes / pins present for reproducibility?

## SCA reachability (why it matters)

Most SCA tools flag ~15% of alerts as actually reachable. Before rating severity:

1. Pull CVEs (Dependency-Track / Trivy), filter CVSS ≥ 7.0.
2. For PoC-bearing CVEs, build a Code Property Graph slice: trace untrusted input →
   vulnerable sink.
3. Use LLM-assisted semantic verification of the path (DEPTEX-style).
4. Validate in an isolated environment — never against production.
5. Prioritize by *actual* impact, not raw CVSS.

## Notes

- Record every scan command + SBOM path in the audit ledger.
- Hash the SBOM and the scanned artifact (`dftk hash`) for provenance.
- Treat a malicious-dependency finding as a security incident: isolate, report, and
  roll back via the Layer-6 response plan.
