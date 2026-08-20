"""Validate DFTK-skill structure, local links, and current-release wording."""
from __future__ import annotations

import re
import subprocess
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^)#]+)(?:#[^)]+)?\)")
OBSOLETE_COUNT = re.compile(r"\b68(?:\+)?\s+(?:read-only\s+)?(?:tools|capabilities)\b", re.I)


def main() -> int:
    errors: list[str] = []
    files = sorted(
        path for path in ROOT.rglob("*.md")
        if not any(part.startswith(".") for part in path.relative_to(ROOT).parts)
    )
    for path in files:
        text = path.read_text(encoding="utf-8")
        if path.name != "CHANGELOG.md" and OBSOLETE_COUNT.search(text):
            errors.append(f"{path.relative_to(ROOT)}: obsolete current capability count")
        for line_no, line in enumerate(text.splitlines(), 1):
            for match in LINK.finditer(line):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:", "/", "<")):
                    continue
                if not (path.parent / target).exists():
                    errors.append(f"{path.relative_to(ROOT)}:{line_no}: missing {target}")

    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    for path in skills:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\nname:" not in text or "\ndescription:" not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing skill frontmatter")

    if len((ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()) > 180:
        errors.append("SKILL.md exceeds the 180-line entry-point limit")

    try:
        manifest = json.loads((ROOT / "references" / "capabilities.manifest.json").read_text(encoding="utf-8"))
        skill_version = re.search(r"^version:\s*(.+)$", (ROOT / "SKILL.md").read_text(encoding="utf-8"), re.M)
        if skill_version is None or skill_version.group(1).strip() != manifest.get("toolkit_version"):
            errors.append("SKILL.md version does not match capabilities.manifest.json")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read capability manifest: {exc}")

    sync = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_capabilities.py"), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if sync.returncode:
        errors.append(sync.stdout.strip() or sync.stderr.strip() or "capability catalog check failed")

    skill_catalog = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_skill_catalog.py"), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if skill_catalog.returncode:
        errors.append(skill_catalog.stdout.strip() or skill_catalog.stderr.strip() or "skill catalog check failed")

    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
